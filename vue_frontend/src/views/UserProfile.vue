<script async setup>
import axios from 'axios';
import { ref, reactive, watch, onBeforeMount, defineAsyncComponent } from "vue"
import { storeToRefs } from "pinia" 
import { useAuthStore } from "../stores/AuthStore"
import { useRoute } from 'vue-router';
import Repository from "../repositories/RepositoryFactory";

const TweetCard = defineAsyncComponent(() => import("../components/TweetCard.vue"))
const EditTweetModal = defineAsyncComponent(() => import("../components/modals/EditTweetModal.vue"))

const UserRepository = Repository.get("users");
const route = useRoute()

const isLoading = ref(false)
const userProfile = ref({})
const userTweets = ref({})
const userId = ref(route.params.uuid)

const loadUserProfile = async() => {
    isLoading.value = true
    const userRequest = UserRepository.getUserById(userId.value)
    const tweetsRequest = UserRepository.getUserTweets(userId.value)
        
    axios.all([userRequest, tweetsRequest])
        .then(axios.spread((...responses) => {
            const userResponse = responses[0]
            const tweetsResponse = responses[1]
            userProfile.value = userResponse.data
            userTweets.value = tweetsResponse.data
    })).catch(error => {
        console.log(error)
        this.$notify({ type: "error", text: error.message });

    }).finally(()=> {
        isLoading.value = false
    })
}

//If the userId changes fetch the new profile (e.g.: navigating from own profile to someone else or navigation between user profiles) the component doesn't remount 
watch(
    () => userId.value,
    () => {
        loadUserProfile()
    }
)


const TweetsRepository = Repository.get("tweets");
const isTweetEditLoading = ref(false)

const authStore = useAuthStore()
const { auth } = storeToRefs(authStore)

const isEditModalOpen = ref(false)
const tweetToEdit = ref(null)

const handleOpenEditModal = (tweet) => {
    tweetToEdit.value = tweet
    isEditModalOpen.value = true
}
const handleCloseEditModal = () => {
    isEditModalOpen.value = false
    tweetToEdit.value = null
}
const handleEditTweet = async (form) => {
    try {
        isTweetEditLoading.value = true
        const response = await TweetsRepository.updateTweet(form, tweetToEdit.value.id)
        const newTweet = await response.data
        
        loadUserProfile()
    } catch (error) {
        console.log(error)
        this.$notify({ type: "error", text: error.message });
    } finally {
        handleCloseEditModal()
        isTweetEditLoading.value = false
    }
}
const handleDeleteTweet = async (tweetId) => {
    console.log(tweetId)
    try {
        isLoading.value = true
        const response = await TweetsRepository.deleteTweet(tweetId)
        const data = await response.data
        console.log(data)
        
        loadUserProfile()
    } catch (error) {
        console.log(error)
        this.$notify({ type: "error", text: error.message });
    } finally {
        handleCloseEditModal()
        isLoading.value = false
    }
}

onBeforeMount(() => {
    loadUserProfile()
})
</script>

<style scoped>
.tweet-card:nth-child(even) {
    background: gray;
}

</style>

<template>
    <section>
        <div class="h-screen p-relative">
            <div class="flex justify-center">
                <!-- User card-->
                <div class="w-full">
                    <div class="w-full h-48 bg-center bg-no-repeat bg-cover">
                        <img class="w-full h-full" src="https://picsum.photos/600/200" alt="">
                    </div>
                    <div class="p-4">
                        <div class="relative flex w-full">
                            <!-- Avatar -->
                            <div class="flex flex-1">
                                <div class="-mt-24">
                                    <div class="relative rounded-full h-36 w-36 avatar">
                                        <img class="relative border-4 rounded-full h-36 w-36 md border-blue" :src="userProfile.user_image" :alt="`${userProfile.user_first_name}'s profile image`">
                                        <div class="absolute"></div>
                                    </div>
                                </div>
                            </div>
                            <!-- Follow Button -->
                            <!--
                            <div class="flex flex-col text-right">
                                <button class="flex items-center justify-center px-4 py-2 ml-auto mr-0 font-bold bg-transparent border rounded max-h-max whitespace-nowrap focus:outline-none focus:ring max-w-max border-blue text-blue hover:border-darkblue hover:shadow-lg">
                                    Edit Profile
                                </button>
                            </div>
                            -->
                        </div>

                        <!-- Profile info -->
                        <div class="justify-center w-full mt-3 ml-3 space-y-1">
                            <!-- User basic-->
                            <div>
                                <h2 class="text-xl font-bold leading-6">{{ userProfile.user_first_name + userProfile.user_last_name }}</h2>
                                <p class="text-sm font-medium leading-5 text-dark">@{{ userProfile.user_name }}</p>
                            </div>
                            <!-- Description and others -->
                            <div class="mt-3">
                                <p class="mb-2 leading-tight">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>
                                <div class="flex text-dark">
                                    <span class="flex mr-2">
                                        <i class="fas fa-calendar"></i>
                                        <span class="ml-2 leading-5">Joined December, 2019</span>
                                    </span>
                                </div>
                            </div>
                            <div class="flex items-start justify-start w-full pt-3 divide-x divide-black divide-solid">
                                <div class="pr-3 text-center"><span class="font-bold">520</span><span class="text-gray-600"> Following</span></div>
                                <div class="px-3 text-center"><span class="font-bold">23,4m </span><span class="text-gray-600"> Followers</span></div>
                            </div>
                        </div>
                    </div>
                    <hr class="border-dark">
                    <BaseSpinnerBar v-if="isLoading || isTweetEditLoading" />
                    <div v-if="userTweets.length" class="flex flex-col-reverse">
                        <TweetCard class="tweet-card" v-for="tweet of userTweets" :key="tweet.tweet" :tweet="tweet" :is-editable="auth && tweet.tweet_creator_id == auth.id" @edit-tweet="handleOpenEditModal" @delete-tweet="handleDeleteTweet" />
                    </div>
                    <div v-else class="flex flex-col-reverse">
                        No tweets to show
                    </div>
                </div>    
            </div>
        </div>

        <EditTweetModal v-if="isEditModalOpen" :tweet="tweetToEdit" @edit-tweet="handleEditTweet" @close="handleCloseEditModal" />
    </section>
</template>