<script setup>
import { reactive } from "vue"
import { FormKit, FormKitSchema } from "@formkit/vue"
import { getFormDataFromObject } from "../../helpers"
import { forgotPasswordSchema } from "../../formik-schemas"

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
</script>

<template>
    <BaseModal :isLoading="props.isLoading" @close-modal="handleCloseModal">
        <FormKit 
            type="form"
            v-model="formData"
            @submit="handleSubmit"
        >
            <FormKitSchema :schema="forgotPasswordSchema" />
        </FormKit>
    </BaseModal>
</template>