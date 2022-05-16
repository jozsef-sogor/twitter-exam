<template>
  <Transition name="fade">
    <div
      class="fixed inset-0 flex items-center justify-center w-full h-screen bg-dark/60"
      @click.self="close"
    >
      <div class="relative w-full max-w-2xl p-8 overflow-y-auto bg-white rounded-lg shadow-lg max-h-96">
        <BaseSpinnerOverlay v-if="isLoading" />
        <button
          aria-label="close"
          class="absolute top-0 right-0 mx-4 my-2 text-x"
          @click.prevent="close"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>
        <slot />
      </div>
    </div>
  </Transition>
</template>
 
<script setup>
const emit = defineEmits(['close-modal'])
const props = defineProps({
    isLoading: {
        type: Boolean,
        deafult: false
    }
})

const close = () => {
    emit('close-modal')
}
</script>
 
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>