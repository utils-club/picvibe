<script setup>
import { RouterView } from 'vue-router'

</script>

<template>
  <Suspense>
    <RouterView />
    
    <template #fallback>
      loading...
    </template>
  </Suspense>
</template>
