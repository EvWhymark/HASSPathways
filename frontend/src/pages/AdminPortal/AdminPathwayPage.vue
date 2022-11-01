<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <v-autocomplete
                v-model="selectedPathway"
                clearable
                rounded
                solo
                :items="autocompletePathways"
                label="Pathways"
                @change="filterCourses()"
            />
            <v-btn @click="submit()">
                Submit
            </v-btn>

            <v-data-table
                :headers="headers"
                :items="filteredCourses"
            >
                <template slot="no-data">
                    No classes found, make sure to select a pathway in the dropdown above
                </template>

                <template #item.name="{ item }">
                    <v-text-field
                        v-model="item.name"
                        single-line
                        clearable
                    />
                </template>

                <template #item.prefix="{ item }">
                    <v-text-field
                        v-model="item.subj"
                        single-line
                        clearable
                    />
                </template>

                <template #item.ID="{ item }">
                    <v-text-field
                        v-model="item.ID"
                        single-line
                        clearable
                    />
                </template>
                <template #item.fall="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.fall"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.summer="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.summer"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.spring="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.spring"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.uia=" {item} ">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.offered.uia"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.category="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-select
                            :items="['Required', 'One Of', 'Remaining']"
                            :value="inCategory(item)"
                            @input="event => changeCategory(item, event)"
                        />
                    </div>
                </template>
                <template #item.CI="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.properties.CI"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.HI="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-checkbox
                            v-model="item.properties.HI"
                            :ripple="false"
                        />
                    </div>
                </template>
                <template #item.delete="{ item }">
                    <div style="display: flex; justify-content: center">
                        <v-btn color="error" @click="remove(item.name)">
                            <v-icon>mdi-delete</v-icon>
                        </v-btn>
                    </div>
                </template>
            </v-data-table>
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
            breadcrumbs: breadcrumbs.admin_pathway_page,
            selectedPathway: "",
            pathways: [],
            headers: [
                { text: 'Course Name', value: 'name', align: 'start', width: '20%'},
                { text: 'Prefix', value: 'prefix', align: 'center'},
                { text: 'Course Code', value: 'ID', align: 'center'},
                { text: 'Fall', value: 'fall', align: 'center'},
                { text: 'Spring', value: 'spring', align: 'center'},
                { text: 'Summer', value: 'summer', align: 'center'},
                { text: 'Category', value: 'category', align: 'center'},
                { text: 'Comm Intensive', value: 'CI', align: 'center'},
                { text: 'Hass Inquiry', value: 'HI', align: 'center'},
                { text: 'Delete From Pathway', value: 'delete', align: 'center'},
            ],
            filteredCourses: [],
            coursesData: {},
            pathwaysData: {}
        }
    },
    computed: {
        autocompletePathways() {
            let output = [];
            for(const path in this.pathways) {
                if(this.pathways[path] != undefined) {
                    output.push(this.pathways[path]);
                }
            }
            return output;
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/pathways.json').then((val) => {
            this.pathwaysData = Object.freeze(val);
            this.pathways = [];
            for(const key in this.pathwaysData) {
                this.pathways.push(this.pathwaysData[key].name);
            }
        });
        import('../../data/json/' + year + '/courses.json').then((val) => this.coursesData = Object.freeze(val));
    },
    methods: {
        toClass(clazz) {
            let urlStart = "/admin-portal/course?class=";
            let urlEnd = clazz;
            const finalURL = urlStart + urlEnd;
            return finalURL;
        },
        inCategory(item) {
            let pathway = this.pathwaysData[this.selectedPathway];
            let cat = "";
            Object.keys(pathway).forEach(key => {
                if (pathway[key] instanceof Object && !(pathway[key] instanceof Array)) {
                    if (item.name in pathway[key]) {
                        if (key.substring(0,6) === "One Of") {
                            key = "One Of";
                        }
                        cat = key;
                    }
                }
            });
            return cat;
        },
        changeCategory(item, selection) {
            console.log(selection);
            let pathway = this.pathwaysData[this.selectedPathway];
            Object.keys(pathway).forEach(key => {
                if (pathway[key] instanceof Object && !(pathway[key] instanceof Array) && item.name in pathway[key]) {
                    delete pathway[key][item.name];
                    if (Object.keys(pathway[key]).length === 0) {
                        delete pathway[key];
                    }
                }
            })
            if (selection === "One Of") selection = "One Of0";
            if (!(selection in pathway)) {
                pathway[selection] = {};
            }
            pathway[selection][item["name"]] = item["subj"] + item["ID"];
            console.log(pathway);
        },
        filterCourses() {
            if(this.selectedPathway == null || this.selectedPathway == "") {
                return [];
            }
            let pathwayID = this.selectedPathway;
            let pathway = this.pathwaysData[pathwayID];
            if(pathway != null) {
                let classes = new Set();
                for(const prio in pathway) {
                    if(pathway[prio] instanceof Object && !(pathway[prio] instanceof Array)) {
                        for(const course in pathway[prio]) {
                            if(this.coursesData[course]) {
                                let clazz = this.coursesData[course];
                                clazz = JSON.parse(JSON.stringify(clazz));
                                classes.add(clazz);
                            }
                        }
                    }
                }
                this.filteredCourses = Array.from(classes);
            }
            else {
                this.filteredCourses = [];
            }
        },
        submit() {
            const endpoint = 'http://127.0.0.1:5000/edit-pathway'
            axios.post(endpoint, {
                courses: this.filteredCourses,
                pathway: this.pathwaysData[this.selectedPathway],
                type: 'update',
                year: this.$store.state.year
            })
            .then(response => {
                console.log(response);
            })
            .catch(err =>{
                console.log(err);
            });
        },
        remove(name) {
            const endpoint = 'http://127.0.0.1:5000/edit-pathway'
            axios.post(endpoint, {
                course: this.coursesData[name],
                pathway: this.pathwaysData[this.selectedPathway],
                type: 'remove',
                year: this.$store.state.year
            })
            .then(response => {
                console.log(response);
            })
            .catch(err =>{
                console.log(err);
            });
        }
    }
}
</script>

<style>

</style>
