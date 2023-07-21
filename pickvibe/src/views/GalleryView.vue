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

const selected_folder = ref('')
const content = useContentStore()

const api_url = 'http://localhost:9090'

async function fetch_data(api_url) {
  try {
    const response = await fetch(api_url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.log("Error fetching data: ", error);
  }
}

let folders = await fetch_data(`${api_url}/flds`)

content.set_folders(folders.folders)

watch(selected_folder, async function() {
    let resources = await fetch_data(`${api_url}/rs/${selected_folder.value}`)
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