from typing import Dict, List, Tuple
import requests
import sys
from lxml import html
import os
from tqdm import tqdm
import json
from lxml import etree
import csv
# this is the modified version of the pathway scraper, this scraper will be for minors
# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 500

# returns the list of catalogs with the newest one being first
# each catalog is a tuple (year, catalog_id) ex: ('2020-2021', 21)
def get_catalogs() -> List[Tuple[str, int]]:
    catalogs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs"
        ).text.encode("utf8")
    )
    catalogs = catalogs_xml.xpath("//catalogs/catalog")

    ret: List[Tuple[str, int]] = []
    # For each catalog get its year and id and add that as as tuples to ret
    for catalog in catalogs:
        catalog_id: int = catalog.xpath("@id")[0].split("acalog-catalog-")[1]
        catalog_year: str = catalog.xpath(".//title/text()")[0].split(
            "Rensselaer Catalog "
        )[1]
        ret.append((catalog_year, catalog_id))

    # sort so that the newest catalog is always first
    ret.sort(key=lambda tup: tup[0], reverse=True)
    return ret


# Returns a list of course ids for a given catalog
def get_minor_ids(catalog_id: str) -> List[str]:
    programs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}search/programs{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return programs_xml.xpath('//result[type="Minor"]/id/text()')

def course_from_string(inp, depts):
    for dept in depts:
        fnd = inp.find(dept)
        if fnd != -1:
            if inp[fnd+8].isdigit() or inp[fnd+8] == "X":
                if inp[fnd+5] != '6':
                    return inp[fnd:fnd+4] + inp[fnd+5:fnd+9]

def handle_electives(cont, courses, depts, year):
    level = '0'
    for char in cont:
        if char.isdigit():
            level = char
            break;
    if level == '0':
        return
    subj = "TEMP"
    for word in cont.split():
        if word in depts:
            subj = word
            break
    if subj == "TEMP":
        return
    path = '../../frontend/src/data/json/' + str(year)
    #f = open(path + '/minor_courses.json', 'r')
    f = open(path + '/courses.json', 'r')
    all_courses = json.load(f)
    for course in all_courses:
        ID = all_courses[course]["ID"]
        subjC = all_courses[course]["subj"]
        if ID[0] == level and subjC == subj:
            courses[course.encode("ascii", "ignore").strip().decode().strip()] = subjC+ID
    f.close()

def parse_courses(core, name, year):
    courses = {}
    depts = []
    f = open('depts.json', 'r')
    f = json.load(f)
    for dept in f:
        depts.append(dept)

    tmp = core.xpath("./content/ul/li/descendant-or-self::*/text()")
    tmp += core.xpath("./courses/adhoc/content/ul/li/descendant-or-self::*/text()")
    content = []

    for t in tmp:
        app = False
        for s in t.split():
            if s in depts:
                app = True
        if app:
            t = (t.strip())
            t = t.encode("ascii", "ignore").strip().decode().strip()
            content.append(t)
    if not(len(content) == 0):
        for cont in content:
            if "transfer" in name.lower():
                crs = cont + "XXXX"
                courses[crs] = crs
            # handle as an elective meaning we will have to some funky stuff
            elif "elective" in cont.lower() or "any" in cont.lower() or "level" in cont.lower():
                handle_electives(cont, courses, depts, year)
            else:
                subjID = course_from_string(cont, depts)
                name = ""
                if "-" in cont:
                    name = cont.split("-", 1)[1].strip()
                else:
                    name = cont.split(subjID[4:])[1].strip()
                courses[name] = subjID
    courses_xml = core.xpath("./courses/include/fallback/title/text()")

    for course in courses_xml:
        # fixes all weird unicode and stuff
        course = course.strip().encode("ascii", "ignore").strip().decode()
        subjID = course_from_string(course, depts)
        name = course.split("-", 1)[1].split("Credit")[0].strip()
        courses[name] = subjID
    if '' in courses.keys():
        del courses['']      
    return courses

def get_minor_data(minor_ids: List[str], catalog_id, year) -> Dict:
    data = {}

    ids = "".join([f"&ids[]={path}" for path in minor_ids])
    url = f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getItems&options[full]=1&catalog={catalog_id}&type=programs{ids}"

    minors_xml = html.fromstring(requests.get(url).text.encode("utf8"))
    minors = minors_xml.xpath("//programs/program[not(@child-of)]");
    for minor in minors:
        name = minor.xpath("./title/text()")[0].strip()
        data[name] = {}
        data[name]["name"] = name
        desc = []
        if len(minor.xpath("./content/p/span/text()")) >0:
            desc = minor.xpath("./content/p/span/text()")
        elif len(minor.xpath("./content/p/text()")) >0:
            desc = minor.xpath("./content/p/text()")
        if len(minor.xpath("./content/p/em/a/text()"))>0:
            desc.append(minor.xpath("./content/p/em/a/text()")[0])
        if len(minor.xpath("./content/ul/li/text()"))>0:
            desc+=minor.xpath("./content/ul/li/text()")
        if len(minor.xpath("./content/ul/li/p/text()"))>0:
            bull=minor.xpath("./content/ul/li/p/text()")
            for i in range(len(bull)-1):
                bull[i]+=','
            desc+=bull
        for i in range(len(desc)):
            desc[i]=desc[i].strip().encode("ascii", "ignore").strip().decode()
        data[name]["description"] = ''
        data[name]["description"]+=' '.join(desc)
        cores = minor.xpath("./cores/core")
        cores += minor.xpath("./cores/core/children/core")
        one_of_index = 0
        for core in cores:
            anchor_name = core.xpath("./anchors/a")[0].get('name').lower()
            desc_more=[]
            desc_more=core.xpath("./content/p/text()")
            for i in range(len(desc_more)):
                desc_more[i]=desc_more[i].strip().encode("ascii", "ignore").strip().decode()
            if len(desc_more)==1 and len(desc_more[0])<2:
                desc_more=[]
            if len(desc_more)==0 and len(core.xpath("./content/p/em/text()"))>0:
                desc_more=core.xpath("./content/p/em/text()")
            if len(desc_more)==0 and len(core.xpath("./content/ul/li/text()"))>0:
                desc_more=core.xpath("./content/ul/li/text()")
            if len(desc_more)==0 and len(core.xpath("./content/ol/li/em/text()"))>0:
                desc_more=core.xpath("./content/ol/li/em/text()")
            for i in range(len(desc_more)):
                desc_more[i]=desc_more[i].strip().encode("ascii", "ignore").strip().decode()
            while '' in desc_more:
                desc_more.remove('')
            if len(core.xpath("./content/p/a/em/text()"))==1 and '@rpi.edu' in core.xpath("./content/p/a/em/text()")[0]:
                desc_more.insert(1,core.xpath("./content/p/a/em/text()")[0])
            elif len(core.xpath("./content/ol/li/em/a/text()"))>0 and '@rpi.edu' in core.xpath("./content/ol/li/em/a/text()")[0]:
                desc_more.insert(1,core.xpath("./content/ol/li/em/a/text()")[0])
            tmp=[]
            for i in desc_more:
                if not (0<len(i)<30 and len(desc_more)<2):
                    test=True
                    if (len(i)>4):
                        if i[0:4].isalpha() and i[0:4]==i[0:4].upper():
                            test=False
                    if test==True:
                        tmp.append(i)
            desc_more=tmp
            if 'recommendedcoursesforstudentsinbachelorofarchitectureprogram'==anchor_name:
                break
            if "require" in anchor_name or "takethefollowing" in anchor_name or "studiocourses" in anchor_name:
                courses = parse_courses(core, name, year)
                if len(courses)>0:
                    data[name]["Required"] = courses
            elif 'architectureminor'==anchor_name:
                courses = parse_courses(core, name, year)
                data[name]["Required"] = courses
            elif ("oneof" in anchor_name or "chooseone" in anchor_name) and "philcourses" not in anchor_name:
                courses = parse_courses(core, name, year)
                one_of_name = "One Of" + str(one_of_index)
                data[name][one_of_name] = courses
                one_of_index += 1
            elif "minor" in anchor_name:
                if name=='Chemistry Minor for Non-Chemistry Majors':
                    continue
                minors = list(filter(lambda x: x != "", \
                 [minor.replace("Minor", "").replace("minor", "").encode("ascii", "ignore").strip().decode() \
                 for minor in core.xpath("./content/descendant::*/text()")]))
                for i in range(len(minors)):
                    if minors[i][-1]=='4' or minors[i][-1]=='3' or minors[i][-1]=='1':
                        minors[i]+=','
                data[name]["description"]+='\n'
                data[name]["description"]+=' '.join(minors)
            else:
                if "additional" in anchor_name or 'note' in anchor_name or 'level' in anchor_name or 'areas' in anchor_name:
                    more=(core.xpath("./title/text()")[0].strip().encode("ascii", "ignore").strip().decode())
                    if len(more)<10:
                        more+=', '
                    desc_more.insert(0,more)
                else:
                    data[name]["remaining_header"] = core.xpath("./title/text()")[0].strip().encode("ascii", "ignore").strip().decode()
                courses = parse_courses(core, name, year)
                if 'Remaining' not in data[name].keys():
                    if len(courses)>0:
                        data[name]["Remaining"] = courses
                else:
                    for i in courses.keys():
                        data[name]["Remaining"][i]=courses[i]
            if len(desc_more)>0:
                data[name]["description"]+='\n'
                data[name]["description"]+=' '.join(desc_more)

        # get rid of duplicates (if it shows up in required, we don't want it to be optional too)
        if "Required" in data[name]:
            for req in data[name]["Required"]:
                for type in data[name]:
                    if (type == "Remaining" or type[0:6] == "One Of") and req in data[name][type]:
                        del data[name][type][req]
        
    return data

#a=get_minor_ids('24')
#b=get_minor_data(['6387'], '24', '2022-2023')
#print(b)

def scrape_minors():
    print("Starting minor scraping")
    catalogs = get_catalogs()

    catalogs = catalogs[:4]
    minors_per_year = {}
    for index, (year, catalog_id) in enumerate(tqdm(catalogs)):
        minor_ids = get_minor_ids(catalog_id)
        data = get_minor_data(minor_ids, catalog_id, year)

        minors_per_year[year] = data
    print("Finished minor scraping")
    return minors_per_year