<template>
  <div
    class="job-bar"
    :style="barStyle"
    :class="[
      job.type.toLowerCase().replace(' ', '-'),
      { paused: job.isPaused },
      { 'focused-mode': isFocusedMode },
    ]"
    :title="tooltipText"
  >
    <!-- Показываем информацию в режиме фокуса -->
    <div v-if="isFocusedMode && shouldShowText" class="job-info">
      <span class="job-name">{{ job.name }}</span>
      <span class="job-runs">{{ job.runs || 1 }} runs</span>
      <span class="job-countdown">{{ countdown }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  job: Object,
  pixelsPerHour: Number,
  now: Date,
  isFocusedMode: {
    type: Boolean,
    default: false,
  },
});

const barStyle = computed(() => {
  const start = new Date(props.job.startDate);
  const end = new Date(props.job.endDate);
  const now = props.now;

  // Если работа завершена, скрываем полосу
  if (end <= now) {
    return {
      display: "none",
    };
  }

  // Если работа еще не началась, показываем полную полосу
  if (start > now) {
    const durationMs = end - start;
    const width = (durationMs / (1000 * 60 * 60)) * props.pixelsPerHour;
    return {
      width: `${width}px`,
    };
  }

  // Работа в процессе - показываем оставшееся время
  const remainingMs = end - now;
  const width = (remainingMs / (1000 * 60 * 60)) * props.pixelsPerHour;

  return {
    width: `${Math.max(0, width)}px`,
  };
});

const countdown = computed(() => {
  const endDate = new Date(props.job.endDate);
  const diff = endDate - props.now;

  if (diff <= 0) {
    return "Complete";
  }

  const d = Math.floor(diff / (1000 * 60 * 60 * 24));
  const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const s = Math.floor((diff % (1000 * 60)) / 1000);

  return `${d}d ${h}h ${m}m ${s}s`;
});

const tooltipText = computed(() => {
  const startTime = new Date(props.job.startDate).toLocaleString();
  const endTime = new Date(props.job.endDate).toLocaleString();

  return `${props.job.name}
Location: ${props.job.location || "Unknown"}
Blueprint: ${props.job.blueprint || "N/A"}
Runs: ${props.job.runs || 1}
Progress: ${props.job.progress || 0}%
Time Left: ${countdown.value}
Type: ${props.job.type.toUpperCase()}
Status: ${props.job.status.toUpperCase()}`.trim();
});

// Определяем, нужно ли показывать текст на основе ширины job-bar
const shouldShowText = computed(() => {
  if (!props.isFocusedMode) return false;

  const start = new Date(props.job.startDate);
  const end = new Date(props.job.endDate);
  const now = props.now;

  // Если работа завершена, не показываем текст
  if (end <= now) {
    return false;
  }

  // Если работа еще не началась, показываем текст
  if (start > now) {
    return true;
  }

  // Вычисляем ширину job-bar в пикселях
  const remainingMs = end - now;
  const widthPx = (remainingMs / (1000 * 60 * 60)) * props.pixelsPerHour;

  // Показываем текст только если ширина больше 60px
  return widthPx > 60;
});
</script>

<style scoped>
.job-bar {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  box-sizing: border-box;
  flex-shrink: 0;
}

.industry {
  background-color: #e1aa36;
}
.reaction {
  background-color: #7adaa5;
}
.research {
  background-color: #239ba7;
}
.planetary {
  background-color: #ececbb;
}

.job-bar.paused {
  background-image: repeating-linear-gradient(
    45deg,
    #888888,
    #888888 10px,
    #999999 10px,
    #999999 20px
  );
}

/* Стили для режима фокуса */
.job-bar.focused-mode {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 4px 8px;
  overflow: hidden;
  min-height: 30px; /* Минимальная высота для режима фокуса */
  gap: 8px;
}

.job-info {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  overflow: hidden;
  height: 100%;
  justify-content: flex-start;
}

.job-name {
  font-size: 12px;
  font-weight: bold;

  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
  min-width: 0;
}

.job-runs {
  font-weight: 600;

  color: #ffffff;
  white-space: nowrap;
  font-size: 12px;
  flex-shrink: 0;
}

.job-countdown {
  font-weight: 600;

  white-space: nowrap;
  font-size: 12px;
  flex-shrink: 0;
  margin-left: auto;
}

/* Дополнительные стили для лучшего отображения текста */
.job-bar.focused-mode {
  position: relative;
}
</style>
