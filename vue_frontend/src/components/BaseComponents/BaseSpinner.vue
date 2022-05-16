<template>
    <div style="border-top-color:transparent"
        class="w-8 h-8 border-2 border-solid rounded-full animate-spin"
        :class="isDark ? 'border-darkblue' : 'border-lightblue'">
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
