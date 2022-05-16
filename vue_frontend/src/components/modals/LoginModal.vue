<script setup>
import { reactive } from "vue"
import { FormKit, FormKitSchema } from "@formkit/vue"
import { getFormDataFromObject } from "../../helpers"
import { loginSchema } from "../../formik-schemas"
import { useRouter } from "vue-router"

const emit = defineEmits(["close", "submit-form"])
const handleCloseModal = () => {
    emit("close")
}

const props = defineProps({
    isLoading: {
        type: Boolean,
        deafult: false
    }
})

let formData = reactive({})
const handleSubmit = (form) => {
    let formData = getFormDataFromObject(form)
    emit('submit-form', formData)
}

const route = useRouter()
const handleForgotPassword = () => {
    route.push({hash: "#ForgotPasswordModal"})
}
</script>

<template>
    <BaseModal :isLoading="isLoading" @close-modal="handleCloseModal">
        <FormKit 
            type="form"
            v-model="formData"
            @submit="handleSubmit"
        >
            <FormKitSchema :schema="loginSchema" />
        </FormKit>
        <p class="pt-2 text-xs underline cursor-pointer" @click="handleForgotPassword">Forgot password?</p>
    </BaseModal>
</template>