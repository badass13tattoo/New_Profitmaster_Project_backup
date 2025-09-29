<template>
  <div class="character-panel" :class="{ collapsed: isCollapsed }">
    <div class="panel-header">
      <div class="header-left">
        <span class="header-icon">👥</span>
        <button v-if="!isCollapsed" class="add-char-btn">
          + Add Character
        </button>
      </div>
      <button @click="toggleCollapse" class="collapse-btn">
        {{ isCollapsed ? "»" : "«" }}
      </button>
    </div>
    <div class="character-list">
      <CharacterCard
        v-for="character in charactersWithJobs"
        :key="character.id"
        :character="character"
        :is-collapsed="isCollapsed"
        :has-completed-jobs="charactersWithCompletedJobs.has(character.id)"
        :is-focused="focusedCharacterId === character.id"
        @click="setFocusCharacter(character.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CharacterCard from "./CharacterCard.vue";
import { useStore } from "../store";

const {
  charactersWithJobs,
  charactersWithCompletedJobs,
  setFocusCharacter,
  isCharacterPanelCollapsed,
  toggleCharacterPanelCollapse,
  focusedCharacterId,
} = useStore();

const isCollapsed = isCharacterPanelCollapsed;
const toggleCollapse = toggleCharacterPanelCollapse;
</script>

<style scoped>
.character-panel {
  background-color: #393e46;
  padding: 10px;
  max-height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 300px;
  transition: width 0.3s ease;
}

.character-panel.collapsed {
  width: 100px;
}

.character-list {
  /* Убираем внутренний скролл - теперь скролл общий */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}

.character-list::-webkit-scrollbar {
  display: none; /* WebKit */
}

.character-panel.collapsed .character-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  position: relative;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.collapse-btn {
  background-color: #948979;
  color: #dfd0b8;
  border: 1px solid #dfd0b8;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  right: 8px;
  bottom: 0px;
  z-index: 10;
  font-size: 16px;
}

.character-panel.collapsed .panel-header {
  justify-content: space-between;
}

.character-panel.collapsed .collapse-btn {
  position: absolute;
  right: 8px;
  bottom: 0px;
  margin-bottom: 0;
}

.header-icon {
  font-size: 24px;
}

.add-char-btn {
  background-color: #948979;
  color: #dfd0b8;
  border: 1px solid #dfd0b8;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>
