<template>
  <div
    class="job-bar"
    :style="barStyle"
    :class="[job.type.toLowerCase().replace(' ', '-'), { paused: job.isPaused }]"
    :title="tooltipText"
  >
    <div class="job-bar-content">
      <span class="job-name">{{ job.name }}</span>
      <span class="job-countdown">{{ countdown }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  job: Object,
  pixelsPerHour: Number,
  now: Date,
});

const barStyle = computed(() => {
  const start = new Date(props.job.startDate);
  const end = new Date(props.job.endDate);
  const durationMs = end - start;

  const offsetMs = start - props.now;
  const left = (offsetMs / (1000 * 60 * 60)) * props.pixelsPerHour;
  const width = (durationMs / (1000 * 60 * 60)) * props.pixelsPerHour;

  return {
    transform: `translateX(${left}px)`,
    width: `${width}px`,
  };
});

const countdown = computed(() => {
    const endDate = new Date(props.job.endDate);
    const diff = endDate - props.now;

    if (diff <= 0) {
        return 'Complete';
    }

    const d = Math.floor(diff / (1000 * 60 * 60 * 24));
    const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((diff % (1000 * 60)) / 1000);

    return `${d}d ${h}h ${m}m ${s}s`;
});


const tooltipText = computed(() => {
  return `Item: ${props.job.name}
Location: ${props.job.location}
Time Left: ${countdown.value}
Type: ${props.job.type}
  `.trim();
});

</script>

<style scoped>
.job-bar {
  position: absolute;
  height: 30px;
  border-radius: 8px;
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  padding: 0 10px;
  color: #222831;
  font-weight: bold;
  white-space: nowrap;
}

.job-bar-content {
    display: flex;
    justify-content: space-between;
    width: 100%;
    align-items: center;
}

.manufacturing { background-color: #E1AA36; }
.reaction { background-color: #7ADAA5; }
.research { background-color: #239BA7; }
.planet-extraction { background-color: #ECECBB; }


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