<template>
  <div class="character-card" :class="{ collapsed: isCollapsed }" :title="isCollapsed ? character.name : ''">
    <div class="portrait-container">
      <img :src="character.portrait" :alt="character.name" class="portrait">
      <div v-if="hasCompletedJobs" class="completed-indicator">✓</div>
    </div>
    <div v-if="!isCollapsed" class="character-info">
      <span class="character-name">{{ character.name }}</span>
      <span class="job-info">Jobs: {{ character.jobs.length }}</span>
    </div>
    <button v-if="!isCollapsed" class="delete-btn">
      <div class="delete-icon">×</div>
    </button>
  </div>
</template>

<script setup>
defineProps({
  character: Object,
  isCollapsed: Boolean,
  hasCompletedJobs: Boolean,
});
</script>

<style scoped>
.character-card {
  display: flex;
  align-items: center;
  background-color: #393E46;
  border: 1px solid #DFD0B8;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 10px;
  color: #DFD0B8;
  transition: all 0.3s ease;
  overflow: hidden;
  cursor: pointer;
}

.character-card.collapsed {
  justify-content: center;
  padding: 5px;
}

.character-card.collapsed .portrait-container {
  margin-right: 0;
}

.portrait-container {
    position: relative;
    width: 50px;
    height: 50px;
    margin-right: 15px;
}

.portrait {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.completed-indicator {
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 18px;
    height: 18px;
    background-color: #E1AA36; /* Yellow */
    border-radius: 4px;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    font-weight: bold;
    animation: flash 1.5s infinite;
}

@keyframes flash {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.character-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.character-name {
  font-weight: bold;
}

.job-info {
  font-size: 0.9em;
}

.delete-btn {
  background-color: transparent;
  border: 1px solid #DFD0B8;
  color: #DFD0B8;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete-icon {
  font-size: 20px;
  line-height: 1;
}
</style>