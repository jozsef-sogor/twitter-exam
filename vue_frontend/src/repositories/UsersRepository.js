import Client from './Clients/AxiosClient';
const resource = '/users';

export default {
    getAllUsers() {
        return Client.get(`${resource}`);
    },
    getUserById(userId) {
        return Client.get(`${resource}/${userId}`);
    },
    getUserTweets(userId) {
        return Client.get(`${resource}/${userId}/tweets`)
    },
    getUserFeed(userId) {
        return Client.get(`${resource}/${userId}/feed`)
    },
    create(payload) {
        return Client.post(`${resource}`, payload);
    },
    update(payload, id) {
        return Client.put(`${resource}/${id}`, payload);
    },
    delete(id) {
        return Client.delete(`${resource}/${id}`)
    },

    // MANY OTHER ENDPOINT RELATED STUFFS
};