<template>
    <div class="content">
        <img :src="content.selected_image" alt="Image" @keydown.left="content.back" @keydown.right="content.next">
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