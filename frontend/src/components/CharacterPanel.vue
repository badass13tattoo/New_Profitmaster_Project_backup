<template>
  <div class="character-panel" :class="{ collapsed: isCollapsed }">
    <div class="panel-header">
      <span v-if="!isCollapsed" class="header-icon">👥</span>
      <button v-if="!isCollapsed" class="add-char-btn">+ Add Character</button>
      <button @click="toggleCollapse" class="collapse-btn">
        {{ isCollapsed ? '»' : '«' }}
      </button>
    </div>
    <div class="character-list">
      <CharacterCard
        v-for="character in charactersWithJobs"
        :key="character.id"
        :character="character"
        :is-collapsed="isCollapsed"
        :has-completed-jobs="charactersWithCompletedJobs.has(character.id)"
        @click="setFocusCharacter(character.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CharacterCard from './CharacterCard.vue';
import { useStore } from '../store';

const { charactersWithJobs, charactersWithCompletedJobs, setFocusCharacter } = useStore();

const isCollapsed = ref(false);
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};
</script>

<style scoped>
.character-panel {
  background-color: #393E46;
  padding: 10px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 300px;
  transition: width 0.3s ease;
}

.character-panel.collapsed {
  width: 80px;
}

.character-list {
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  position: relative;
}

.collapse-btn {
    background-color: #948979;
    color: #DFD0B8;
    border: 1px solid #DFD0B8;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: -22px;
    top: 10px;
    z-index: 10;
}

.character-panel.collapsed .panel-header {
    justify-content: center;
}

.character-panel.collapsed .collapse-btn {
    position: static;
    margin-bottom: 10px;
}

.header-icon {
  font-size: 24px;
}

.add-char-btn {
  background-color: #948979;
  color: #DFD0B8;
  border: 1px solid #DFD0B8;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>