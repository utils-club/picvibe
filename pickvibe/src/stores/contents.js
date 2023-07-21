import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useContentStore = defineStore('content', () => {
  const resource_list = ref([])
  const folder_list = ref([])
  const selected_folder = ref('')
  const selected_img_indx = ref(0)

  const selected_image = computed(()=>{
    return selected_folder.value ? `http://localhost:9090/rp/${selected_folder.value}/${resource_list.value[selected_img_indx.value]}`:''
  })

  function next() {
    if (selected_img_indx.value < resource_list.value.length - 1) {
      selected_img_indx.value += 1
    } else {
      selected_img_indx.value = 1
    }
    
  }

  function back() {
    if (selected_img_indx.value == 0) {
      selected_img_indx.value = resource_list.value.length - 1
    } else {
      selected_img_indx.value -= 1
    }
  }

  function set_resources(folder , _resources) {
    console.log({_resources, folder});
    resource_list.value = _resources
    selected_img_indx.value = 0
    selected_folder.value = folder
  }
  
  function set_folders(_folders) {
    folder_list.value = _folders
  }


  return { resource_list, folder_list, set_resources, set_folders, selected_folder, selected_image, next, back, selected_img_indx }
})
