<template>
    <div style="text-align: center">
        <v-text-field
            v-model="user"
        ></v-text-field>
        <v-text-field
            v-model="pass"
            :type="pass_visible ? text : password"
        ></v-text-field>
        <v-button>
        </v-button>
    </div>
</template>

<script>


export default {
    data() {
        return {
            user: "",
            pass: "",
            pass_visible: false
        }
    }
}
</script>

<style>

</style>
