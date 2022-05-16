<script setup>
import { ref, reactive, watch } from "vue"

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false
    },
    profileImage: {
        type: String,
        default: ""
    }
})
const emit = defineEmits(["postTweet"])
const tweet = reactive({tweet_content: ""})
//const isLoading = ref(props.isLoading)
const handlePostTweet = () => {
    emit("postTweet", tweet)
}

//If the isLoading value changes form true to false 
//reset the text area (isLoading trns true when post requests starts, and when it conludes it changes back to false)
watch(
    ()=>props.isLoading,
    (newVal)=> {
        console.log("wathc running")
        console.log(newVal, !newVal)
        if(!newVal) tweet.tweet_content = ""
    }
)
</script>

<template>
    <div class="flex px-5 py-3 border-b-8 border-lighter">
        <div class="flex-none">
            <img :src="props.profileImage" class="flex-none w-12 h-12 border rounded-full border-lighter"/>
        </div>
        <form @submit.prevent="handlePostTweet" class="relative w-full px-4">
            <textarea :disabled="props.isLoading" v-model="tweet.tweet_content" placeholder="What's up?" class="w-full pb-3 mt-3 focus:outline-none"/>
            <div class="flex items-center">
                <i class="mr-4 text-lg text-blue far fa-image"></i>
            </div>
            <!--
            <button :disabled="props.isLoading" type="submit" class="absolute bottom-0 right-0 h-10 px-4 font-semibold text-white rounded-full bg-blue hover:bg-darkblue focus:outline-none">
                Tweet
            </button>
            -->
            <div class="absolute bottom-0 right-0">
                <BaseButton :isLoading="props.isLoading">Tweet</BaseButton>
            </div>
        </form>
    </div>
</template>