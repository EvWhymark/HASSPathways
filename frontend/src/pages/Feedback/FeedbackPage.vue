<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1 class="mb-4">
                Post Feedback
            </h1>
            <div style="max-width: 600px">
                <v-select
                    v-model="selection"
                    :items="options"
                    label="Type of Feedback"
                    outlined dense
                />
                <v-textarea
                    v-model="comment"
                    label="Comment"
                    outlined dense
                />
                <v-btn
                    color="green"
                    @click="submit()"
                >
                    Submit Feedback
                </v-btn>
            </div>
        </v-container>
    </div>
</template>

<script>
import Breadcrumbs from '../../components/Breadcrumbs'
import breadcrumbs from '../../data/breadcrumbs.js'


export default {
    components: {
        Breadcrumbs
    },
    data() {
        return {
            breadcrumbs: breadcrumbs.feedback,
            selection: "",
            comment: "",
            options: ['Bug Report', 'Feature Request', 'Other']
        }
    },
    methods: {
        submit() {

        }
    }
}

</script>

<style>

</style>
