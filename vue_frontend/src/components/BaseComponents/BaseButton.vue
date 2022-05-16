<template>
    <button
        type="submit"
        class="relative px-6 py-2 rounded-full"
        :class="{
            'text-white bg-blue font-semibold focus:outline-none hover:bg-darkblue': props.type == 'primary',
            'text-sm text-blue  border-2 border-blue': props.type == 'secondary',
            loading: props.isLoading,
        }"
        :disabled="props.isLoading"
        v-bind="$attrs"
        v-on="$listeners"
    >
        <BaseSpinner v-if="props.isLoading" />
        <slot v-else></slot>
    </button>
</template>

<script setup>
const props = defineProps({
    type: {
        type: String,
        default: "primary"
    },
    isLoading: {
        type: Boolean,
        default: false
    }
})
</script>