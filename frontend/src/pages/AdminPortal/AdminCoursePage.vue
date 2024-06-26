<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="foundCrumbs" />
            <h1 class="mb-4">
                Modify Course Info
            </h1>
            <div style="max-width: 600px">
                <v-text-field
                    v-model="name"
                    outlined dense
                    label="Course Name"
                    class="text-input"
                />

                <v-row>
                    <v-col>
                        <v-text-field
                            v-model="subj"
                            outlined dense
                            label="Subject Code"
                            class="text-input"
                            placeholder="COGS"
                        />
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="ID"
                            outlined dense
                            label="Course ID"
                            :rules="[rules.courseCode]"
                            maxlength="4"
                            type="number"
                            class="text-input"
                            placeholder="1234"
                        />
                    </v-col>
                </v-row>

                <v-textarea
                    v-model="description"
                    outlined dense
                    label="Description"
                    class="text-input"
                />

                <v-text-field
                    v-model="off_text"
                    outlined dense
                    label="Offered Text"
                    class="text-input"
                />
                <v-row>
                    <v-col>
                        <v-checkbox 
                            v-model="CI"
                            label="Communication Intensive"
                            class="mt-1 mb-1"
                            dense :hide-details="true"
                        />
                        <v-checkbox 
                            v-model="fall"
                            label="Offered in Fall"
                            class="my-1"
                            dense :hide-details="true"
                        />
                        <v-checkbox 
                            v-model="summer"
                            label="Offered in Summer"
                            class="my-1"
                            dense :hide-details="true"
                        />
                        <v-checkbox 
                            v-model="spring"
                            label="Offered in Spring"
                            class="mt-1 mb-8"
                            dense :hide-details="true"
                        />
                    </v-col>
                    <v-col>
                        <v-checkbox 
                            v-model="HI"
                            label="HASS Inquiry"
                            class="my-1 mb-4"
                            dense :hide-details="true"
                        />
                        <v-checkbox 
                            v-model="even"
                            label="Offered even years"
                            class="mt-1 mb-8"
                            dense :hide-details="true"
                        />
                        <v-checkbox 
                            v-model="odd"
                            label="Offered odd years"
                            class="mt-1 mb-8"
                            dense :hide-details="true"
                        />
                    </v-col>
                </v-row>
                <v-row no-gutters>
                    <v-col cols="8">
                        <v-text-field
                            v-model="myCrosslisted"
                            dense
                            label="New Crosslisted"
                            maxlength="9"
                            class="text-input"
                            placeholder="COGS-1234"
                        />
                    </v-col>
                    <v-col cols="4">
                        <v-btn
                            color="green"
                            tile
                            outlined
                            class="ml-2"
                            @click="addCrosslisted()"
                        >
                            <v-icon>
                                mdi-plus-box
                            </v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row no-gutters>
                    <v-chip-group column>
                        <v-chip
                            v-for="cross in crosslisted"
                            :key="cross"
                            class="ma-1"
                            close
                            text
                            @click:close="removeCrosslisted(cross)"
                        >
                            {{ cross }}
                        </v-chip>
                    </v-chip-group>
                </v-row>
                <v-row no-gutters>
                    <v-col cols="8">
                        <v-text-field
                            v-model="myPrerequisite"
                            dense
                            label="New Prerequisite"
                            maxlength="9"
                            class="text-input"
                            placeholder="COGS-1234"
                        />
                    </v-col>
                    <v-col cols="4">
                        <v-btn
                            color="green"
                            tile
                            outlined
                            class="ml-2"
                            @click="addPrereq()"
                        >
                            <v-icon>
                                mdi-plus-box
                            </v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row no-gutters>
                    <v-chip-group column>
                        <v-chip
                            v-for="prereq in prerequisites"
                            :key="prereq"
                            class="ma-1"
                            close
                            text
                            @click:close="removePrereq(prereq)"
                        >
                            {{ prereq }}
                        </v-chip>
                    </v-chip-group>
                </v-row>
                <v-select
                    v-model="myPathways"
                    :items="vselectPathways"
                    multiple
                    label="Pathways"
                    outlined
                    class="text-input"
                    chips
                />
                <v-btn
                    color="green"
                    class="mb-16 font-weight-bold"
                    outlined tile
                    @click="submit()"
                >
                    Submit Changes
                    <v-icon right>
                        mdi-check
                    </v-icon>
                </v-btn>
            </div>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import axios from 'axios'

export default {
    components: {
        Breadcrumbs
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.admin_course_page,
            name: "",
            subj: "",
            ID: 0,
            CI: false,
            HI: false,
            description: "",
            off_text: "",
            fall: false,
            summer: false,
            spring: false,
            odd: false,
            even: false,
            major_rest: false,
            minors: [],
            myPathways: [],
            pathways: [],
            myPrerequisite: '',
            myCrosslisted: '',
            prerequisites: [],
            crosslisted: [],
            pathwaysData: {},
            coursesData: {},

            rules: {
                courseCode: value => ('' + value).length === 4
            }
        }
    },
    computed: {
        foundCrumbs() {
            const course = this.getCourse();
            
            if(course) {
                return breadcrumbs.admin_course_page.map(x => x || {
                    text: course.name,
                    href: '/admin-portal/course?class=' + course.name
                });
            }
            else {
                return breadcrumbs.admin_course_page.map(x => x || {
                    text: "Empty Course",
                    href: '/admin-portal/course'
                });
            }
        },
        vselectPathways() {
            let output = [];
            for(const path in this.pathways) {
                if(this.pathways[path]) {
                    output.push(this.pathways[path]);
                }
            }
            return output;
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/courses.json').then((val) => this.coursesData = Object.freeze(val));
        import('../../data/json/' + year + '/pathways.json').then((val) => {
            this.pathwaysData = Object.freeze(val);
            const course = this.getCourse();
            if(course) {
                this.name = course.name;
                this.subj =  course.subj;
                this.ID = course.ID;
                this.CI = course.properties.CI;
                this.HI = course.properties.HI;
                this.description = course.description;
                this.fall = course.offered.fall;
                this.summer = course.offered.summer;
                this.spring = course.offered.spring;
                this.off_text = course.offered.text;
                this.major_rest = course.properties.major_restricted;
                this.even = course.offered.even;
                this.odd = course.offered.odd;
                this.prerequisites = course.prerequisites;
                this.crosslisted = course['cross listed'];
            }
            let myPathways = new Set();
            for(const key in this.pathwaysData) {
                const singlePathway = this.pathwaysData[key];
                if(course) {
                    for(const prio in singlePathway) {
                        if(singlePathway[prio] instanceof Object && !(singlePathway[prio] instanceof Array)) {
                            const array = singlePathway[prio];
                            if(Object.keys(array).includes(course.name)) {
                                myPathways.add(singlePathway.name);
                            }
                            this.pathways.push(singlePathway.name);
                        }
                    }
                }
                this.pathways.push(singlePathway.name);
            }
            this.myPathways = Array.from(myPathways);
        });
    },
    methods: {
        getCourse() {
            if(!this.$route.query.class) {
                return null;
            }
            if(!this.coursesData[this.$route.query.class]) {
                return null;
            }
            return this.coursesData[this.$route.query.class];
        },
        addPrereq() {
            this.prerequisites.push(this.myPrerequisite);
            this.myPrerequisite = '';
        },
        addCrosslisted() {
            this.crosslisted.push(this.myCrosslisted);
            this.myCrosslisted = '';
        },
        removePrereq(input) {
            let index = this.prerequisites.indexOf(input);
            if(index != -1) {
                this.prerequisites.splice(index, 1);
            }
        },
        removeCrosslisted(input) {
            let index = this.crosslisted.indexOf(input);
            if(index != -1) {
                this.crosslisted.splice(index, 1);
            }
        },
        submit() {
            let newCourse = this.getCourse();
            if(!newCourse) {
                newCourse = {
                    ID: "",
                    description: "",
                    name: "",
                    offered: {
                        even: false,
                        fall: false,
                        odd: false,
                        spring: false,
                        summer: false,
                        text: ""
                    },
                    properties: {
                        CI: 0,
                        HI: 0,
                        major_restricted: 0
                    },
                    subj: ""
                };
                newCourse["cross listed"] = [];
                newCourse["prerequisites"] = [];
            }
            newCourse.name = this.name;
            newCourse.subj = this.subj;
            newCourse.ID = this.ID;
            newCourse.properties.CI = this.CI;
            newCourse.properties.HI = this.HI;
            newCourse.description = this.description;
            newCourse.offered.fall = this.fall;
            newCourse.offered.summer = this.summer;
            newCourse.offered.spring = this.spring;
            newCourse.offered.even = this.even;
            newCourse.offered.odd = this.odd;
            newCourse.offered.text = this.off_text;
            newCourse.properties.major_restricted = this.major_rest;
            newCourse["cross listed"] = this.crosslisted;
            newCourse["prerequisites"] = this.prerequisites;

            const endpoint = 'http://127.0.0.1:5000/edit'
            axios.post(endpoint, {
                courses:newCourse,
                pathways:this.myPathways,
            })
                .then(response => {
                    console.log(response);
                })
                .catch(err =>{
                    console.log(err);
                });
            console.log(newCourse);
            console.log(this.myPathways);
        }
    }
}
</script>

<style scoped>
/* Square inputs :) */
.text-input {
    border-radius: 0;
}
</style>

<style>
/* Fix annoying vuetify bug where the select has extra padding on the bottom */
.v-select.v-select--chips:not(.v-text-field--single-line).v-text-field--box .v-select__selections,
.v-select.v-select--chips:not(.v-text-field--single-line).v-text-field--enclosed
.v-select__selections {
    min-height: 0;
}
</style>
