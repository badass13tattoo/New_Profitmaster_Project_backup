<template>
  <div id="app-container">
    <CharacterPanel />
    <Timeline />
  </div>
</template>

<script setup>
import CharacterPanel from './components/CharacterPanel.vue';
import Timeline from './components/Timeline.vue';
</script>

<style>
#app-container {
  display: flex;
  height: 100vh;
}
</style>