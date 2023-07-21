<template>
    <div class="gallery_container">
        <nav-bar></nav-bar>
        <select v-model="selected_folder">
            <option :value="ct" v-for="ct in content.folder_list" :key="ct">{{ ct }}</option>
        </select>
        <gallery-display></gallery-display>
    </div>
</template>

<script async setup>
import { ref, watch } from 'vue'
import NavBar from '../components/NavBar.vue';
import GalleryDisplay from '../components/GalleryDisplay.vue';
import {useContentStore} from '../stores/contents'
import { BACK_URL } from '../api/infrastructure'
import { fetch_data } from '../api/resources'

const selected_folder = ref('')
const content = useContentStore()

let folders = await fetch_data(`${BACK_URL}/flds`)
content.set_folders(folders.folders)

watch(selected_folder, async function() {
    let resources = await fetch_data(`${BACK_URL}/rs/${selected_folder.value}`)
    content.set_resources(selected_folder.value, resources.files)
})

</script>

<style>

.gallery_container {
    display: flex;
    flex-direction: column;
}
select {
    margin: 5px;
}
</style>