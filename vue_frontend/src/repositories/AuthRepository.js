import Client from './Clients/AxiosClient';
//const resource = '/posts';

export default {
    login(form) {
        return Client.post("/login", form);
    },
    logout() {
        return Client.post("/logout");
    },
    register(form) {
        return Client.post("/register", form);
    },
    forgotPassword(form) {
        return Client.post("/forgot-password", form)
    },
    resetPassword(form, token) {
        return Client.post(`/reset-password?token=${token}`, form)
    }

    // MANY OTHER ENDPOINT RELATED STUFFS
};