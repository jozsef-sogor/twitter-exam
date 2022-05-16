import Client from './Clients/AxiosClient';
const resource = '/tweets';

export default {
    getAllTweets() {
        return Client.get(`${resource}`);
    },
    getTweetById(id) {
        return Client.get(`${resource}/${id}`);
    },
    createTweet(form) {
        return Client.post(`${resource}`, form);
    },
    updateTweet(form, id) {
        return Client.put(`${resource}/${id}`, form);
    },
    deleteTweet(id) {
        return Client.delete(`${resource}/${id}`)
    },

    // MANY OTHER ENDPOINT RELATED STUFFS
};