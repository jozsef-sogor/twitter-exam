<script setup>
    import { ref, onBeforeMount, watch } from "vue"
	import { storeToRefs } from "pinia" 
    import { useAuthStore } from "../stores/AuthStore"
    import { getFormDataFromObject } from "../helpers"
    import Repository from "../repositories/RepositoryFactory";
    import TweetInput from "../components/TweetInput.vue"
    import TweetCard from "../components/TweetCard.vue"

	//Get auth state to control rendering of tweet input
	const authStore = useAuthStore()
	const { auth } = storeToRefs(authStore)

    const isFeedLoading = ref(false)
    const isTweetPostingLoading = ref(false)

    const tweets = ref([])
    const TweetsRepository = Repository.get("tweets");
    const UsersRepository = Repository.get("users")
    const loadTweets = async () => {
        isFeedLoading.value = true
        try {
            //If logged in fetch own feed not all tweets
            const response = auth.value 
                                ? await UsersRepository.getUserFeed(auth.value.id)
                                : await TweetsRepository.getAllTweets()

            const responseTweets = await response.data
            tweets.value = responseTweets
        } catch (error) {
            console.log(error)
            this.$notify({ type: "error", text: error.message });
        } finally {
            isFeedLoading.value = false
        }
    }
    const handleTweet = tweetObj => {
        console.log(tweetObj)
        const tweetForm = getFormDataFromObject(tweetObj)
        try {
            isTweetPostingLoading.value = true
            TweetsRepository.createTweet(tweetForm)
            loadTweets()
        } catch (error) {
            console.log(error)
            this.$notify({ type: "error", text: error.message });
        } finally {
            isTweetPostingLoading.value = false
        }
    }
    //If auth state changes refetch tweets
    //If login user gets own feed
    //If logout user gets general feed
    watch(
        ()=> auth.value,
        () => {
            loadTweets()
        }
    )
    //Load feed before component mounts
    onBeforeMount(()=> {
        loadTweets()
    })
</script>

<template>
    <div>
        <TweetInput v-if="auth" :is-loading="isTweetPostingLoading" :profile-image="auth.user_image" @post-tweet="handleTweet" />
        <BaseSpinnerBar v-if="isFeedLoading || isTweetPostingLoading" />

        <div v-if="tweets.length" class="flex flex-col-reverse">
            <TweetCard v-for="tweet of tweets" :key="tweet.tweet" :tweet="tweet" />
        </div>
        <div v-else class="flex flex-col-reverse">
            No tweets to show
        </div>
        
    </div>
</template>