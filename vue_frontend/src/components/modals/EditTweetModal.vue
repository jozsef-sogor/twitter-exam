<script setup>
import { reactive } from "vue"
import { FormKit, FormKitSchema } from "@formkit/vue"
import { getFormDataFromObject } from "../../helpers"
import { editTweetSchema } from "../../formik-schemas"


const emit = defineEmits(["close", "edit-tweet"])
const props = defineProps({
    tweet: {
        type: Object,
        required: true
    },
    isLoading: {
        type: Boolean,
        deafult: false
    }
})

const handleCloseModal = () => {
    emit("close")
}

let formData = reactive(props.tweet)
const handleSubmit = (form) => {
    let formData = getFormDataFromObject(form)
    emit('edit-tweet', formData)
}
</script>

<template>
    <BaseModal :isLoading="props.isLoading" @close-modal="handleCloseModal">
        <FormKit 
            type="form"
            v-model="formData"
            @submit="handleSubmit"
        >
            <FormKitSchema :schema="editTweetSchema" />
        </FormKit>
    </BaseModal>
</template>