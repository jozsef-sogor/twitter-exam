<template>
    <div class="flex justify-center w-full p-3 bg-lightest">
        <BaseSpinner :isDark="true" />
    </div>
</template>

<script setup>
const props = defineProps({
    isDark: {
        type: Boolean,
        default: false
    }
})
</script>
