<script setup>
import { useRouter } from "vue-router"

const props = defineProps({
    tweet: {
        type: Object,
        required: true
    },
    isEditable: {
      type: Boolean,
      default: false
    }
})

const emit = defineEmits(["edit-tweet", "delete-tweet"])

const router = useRouter()

const handleEditTweet = () => {
  emit("edit-tweet", props.tweet)
}

const handleDeleteTweet = () => {
  emit("delete-tweet", props.tweet.id)
}
</script>

<template>
    <div class="flex w-full p-4 border-b following hover:bg-lighter">
        <router-link :to="`/profile/${props.tweet.tweet_creator_id}`">
          <div class="flex-none mr-4">
            <img src="https://sogor98.eu.pythonanywhere.com/assets/img/default-profile-image.jpeg" class="flex-none w-12 h-12 rounded-full"/>
          </div>
        </router-link>
          <div class="w-full">
            <div class="flex items-center w-full">
              <p class="font-semibold"> {{ props.tweet.name }} </p>
              <p class="ml-2 text-sm text-dark"> {{ props.tweet.handle }} </p>
              <p class="ml-2 text-sm text-dark"> {{ props.tweet.time }} </p>
            </div>
          <p class="py-2">
            {{ props.tweet.tweet_content }}
          </p>
          <div class="flex items-center justify-between w-full">
            <div class="flex items-center text-sm text-dark">
              <i class="mr-3 fas fa-heart"></i>
              <p> {{ props.tweet.like }} </p>
            </div>
            <div v-if="props.isEditable" @click="handleEditTweet" class="flex items-center text-sm cursor-pointer text-dark">
              <i class="mr-3 fa-solid fa-pen"></i>
              <p> Edit </p>
            </div>
            <div v-if="props.isEditable" @click="handleDeleteTweet" class="flex items-center text-sm cursor-pointer text-dark">
              <i class="mr-3 fa-solid fa-trash"></i>
              <p> Remove </p>
            </div>
          </div>
        </div>
      </div>
</template>