<template>
    <div class="navbar">
        <button class="lf" @click="content.back">Back</button>
        <button class="rg" @click="content.next">Next</button>
    </div>
</template>

<script async setup>
import {useContentStore} from '../stores/contents'

const content = useContentStore()

</script>

<style scoped>
/* Style for the navigation bar */
.navbar {
    display: flex;
    flex-direction: row;
    margin-bottom: 10px;
}
button {
    flex-grow: 1;
    margin: 3px;
    padding: 15px 10px;
}
</style>