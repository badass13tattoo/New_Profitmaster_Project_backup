<template>
  <div id="app-container">
    <div class="headers-container">
      <div class="top-info-panel" :style="{ width: topInfoPanelWidth }">
        <div class="info-content">
          <span class="info-text"
            >Characters: {{ charactersWithJobs.length }}</span
          >
          <span class="info-text">Active Jobs: {{ totalActiveJobs }}</span>
        </div>
      </div>
      <div class="timeline-header-container">
        <TimelineHeader />
      </div>
    </div>
    <div class="panels-container">
      <CharacterPanel />
      <Timeline />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import CharacterPanel from "./components/CharacterPanel.vue";
import Timeline from "./components/Timeline.vue";
import TimelineHeader from "./components/TimelineHeader.vue";
import { useStore } from "./store";

const { charactersWithJobs, isCharacterPanelCollapsed } = useStore();

// Подсчет общего количества активных работ
const totalActiveJobs = computed(() => {
  return charactersWithJobs.value.reduce((total, character) => {
    return (
      total +
      character.industryJobs.active +
      character.researchJobs.active +
      character.reactionJobs.active +
      character.planetaryJobs.active
    );
  }, 0);
});

// Ширина top-info-panel в зависимости от состояния сворачивания CharacterPanel
const topInfoPanelWidth = computed(() => {
  return isCharacterPanelCollapsed.value ? "100px" : "300px";
});
</script>

<style>
#app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-info-panel {
  height: 30px;
  background-color: rgba(148, 137, 121, 0.1);
  border-bottom: 1px solid rgba(223, 208, 184, 0.2);
  display: flex;
  align-items: center;
  padding: 0 0px;
  flex-shrink: 0;
  transition: width 0.3s ease; /* Плавная анимация изменения ширины */
}

.info-content {
  display: flex;
  gap: 20px;
  width: 100%;
}

.info-text {
  font-size: 12px;
  color: #dfd0b8;
  opacity: 0.8;
}

.headers-container {
  display: flex;
  height: 60px; /* Высота заголовков */
  flex-shrink: 0;
}

.timeline-header-container {
  flex: 1;
  background-color: #222831;
}

.panels-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}
</style>
