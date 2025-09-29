<template>
  <div class="timeline-container" :class="{ 'focus-mode': isFocused }">
    <div class="timeline-header">
      <div class="zoom-controls">
        <button @click="setScale('day')">Day</button>
        <button @click="setScale('week')">Week</button>
        <button @click="setScale('month')">Month</button>
      </div>
    </div>
    <div class="timeline-body" ref="timelineBodyRef">
      <div class="now-line"></div>
      <div class="character-job-lanes">
        <div
          v-for="charJobs in jobsByCharacter"
          :key="charJobs.characterId"
          class="job-lane"
          :class="{ 'is-focused': isFocused && charJobs.characterId === focusedCharacterId, 'is-unfocused': isFocused && charJobs.characterId !== focusedCharacterId }"
        >
          <JobBar
            v-for="job in charJobs.jobs"
            :key="job.id"
            :job="job"
            :pixels-per-hour="pixelsPerHour"
            :now="now"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import JobBar from './JobBar.vue';
import { useStore } from '../store';

const { now, jobsByCharacter, isFocused, focusedCharacterId } = useStore();

const scale = ref('week'); // day, week, month
const timelineBodyRef = ref(null);

const setScale = (newScale) => {
  scale.value = newScale;
};

// Pixels Per Hour calculation
const pixelsPerHour = computed(() => {
  if (!timelineBodyRef.value) return 20;
  const timelineWidth = timelineBodyRef.value.clientWidth;
  switch (scale.value) {
    case 'day':
      return timelineWidth / 24;
    case 'week':
      return timelineWidth / (24 * 7);
    case 'month':
      return timelineWidth / (24 * 30);
    default:
      return 20;
  }
});



</script>

<style scoped>
.timeline-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: #222831;
  color: #DFD0B8;
  height: 100%;
  overflow: hidden;
}

.timeline-header {
  padding: 10px;
  border-bottom: 1px solid #DFD0B8;
  position: sticky;
  top: 0;
  background-color: #222831;
  z-index: 10;
}

.zoom-controls button {
  background-color: #948979;
  color: #DFD0B8;
  border: 1px solid #DFD0B8;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  margin-right: 10px;
}

.timeline-body {
  position: relative;
  flex-grow: 1;
  overflow-x: auto;
}

.now-line {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #F39F9F;
  z-index: 5;
}

.character-job-lanes {
    position: relative;
    padding-top: 20px;
}

.job-lane {
    position: relative;
    height: 50px; /* Height for each character's job lane */
    margin-bottom: 10px;
    transition: height 0.4s ease, opacity 0.4s ease;
}

.timeline-container.focus-mode .job-lane.is-unfocused {
    height: 5px;
    opacity: 0.5;
}

.timeline-container.focus-mode .job-lane.is-focused {
    height: 120px; /* Expanded height for focused character */
}

/* Hide job bars in unfocused lanes when in focus mode */
.timeline-container.focus-mode .job-lane.is-unfocused .job-bar {
    display: none;
}
</style>