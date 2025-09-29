<template>
  <div class="timeline-container" :class="{ 'focus-mode': isFocused }">
    <div class="timeline-body" ref="timelineBodyRef">
      <div class="timeline-grid">
        <div class="time-marks">
          <div
            v-for="mark in timeMarks"
            :key="mark.time"
            class="time-mark"
            :style="{ left: mark.position + 'px' }"
          >
            <span class="time-label">{{ mark.label }}</span>
          </div>
        </div>
        <div class="now-line"></div>
        <div class="character-job-lanes">
          <div
            v-for="character in charactersWithJobs"
            :key="character.id"
            class="job-lane"
            :class="{
              'is-focused': isFocused && character.id === focusedCharacterId,
              'is-unfocused': isFocused && character.id !== focusedCharacterId,
            }"
          >
            <div class="job-bars-container">
              <JobBar
                v-for="job in getJobsForCharacter(character.id)"
                :key="job.id"
                :job="job"
                :pixels-per-hour="pixelsPerHour"
                :now="now"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import JobBar from "./JobBar.vue";
import { useStore } from "../store";

const {
  now,
  jobs,
  isFocused,
  focusedCharacterId,
  characters,
  charactersWithJobs,
  timelineScale,
  activeJobFilter,
  filteredJobsForTimeline,
} = useStore();

const timelineBodyRef = ref(null);
const scale = timelineScale;

// Функция для получения работ конкретного персонажа
const getJobsForCharacter = (characterId) => {
  // Используем отфильтрованные работы из store
  return filteredJobsForTimeline.value.filter(
    (job) => job.characterId === characterId
  );
};

// Pixels Per Hour calculation
const pixelsPerHour = computed(() => {
  if (!timelineBodyRef.value) return 20;
  const timelineWidth = timelineBodyRef.value.clientWidth;
  switch (scale.value) {
    case "day":
      return timelineWidth / 24;
    case "week":
      return timelineWidth / (24 * 7);
    case "month":
      return timelineWidth / (24 * 30);
    default:
      return 20;
  }
});

// Time marks for the timeline
const timeMarks = computed(() => {
  if (!timelineBodyRef.value) return [];

  const timelineWidth = timelineBodyRef.value.clientWidth;
  const marks = [];
  const now = new Date();

  switch (scale.value) {
    case "day":
      for (let i = 0; i < 24; i += 2) {
        marks.push({
          time: i,
          position: i * pixelsPerHour.value,
          label: `${i.toString().padStart(2, "0")}:00`,
        });
      }
      break;
    case "week":
      for (let i = 0; i < 7; i++) {
        const date = new Date(now.getTime() - (6 - i) * 24 * 60 * 60 * 1000);
        marks.push({
          time: i,
          position: i * pixelsPerHour.value * 24,
          label: date.toLocaleDateString("en-US", { weekday: "short" }),
        });
      }
      break;
    case "month":
      for (let i = 0; i < 30; i += 5) {
        const date = new Date(now.getTime() - (29 - i) * 24 * 60 * 60 * 1000);
        marks.push({
          time: i,
          position: i * pixelsPerHour.value * 24,
          label: date.toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
          }),
        });
      }
      break;
  }

  return marks;
});
</script>

<style scoped>
.timeline-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: #222831;
  color: #dfd0b8;
  height: 100%;
  overflow: hidden;
}

.timeline-body {
  position: relative;
  flex-grow: 1;
  /* Убираем внутренний скролл - теперь скролл общий */
}

.timeline-grid {
  position: relative;
  min-width: 100%;
  min-height: 100%;
}

.time-marks {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  height: 30px;
  background-color: rgba(57, 62, 70, 0.8);
  border-bottom: 1px solid #dfd0b8;
  z-index: 3;
  transform: translateY(30px);
}

.time-mark {
  position: absolute;
  top: 0;
  height: 100%;
  border-left: 1px solid rgba(223, 208, 184, 0.3);
  display: flex;
  align-items: center;
  padding-left: 5px;
}

.time-label {
  font-size: 11px;
  color: #dfd0b8;
  opacity: 0.7;
}

.now-line {
  position: absolute;
  top: 30px;
  bottom: 0;
  left: 0; /* Прикрепляем к левому краю */
  width: 2px;
  background-color: #f39f9f;
  z-index: 5;
  box-shadow: 0 0 4px rgba(243, 159, 159, 0.5);
}

.character-job-lanes {
  position: relative;
  padding-top: 10px;
  margin-top: 30px;
  min-height: 100%; /* Занимаем всю доступную высоту для синхронизации */
  /* Убираем transform, чтобы не мешать скроллу */
}

.job-lane {
  position: relative;
  height: 121px; /* Базовая высота для 10px job-bar */
  margin-bottom: 10px; /* Совпадает с margin-bottom character-card */
  display: flex;
  align-items: center;
  transition: height 0.4s ease, opacity 0.4s ease;
  border-bottom: 1px solid rgba(223, 208, 184, 0.1);
}

.job-lane.is-unfocused {
  height: 0;
  margin-bottom: 0;
  overflow: hidden;
  opacity: 0;
}

.job-lane.is-focused {
  height: 100vh;
  opacity: 1;
  border-left: 3px solid #e1aa36;
  background-color: rgba(225, 170, 54, 0.05);
}

.job-lane.is-focused .job-bar {
  height: 30px;
}

.job-lane:not(.is-focused) .job-bar {
  height: 10px;
}

.job-bars-container {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 1;
}
</style>
