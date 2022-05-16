
import AuthRepository from "./AuthRepository";
import UsersRepository from "./UsersRepository";
import TweetsRepository from "./TweetsRepository";

const repositories = {
    "auth": AuthRepository,
    "users": UsersRepository,
    "tweets": TweetsRepository
}
export default {
    get: name => repositories[name]
};