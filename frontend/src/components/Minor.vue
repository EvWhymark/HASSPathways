<template>
    <v-card class="card" elevation="1">
        <h1>Test Minor Page</h1>
        <div class="darken" />
        <v-card-title class="'font-weight-bold text-truncate card-title">
            {{ title }}
        </v-card-title>
    </v-card>
</template>

<script>
export default {
    name: 'Minor',
    props: {
        title: {
            type: String,
            required: true
        }
    },
    data() {return {minorsData: {}};},
    computed: {

    },
    created() {
        const year=this.$store.state.year;
        import('../data/json/' + year+ '')
    }
}
</script>


<style scoped lang="scss">
.bookmark-holder:hover {
    cursor: pointer;
}
.card {
    width: 100%;
    max-width: calc(100vw - 24px);
    display: inline-block;
    vertical-align: top;
}

.darken {
    width: 100%;
    height: 100%;
    background-color: DarkSlateGray;
    opacity: 0.4;
    transition: opacity 0.2s;
}
.card-title {
    color: white;
    position: absolute;
    bottom: 0;
    display: block;
    width: 100%;
}


</style>