import { ref, computed } from "vue";
import { fetchCharacters, fetchJobs } from "../api";

// --- State ---
const now = ref(new Date());
setInterval(() => {
  now.value = new Date();
}, 1000);

const characters = ref([]);
const jobs = ref([]);

const focusedCharacterId = ref(null);
const activeJobFilter = ref(null); // 'industry', 'research', 'reaction', 'planetary', или null
const isCharacterPanelCollapsed = ref(false);
const timelineScale = ref("week");

// --- Getters ---
const charactersWithJobs = computed(() => {
  return characters.value.map((char) => {
    return {
      ...char,
      jobs: jobs.value.filter((j) => j.characterId === char.id),
    };
  });
});

const jobsByCharacter = computed(() => {
  const grouped = {};
  jobs.value.forEach((job) => {
    if (
      focusedCharacterId.value &&
      job.characterId !== focusedCharacterId.value
    ) {
      return; // Skip jobs of unfocused characters if focus mode is on
    }
    if (!grouped[job.characterId]) {
      grouped[job.characterId] = { characterId: job.characterId, jobs: [] };
    }
    grouped[job.characterId].jobs.push(job);
  });
  return Object.values(grouped);
});

const charactersWithCompletedJobs = computed(() => {
  const charIds = new Set();
  jobs.value.forEach((job) => {
    if (new Date(job.endDate) < now.value) {
      charIds.add(job.characterId);
    }
  });
  return charIds;
});

const isFocused = computed(() => focusedCharacterId.value !== null);

// Геттер для фильтрации работ на таймлайне
const filteredJobsForTimeline = computed(() => {
  let filteredJobs = jobs.value;

  // Фильтр по персонажу (фокус)
  if (focusedCharacterId.value !== null) {
    filteredJobs = filteredJobs.filter(
      (job) => job.characterId === focusedCharacterId.value
    );
  }

  // Фильтр по типу работы
  if (activeJobFilter.value !== null) {
    filteredJobs = filteredJobs.filter(
      (job) => job.type === activeJobFilter.value
    );
  }

  return filteredJobs;
});

// --- Actions ---
const loadData = async () => {
  characters.value = await fetchCharacters();
  const rawJobs = await fetchJobs();
  // Dates are strings in JSON/from API, so convert them back to Date objects
  jobs.value = rawJobs.map((job) => ({
    ...job,
    startDate: new Date(job.startDate),
    endDate: new Date(job.endDate),
  }));
};

const setFocusCharacter = (characterId) => {
  if (focusedCharacterId.value === characterId) {
    focusedCharacterId.value = null; // Toggle off if same character is clicked
  } else {
    focusedCharacterId.value = characterId;
  }
};

const toggleCharacterPanelCollapse = () => {
  isCharacterPanelCollapsed.value = !isCharacterPanelCollapsed.value;
};

const setTimelineScale = (scale) => {
  timelineScale.value = scale;
};

const setActiveJobFilter = (jobType) => {
  if (activeJobFilter.value === jobType) {
    activeJobFilter.value = null; // Сброс фильтра при повторном клике
  } else {
    activeJobFilter.value = jobType;
  }
};

// --- Main export ---
export function useStore() {
  // Load data when the store is first used
  if (characters.value.length === 0) {
    loadData();
  }

  return {
    now,
    characters,
    charactersWithJobs,
    jobs, // Добавляем экспорт jobs
    jobsByCharacter,
    charactersWithCompletedJobs,
    isFocused,
    setFocusCharacter,
    focusedCharacterId,
    activeJobFilter,
    setActiveJobFilter,
    filteredJobsForTimeline,
    isCharacterPanelCollapsed,
    toggleCharacterPanelCollapse,
    timelineScale,
    setTimelineScale,
  };
}
