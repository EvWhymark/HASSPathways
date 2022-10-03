<template>
    <div>
        <v-container v-if="filesReceived == 2">
            <Breadcrumbs :breadcrumbs="foundCrumbs" />
            <h1 class="mb-4">
                Modify Course Info
            </h1>
            <div style="max-width: 600px">
                <v-text-field
                    v-model="thisCourse.name"
                    outlined dense
                    label="Course Name"
                    class="text-input"
                />

                <v-row>
                    <v-col>
                        <v-text-field
                            v-model="thisCourse.subj"
                            outlined dense
                            label="Subject Code"
                            class="text-input"
                            placeholder="COGS"
                        />
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="thisCourse.ID"
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
                    v-model="thisCourse.description"
                    outlined dense
                    label="Description"
                    class="text-input"
                />

                <v-text-field
                    v-model="thisCourse.offered.text"
                    outlined dense
                    label="Offered Text"
                    class="text-input"
                />

                <v-checkbox
                    v-model="thisCourse.properties.CI"
                    label="Communication Intensive"
                    class="mt-1 mb-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.properties.HI"
                    label="HASS Inquiry"
                    class="my-1 mb-4"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.offered.fall"
                    label="Offered in Fall"
                    class="my-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.offered.summer"
                    label="Offered in Summer"
                    class="my-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.offered.spring"
                    label="Offered in Spring"
                    class="mt-1 mb-8"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.offered.even"
                    label="Offered even years"
                    class="mt-1"
                    dense :hide-details="true"
                />
                <v-checkbox
                    v-model="thisCourse.offered.odd"
                    label="Offered odd years"
                    class="mt-1 mb-8"
                    dense :hide-details="true"
                />
                <v-select
                    v-model="inPathways"
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
            thisCourse: {},
            filesReceived: 0,
            inPathways: [],
            pathwaysData: {},
            coursesData: {},
            rules: {
                courseCode: value => ('' + value).length === 4
            }
        }
    },
    computed: {
        foundCrumbs() {
            const course = this.getCourse;

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
            for(const path in this.pathwaysData['default']) {
                output.push(path);
            }
            return output;
        },
        getCourse() {
            if(!this.$route.query.class) {
                return null;
            }
            if(!this.coursesData[this.$route.query.class]) {
                return null;
            }
            return this.coursesData[this.$route.query.class];
        },
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/courses.json').then((val) => {
             this.coursesData = Object.freeze(val);
             const course = this.getCourse;
             if(course) {
                 for (const outside in course) {
                     if (this.coursesData[outside] instanceof Object && !(this.coursesData[outside] instanceof Array)) {
                         this.thisCourse[outside] = {};
                         for (const inside in course[outside]) {
                             this.thisCourse[outside][inside] = this.coursesData[outside][inside];
                         }
                     }
                     else {
                         this.thisCourse[outside] = this.coursesData[outside];
                     }
                 }
             }
             else {
                 for (const course in this.coursesData) {
                     for (const outside in this.coursesData[course]) {
                         const attr = this.coursesData[course][outside];
                         if (typeof attr === 'string') {
                             this.thisCourse[outside] = "";
                         }
                         else if (typeof attr === 'boolean') {
                             this.thisCourse[outside] = false;
                         }
                         else if (attr instanceof Array) {
                             this.thisCourse[outside] = [];
                         }
                         else if (attr instanceof Object) {
                             this.thisCourse[outside] = {};
                             for (const inside in attr) {
                                 const attr2 = attr[inside];
                                 if (typeof attr2 === 'string') {
                                     this.thisCourse[outside][inside] = "";
                                 }
                                 else if (typeof attr2 === 'boolean') {
                                     this.thisCourse[outside][inside] = false;
                                 }
                                 else if (attr2 instanceof Array) {
                                     this.thisCourse[outside][inside] = [];
                                 }
                             }
                         }
                     }
                     console.log(this.thisCourse);
                     break;
                 }
             }
             this.filesReceived++;
         });
         import('../../data/json/' + year + '/pathways.json').then((val) => {
             this.pathwaysData = Object.freeze(val);
             const course = this.getCourse;
             if(course) {
                 for(const key in this.pathwaysData) {
                     const singlePathway = this.pathwaysData[key];
                     for(const prio in singlePathway) {
                        if(singlePathway[prio] instanceof Object && !(singlePathway[prio] instanceof Array)) {
                            if(course.name in singlePathway[prio]) {
                                this.inPathways.push(singlePathway.name);
                            }
                        }
                    }
                }
            }
            this.filesReceived++;
         });
    },
    methods: {
        submit() {
            const endpoint = 'http://127.0.0.1:5000/edit'
            axios.post(endpoint, {
                courses: this.thisCourse,
                pathways: this.inPathways,
                type: 'add',
                year: this.$store.state.year
            })
                .then(response => {
                    console.log(response);
                })
                .catch(err =>{
                    console.log(err);
                });
            console.log(this.thisCourse);
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
