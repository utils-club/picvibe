<template>
    <div class="content">
        <div v-if="content.selected_is_image">
            <img :src="content.selected_image" @keydown.left="content.back" @keydown.right="content.next">
        </div>
        <div v-else-if="content.selected_is_video">
            <div>{{ vid_title(content.selected_image) }}</div>
            <video :key="content.selected_image" controls width="400" poster preload="metadata">
                <source :src="content.selected_image" :type="vid_type(content.selected_image)">
            </video>
        </div>
        <div v-else>cant show this</div>
    </div>
</template>

<script async setup>
import {useContentStore} from '../stores/contents'

const content = useContentStore()

function vid_type(link) {
    let items = link.split('.')
    let termination = items[items.length - 1]
    return `video/${termination}`
}

function vid_title(link) {
    let items = link.split('/')
    let vid_name = items[items.length - 1]
    return vid_name
}

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