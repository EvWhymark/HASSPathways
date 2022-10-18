<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>Search for the classes to edit!</h1>
            <h3>Type in the name of the course or the course ID to search for the courses you have taken</h3>
            <div class="search-field">
                <v-text-field
                    v-model="searchValue"
                    outlined
                    rounded
                    solo
                    label="Search Class"
                    class="search-field"
                />
            </div>
            <div v-for="course in filteredCourses" :key="course.name">
                <div v-if="course.name && course.subj && course['cross listed']">
                    <v-btn
                        :id="course.name"
                        :to="`/admin-portal/course?class=${course.name}`"
                    >
                        Edit
                    </v-btn>
                    <label class="label" :for="course.name"> {{ course.name + ", " + course.subj + "-" + course.ID + course['cross listed'].map(el => ' / ' + el).join("") }} </label>
                    <v-btn color="red" @click="chooseCourse(course.name)">
                        Remove
                    </v-btn>
                </div>
            </div>
        </v-container>
        <v-dialog
            v-model="dialog"
            light
            width="500"
            overlay-opacity="0.8"
        >
            <v-card>
                <v-card-text class="pt-4">
                    <p style="font-size: 1.3em">
                        Are you sure you want to delete this course?
                    </p>
                </v-card-text>
                <v-divider />
                <v-card-actions>
                    <v-spacer />
                    <v-btn
                        color="primary"
                        text
                        class="font-weight-bold"
                        @click="remove()"
                    >
                        Yes
                    </v-btn>
                    <v-btn
                        color="primary"
                        text
                        class="font-weight-bold"
                        @click="dialog = false"
                    >
                        No
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
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
            breadcrumbs: breadcrumbs.admin_search_cc_page,
            searchValue: '',
            dialog: false,
            chosenCourse: null,
            coursesData: {}
        }
    },
    computed: {
        filteredCourses() {
            let tempCourses = Object.entries(this.coursesData);

            if(this.searchValue != '' && this.searchValue) {
                tempCourses = tempCourses.filter((item) => {
                    if(!item[1].name) return false;
                    let combinedID = item[1].prefix + '-' + item[1].ID;

                    return item[1].name
                        .toUpperCase()
                        .includes(this.searchValue.toUpperCase()) ||
                        combinedID
                            .toUpperCase()
                            .includes(this.searchValue.toUpperCase());
                })
            }
            return Object.fromEntries(tempCourses);
        }
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/courses.json').then((val) => this.coursesData = Object.freeze(val));
    },
    methods: {
        chooseCourse(course) {
            this.chosenCourse = course
            this.dialog = true
        },
        remove() {
            this.dialog = false;
            const endpoint = 'http://127.0.0.1:5000/edit-course'
            axios.post(endpoint, {
                course: this.chosenCourse,
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
    .label {
        border: 1px solid #666;
        padding: 10px 15px;
        text-align: center;
        display: inline-block;
        font-size: 15px;
        margin: 5px;
        cursor: pointer;
        }
    .search-field {
        width: 400px;
    }
</style>
