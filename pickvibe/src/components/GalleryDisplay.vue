<template>
    <div class="content">
        <img v-if="content.selected_is_image" :src="content.selected_image" @keydown.left="content.back" @keydown.right="content.next">
        <video v-else-if="content.selected_is_video" :key="content.selected_image" controls width="400">
            <source :src="content.selected_image">
        </video>
        <div v-else>cant show this</div>
    </div>
</template>

<script async setup>
import {useContentStore} from '../stores/contents'

const content = useContentStore()

</script>

<style scoped>
/* Style for the content area */
.content {
    text-align: center;
}
img {
    width: 90%;
}
</style>