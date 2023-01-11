<script setup>
import { reactive } from "vue";
import { FormKit, FormKitSchema } from "@formkit/vue";
import { getFormDataFromObject } from "../../helpers";
import { loginSchema } from "../../formik-schemas";
import { useRouter } from "vue-router";
import sha256 from "crypto-js/sha256";
import hmacSHA512 from "crypto-js/hmac-sha512";
import Base64 from "crypto-js/enc-base64";

const emit = defineEmits(["close", "submit-form"]);
const handleCloseModal = () => {
  emit("close");
};

const props = defineProps({
  isLoading: {
    type: Boolean,
    deafult: false,
  },
});

//Password hashing feature
let formData = reactive({});
const handleSubmit = (form) => {
  console.log(form);
  const hashDigest = sha256(form.password);
  const hmacDigest = hashDigest.toString();
  console.log(hmacDigest);
  console.log({ user_password: hmacDigest, user_email: form.user_email });
  let formData = getFormDataFromObject({
    user_password: hmacDigest,
    user_email: form.user_email,
  });
  emit("submit-form", formData);
};

const route = useRouter();
const handleForgotPassword = () => {
  route.push({ hash: "#ForgotPasswordModal" });
};
</script>

<template>
  <BaseModal :isLoading="isLoading" @close-modal="handleCloseModal">
    <FormKit type="form" v-model="formData" @submit="handleSubmit">
      <FormKitSchema :schema="loginSchema" />
    </FormKit>
    <p
      class="pt-2 text-xs underline cursor-pointer"
      @click="handleForgotPassword"
    >
      Forgot password?
    </p>
  </BaseModal>
</template>
