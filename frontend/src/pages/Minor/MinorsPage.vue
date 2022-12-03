<template>
    <div>
        <v-container>
            <Breadcrumbs :breadcrumbs="breadcrumbs" />
            <h1>Minors</h1>
            <p>
                Select a minor below to get started
            </p>

            <v-divider class="my-4" />

            <div class="pathway-categories fade-in">
                <Minor
                    v-for="item in minor_categories"
                    :key="item.minor_category"
                    :title="item.minor_category"
                    :text="item.minor_category"
                    :minors="item.minors"
                />
            </div>
        </v-container>
    </div>
</template>

<script>
import PathwayCategory from '../../components/PathwayCategory'
import Breadcrumbs from '../../components/Breadcrumbs'
import { pathwayCategories } from '../../data/data.js'
import breadcrumbs from '../../data/breadcrumbs.js'
import { minor_categories } from '../../data/data.js'
import Minor from '../../components/Minor'


export default {
    components: {Minor, Breadcrumbs},
    data: () =>{
        return {
          minor_categories,
          breadcrumbs: breadcrumbs.minors
        }
    },
}
</script>

<style scoped>

.search {
  float:right;
  position:relative;
}


.fade-in{
  animation: fadeIn 1s;
  -webkit-animation: fadeIn 1s;
  -moz-animation: fadeIn 1s;
  -o-animation: fadeIn 1s;
  -ms-animation: fadeIn 1s;
}

@keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-moz-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-webkit-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-o-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

@-ms-keyframes fadeIn {
  0% {opacity:0;}
  100% {opacity:1;}
}

.pathway-categories {
    max-width: 100vw;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    grid-gap: 10px;
}
</style>
