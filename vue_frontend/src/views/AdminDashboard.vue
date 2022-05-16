<script async setup>
import axios from 'axios';
import { ref, onBeforeMount, defineAsyncComponent } from "vue"
import { storeToRefs } from "pinia" 
import { useAuthStore } from "../stores/AuthStore"
import Repository from "../repositories/RepositoryFactory";

const TweetCard = defineAsyncComponent(() => import("../components/TweetCard.vue"))
const EditTweetModal = defineAsyncComponent(() => import("../components/modals/EditTweetModal.vue"))

const authStore = useAuthStore()
const { auth } = storeToRefs(authStore)

const TweetsRepository = Repository.get("tweets");
const isTweetEditLoading = ref(false)

const isLoading = ref(false)
const allTweets = ref({})

const loadTweets = async() => {
    try {
        isLoading.value = true
        const response = await TweetsRepository.getAllTweets()
        const tweets = await response.data
        allTweets.value = tweets
    } catch (error) {
        console.log(error)
        this.$notify({ type: "error", text: error.message });
    } finally {
        isLoading.value = false
    }
}

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
        
        loadTweets()
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
        
        loadTweets()
    } catch (error) {
        console.log(error)
        this.$notify({ type: "error", text: error.message });
    } finally {
        handleCloseEditModal()
        isLoading.value = false
    }
}

onBeforeMount(() => {
    loadTweets()
})
</script>

<template>
    <section>
        <div class="h-screen p-relative">
            <div class="flex justify-center">
                <div class="w-full">
                    <BaseSpinnerBar v-if="isLoading || isTweetEditLoading" />
                    <div v-if="allTweets.length" class="flex flex-col-reverse">
                        <TweetCard v-for="tweet of allTweets" :key="tweet.tweet" :tweet="tweet" :is-editable="auth.access_level >= 200" @edit-tweet="handleOpenEditModal" @delete-tweet="handleDeleteTweet" />
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