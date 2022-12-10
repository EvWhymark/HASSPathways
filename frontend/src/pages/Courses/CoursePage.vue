<template>
    <v-container v-if="course.name">
        <Breadcrumbs :breadcrumbs="breadcrumbs" />
        <div class="header">
            <h1>{{ course.subj }}-{{ course.ID }}: {{ course.name }}</h1>
        </div>
        <p>{{ course.description }}</p>
        <template v-if="course.professors.length !== 0">
            <h2>Professors:</h2>
            <ul>
                <li v-for="(prof, index) in course.professors" :key="prof">
                    <h4> {{ prof }} </h4>
                    <div v-if="professorsData[prof]">
                        {{ professorsData[prof].num_ratings }} Rating(s): {{ professorsData[prof].rating }}/5.0
                        <br>
                        <a :href="`https://www.ratemyprofessors.com/professor?tid=${encodeURIComponent(professorsData[prof].rmp_id)}`"> RateMyProfessor Page </a>
                    </div>
                    <div v-if="profSec[prof].length !== 0" class="open-close-btn">
                        <v-btn @click="all(index)">
                            expand
                        </v-btn>
                        <v-btn @click="none(index)">
                            close
                        </v-btn>
                        <v-expansion-panels v-model="panel[index]" multiple>
                            <v-expansion-panel v-for="sec in profSec[prof]" :key="sec">
                                <v-expansion-panel-header>Section information</v-expansion-panel-header>
                                <v-expansion-panel-content>
                                    Days: {{ course.sections['' + sec].days }} <br>
                                    Time: {{ course.sections['' + sec].time }} <br>
                                    Location: {{ course.sections['' + sec].location }} <br>
                                    Type: {{ course.sections['' + sec].type }} <br>
                                    CRN: {{ course.sections['' + sec].crn }} <br><br>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </div>
                    <div v-else>
                        No sections found for this professor
                    </div>
                    <br>
                </li>
            </ul>
        </template>
        <template v-else>
            <h3>This class is not being provided in the current semester</h3>
        </template>
        <h3>Leave your comment for this class: </h3>
        <input v-model="comment" type="text" placeholder="Your comment">
        //"submit_comment" was planed to send user's input and the current course name
        //to flask after using click "comment if", but there are some frontend issue that
        //I can't fix it, so it is not working yet.
        <button type="button" v-on:click="submit_comment">
            Comment it
        </button>
        {{this.comment}}
        <h3><br></h3>
        <template>
            <div>
                <Rating :star="this.star" :disabled="disabled" :maxstars="this.maxstars" :starsize="this.starsize" :hasresults="this.hasresults" :hasdescription="this.hasdescription" :ratingdescription="this.ratingdescription" />
            </div>
        </template>
        <h3>Comments from other users</h3>
        <CourseTableModifiers
            class="mt-4 class-card__subtitle__modifiers"
            :item="course"
        />
        <v-divider class="my-4" />
    </v-container>
</template>

<script>
import { courseCategories } from '../../data/data.js'
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'
import CourseTableModifiers from '../../components/CourseTableModifiers'
import comments from './comments.json'
import Rating from './rating'

export default {
    // name: 'app',
    components: {
        Breadcrumbs,
        CourseTableModifiers,
        Rating
    },
    data() {
        return {
            coursesData: {},
            professorsData: {},
            panel: [],
            comment: "",
        }
    },
    computed: {
        // Get ID of course
        courseID() {
            let courseID = this.$route.query.course;
            return courseID;
        },
        // Get course object
        course() {
            if(!this.coursesData[this.courseID]) {
                return {};
            }
            return this.coursesData[this.courseID];
        },
        categoryName() {
            for (let category in courseCategories)
                if (category.courses.includes(this.courseID))
                    return category.name;
            return '';
        },
        breadcrumbs() {
            return breadcrumbs.course_template.map(x => x || {
                text: this.course.name, 
                href: 'course?course=' + encodeURIComponent(this.courseID)
            })
        },

        // Correspond Professors and their own section(s)
        profSec(){
            let profSec = {};
            for (let i = 0; i < this.course.professors.length; i++) {
                let prof = this.course.professors[i];
                let sec = [];
                for (var section in this.course.sections) {
                    if (this.course.sections[section]["instructor"] === prof){
                        sec.push(section);
                    }
                }
                profSec[prof] = sec;
            }
            return profSec;
        },
        numSections() {
            return this.course.sections.length;
        },
    },
    created() {
        const year = this.$store.state.year;
        import('../../data/json/' + year + '/courses.json').then((val) => {
            this.coursesData = Object.freeze(val);
            let courseID = this.$route.query.course;
            if (!Object.keys(this.coursesData).includes(courseID)) {
                this.$router.push('/404');
            }
        });
        import('../../data/json/professors.json').then((val) => {
            this.professorsData = Object.freeze(val);
        });
    },
    methods: {
        all(prof) {
            let tmpPanel = []
            for (let i = 0; i < this.course.professors.length; i++) {
                if (i == prof)
                    tmpPanel.push([...Array(this.profSec[this.course.professors[prof]].length).keys()].map((_k,i) => i));
                else
                    tmpPanel.push(this.panel[i]);
            }
            this.panel = tmpPanel
        },
        // this function is suppose to send infromation to flask and store the information
        // to .json file using flask, but there is an error in backend, so it is not 
        // working
        submit_comment(){
            const coursename = this.course.name;
            const userInput = this.comment; // Get the user's input
            fetch('/submit-comment', {
                method: 'POST',
                body: JSON.stringify({ user_input: userInput, course_name: coursename}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
            .then(result => { 
                if (result.status === "success") {
                    this.reload;
                }
                else{
                    alert("An error occurred: " + result.message);
                }
            })
        },
        none(prof) {
            let tmpPanel = []
            for (let i = 0; i < this.course.professors.length; i++) {
                if (i == prof)
                    tmpPanel.push([]);
                else
                    tmpPanel.push(this.panel[i]);
            }
            this.panel = tmpPanel
        }
    }
}

</script>

<style scoped>
 .homepage-btn {
     width: 350px;
     height: 50px;
 }
 .btn-container {
     padding: 10px 0;
     display: grid;
     justify-items: center;
     align-items: center;
     grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
     grid-gap: 10px;
     display: flex;
     flex-wrap: wrap;
     justify-content: center;
 }

 .open-close-btn
    {
        padding: 10px 0;
        justify-items: center;
        align-items: center;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        grid-gap: 10px;
        display: flex;
        flex-wrap: wrap;
    }
</style>
