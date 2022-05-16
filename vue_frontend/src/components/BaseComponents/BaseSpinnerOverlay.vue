<template>
  <div class="absolute z-50 flex items-center justify-center w-full h-full -mt-8 -ml-8 bg-dark/50">
    <BaseSpinner />
  </div>
</template>

<script setup>
const props = defineProps({
    isLoading: {
        type: Boolean,
        deafult: false
    }
})
</script>
