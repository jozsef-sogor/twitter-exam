<script setup>
const props = defineProps({
    friendSuggestion: {
        type: Object,
        required: true
    }
})

</script>

<template>
    <div class="flex w-full p-3 border-t hover:bg-lighter border-lighter">
        <img :src="`${ props.friendSuggestion.src }`" class="w-12 h-12 border rounded-full border-lighter" />
        <div class="ml-4">
            <p class="text-sm font-bold leading-tight"> {{ props.friendSuggestion.name }} </p>
            <p class="text-sm leading-tight"> {{ props.friendSuggestion.handle }} </p>
        </div>
        <!--
        <button class="px-4 py-1 ml-auto text-sm border-2 rounded-full text-blue border-blue">
            Follow
        </button>
        -->
        <BaseButton class="ml-auto" type="secondary">Follow</BaseButton>
	</div>
</template>