<template>
    <div class="center">
        <div style="height: 50px" />
        <v-card
            raised
            rounded
            outlined
            elevation="20"
            max-width="500"
            class="pb-5 shown-card"
        >
            <v-card-title class="justify-center">
                <h4>
                    {{pagetype}}
                </h4>
            </v-card-title>
            <v-spacer />
            <v-card-text>
                <div v-if="pagetype == 'Register'">
                    First Name
                    <v-text-field
                        v-model="fname"
                        prepend-icon="mdi-account"
                    />
                    Last Name
                    <v-text-field
                        v-model="lname"
                        prepend-icon="mdi-account"
                    />
                </div>
                Email
                <v-text-field
                    v-model="email"
                    prepend-icon="mdi-email"
                />
                Password
                <v-text-field
                    v-model="pass"
                    :type="pass_visible ? 'text' : 'password'"
                    prepend-icon="mdi-lock"
                    :append-icon="pass_visible ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="pass_visible = !pass_visible"
                />
                <div v-if="pagetype == 'Register'">
                    Confirm Password
                    <v-text-field
                        v-model="confirm_pass"
                        :type="confirm_pass_visible ? 'text' : 'password'"
                        prepend-icon="mdi-lock"
                        :append-icon="confirm_pass_visible ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="confirm_pass_visible = !confirm_pass_visible"
                    />
                    Secret Key
                    <v-text-field
                        v-model="skey"
                        prepend-icon="mdi-key"
                    />
                </div>
            </v-card-text>
            <v-card-actions>
                <v-row
                    align="center"
                    justify="space-around"
                    v-if="pagetype == 'Login'"
                >
                    <v-btn @click="pagetype = 'Register'">
                        Register
                    </v-btn>
                    <v-btn @click="submit('login')">
                        Login
                    </v-btn>
                </v-row>
                <v-row
                    align="center"
                    justify="space-around"
                    v-if="pagetype=='Register'"
                >
                    <v-btn @click="pagetype = 'Login'">
                        Login
                    </v-btn>
                    <v-btn @click="submit('register')">
                        Register
                    </v-btn>
                </v-row>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            fname: "",
            lname: "",
            email: "",
            pass: "",
            confirm_pass: "",
            skey: "",
            pass_visible: false,
            confirm_pass_visible: false,
            pagetype: "Login"
        }
    },
    methods: {
        showMessage(message) {
            let root = document.getElementsByClassName("shown-card")[0];
            let msg = document.createElement('p');
            msg.textContent = message;
            root.appendChild(document.createElement('br'))
            msg.setAttribute('class', 'text-center');
            msg.style.color = 'red';
            root.appendChild(msg);
        },
        clearMessages() {
            let root = document.getElementsByClassName("shown-card")[0];
            let ps = root.getElementsByTagName('p');
            while (ps.length != 0) {
                ps[0].remove();
            }
            let brs = root.getElementsByTagName('br');
            while (brs.length != 0) {
                brs[0].remove();
            }
        },
        submit(action) {
            this.clearMessages();
            if (action === 'register') {
                let endpoint = 'http://localhost:5000/register';
                if (this.pass !== this.confirm_pass) {
                    this.showMessage('Passwords do not match');
                }
                else if (this.skey !== 'open sesame') {
                    this.showMessage('Incorrect secret key');
                }
                else {
                    axios.post(endpoint, {
                        first: this.fname,
                        last: this.lname,
                        email: this.email,
                        password: this.pass,
                    }).then(response => {
                        if (response === 'failure') {
                            this.showMessage('Email already exists');
                        }
                    }).catch(err =>{
                        console.log(err);
                    });
                }
            }
            if (action == 'login') {
                let endpoint = 'http://localhost:5000/login';
                axios.post(endpoint, {
                    email: this.email,
                    password: this.pass,
                }).then(response => {
                    if (response.usernme === 1) {
                        this.showMessage('Email does not exist');
                    }
                    else if (response.passwrd === 1) {
                        this.showMessage('Incorrect password');
                    }
                }).catch(err =>{
                    console.log(err);
                });
            }
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
