import { defineStore } from "pinia";
import { forgotPasswordSchema, resetPasswordSchema } from "../formik-schemas";
import Repository from "../repositories/RepositoryFactory";
const AuthRepository = Repository.get("auth");
import { notify } from "@kyvg/vue3-notification";

export const useAuthStore = defineStore({
    id: "auth",
    state: () => {
        return {
          auth: null
        }
    },
    getters: {
        isLoggedin() {
            return this.auth ? true : false
        }
    },
    actions: {
        async login(form) {
            try {
                const authObj = await AuthRepository.login(form)
                this.auth = await authObj.data
                console.log(authObj.data)
            } catch (error) {
                console.log(error)
                //on First page load we try to login (request has auth cookie)
                //If the login form is empty and the login failed we don't dispaly the error to not confuse the user
                if(!form) return
                notify({
                    type: "error",
                    text: error.message,
                });
            }
        },
        async register(form) {
            const authObj = await AuthRepository.register(form)
            this.auth = await authObj.data
            console.log("registered and logged in: " + authObj)
        },
        async logout() {
            const authObj = await AuthRepository.logout()
            this.auth = null
        },
        async forgotPassword(form) {
            try {
                const response = await AuthRepository.forgotPassword(form)
                const msg = await response.data
                alert(msg.msg)
            } catch (error) {
                console.log(error)
                notify({
                    type: "error",
                    text: error.message,
                });
            }
        },
        async resetPassword(form, token) {
            try {
                //we get the auth user back from the server so we can login right away
                const response = await AuthRepository.resetPassword(form, token)
                const authObj = await response.data
                this.auth = authObj
            } catch (error) {
                console.log(error)
                if(!form) return
                notify({
                    type: "error",
                    text: error.message,
                });
            }
        }
    }
})