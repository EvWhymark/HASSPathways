<template>
    <div class="center">
        <div style="height: 50px" />
        <v-card
            raised
            rounded
            outlined
            elevation="20"
            max-width="500"
        >
            <v-card-title class="justify-center">
                <h4>
                    Login
                </h4>
            </v-card-title>
            <v-spacer />
            <v-card-text>
                Username
                <v-text-field
                    v-model="user"
                    prepend-icon="mdi-account"
                />
                Password
                <v-text-field
                    v-model="pass"
                    :type="pass_visible ? text : 'password'"
                    prepend-icon="mdi-lock"
                    :append-icon="pass_visible ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="pass_visible = !pass_visible"
                />
            </v-card-text>
        </v-card>
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

<style scoped>
.center {
    margin: auto;
    width: 40%;
}

</style>
