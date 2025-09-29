<template>
  <div
    class="job-bar"
    :style="barStyle"
    :class="[
      job.type.toLowerCase().replace(' ', '-'),
      { paused: job.isPaused },
    ]"
    :title="tooltipText"
  >
    <!-- Убираем текст в общем режиме -->
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  job: Object,
  pixelsPerHour: Number,
  now: Date,
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
</style>
