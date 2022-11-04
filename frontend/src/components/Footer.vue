<template>
    <v-footer class="footer">
        <v-layout column>
            <div>
                Think we can improve? Give us feedback
                <router-link to="/feedback">
                    here
                </router-link>
            </div>
        </v-layout>

        <v-spacer />

        <div>HASS Pathways &copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
</template>

<script>
export default {
    name: 'Footer',
    data() {
        return {

        }
    }
}
</script>

<style scoped>
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    z-index: 999;
}
</style>
