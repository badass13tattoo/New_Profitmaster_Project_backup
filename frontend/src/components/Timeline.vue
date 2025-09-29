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
                :is-focused-mode="
                  isFocused && character.id === focusedCharacterId
                "
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
  const jobs = filteredJobsForTimeline.value.filter(
    (job) => job.characterId === characterId
  );

  // Сортируем по типу работ, если активен фильтр
  if (activeJobFilter.value) {
    return jobs.sort((a, b) => {
      // Сначала показываем работы выбранного типа
      if (a.type === activeJobFilter.value && b.type !== activeJobFilter.value)
        return -1;
      if (a.type !== activeJobFilter.value && b.type === activeJobFilter.value)
        return 1;

      // Затем сортируем по оставшемуся времени (сначала те, что заканчиваются раньше)
      const aRemaining = new Date(a.endDate) - now.value;
      const bRemaining = new Date(b.endDate) - now.value;
      return aRemaining - bRemaining;
    });
  }

  // Если фильтр не активен, сортируем только по оставшемуся времени
  return jobs.sort((a, b) => {
    const aRemaining = new Date(a.endDate) - now.value;
    const bRemaining = new Date(b.endDate) - now.value;
    return aRemaining - bRemaining;
  });
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
  background-color: #222831;
  border-bottom: 1px 1pxsolid #dfd0b8;
  z-index: 3;
  transform: translateY(30px);
}

.time-mark {
  position: absolute;
  top: 0;
  height: 100%;
  border-left: 1px solid #dfd0b84d;
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
  width: 4px;
  background-color: #f39f9f;
  z-index: 5;
  box-shadow: 0 0 4px #f39f9f80;
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
  background-color: #171b22;
  display: flex;
  align-items: flex-start;
  transition: height 0.4s ease, opacity 0.4s ease;
  border-bottom: 1px solid #dfd0b833;
  overflow-y: auto;
  overflow-x: hidden;
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
  background-color: #e1aa360d;
  overflow-y: auto;
  overflow-x: hidden;
}

.job-lane.is-focused .job-bar {
  height: 30px;
}

.job-lane:not(.is-focused) .job-bar {
  height: 10px;
}

.job-bars-container {
  position: relative;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 2px 0;
}

/* Стили для скроллбара */
.job-lane::-webkit-scrollbar {
  width: 6px;
}

.job-lane::-webkit-scrollbar-track {
  background: #dfd0b81a;
  border-radius: 3px;
}

.job-lane::-webkit-scrollbar-thumb {
  background: #dfd0b84d;
  border-radius: 3px;
}

.job-lane::-webkit-scrollbar-thumb:hover {
  background: #dfd0b880;
}

/* Firefox */
.job-lane {
  scrollbar-width: thin;
  scrollbar-color: #dfd0b84d #dfd0b81a;
}
</style>
