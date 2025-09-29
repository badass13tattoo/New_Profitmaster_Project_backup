<template>
  <div class="timeline-header">
    <div class="header-bottom-row">
      <div class="job-stats">
        <span
          class="stat-item"
          :class="{
            active: activeJobFilter === 'industry',
            'sort-indicator': activeJobFilter === 'industry',
          }"
          title="Industry Jobs - Click to sort by type"
          @click="setActiveJobFilter('industry')"
        >
          <span class="stat-icon">🏭</span>
          <span class="stat-value"
            >{{ jobStats.industry.active }}/{{ jobStats.industry.total }}</span
          >
        </span>
        <span
          class="stat-item"
          :class="{
            active: activeJobFilter === 'research',
            'sort-indicator': activeJobFilter === 'research',
          }"
          title="Research Jobs - Click to sort by type"
          @click="setActiveJobFilter('research')"
        >
          <span class="stat-icon">🔬</span>
          <span class="stat-value"
            >{{ jobStats.research.active }}/{{ jobStats.research.total }}</span
          >
        </span>
        <span
          class="stat-item"
          :class="{
            active: activeJobFilter === 'reaction',
            'sort-indicator': activeJobFilter === 'reaction',
          }"
          title="Reaction Jobs - Click to sort by type"
          @click="setActiveJobFilter('reaction')"
        >
          <span class="stat-icon">⚗️</span>
          <span class="stat-value"
            >{{ jobStats.reaction.active }}/{{ jobStats.reaction.total }}</span
          >
        </span>
        <span
          class="stat-item"
          :class="{
            active: activeJobFilter === 'planetary',
            'sort-indicator': activeJobFilter === 'planetary',
          }"
          title="Planetary Jobs - Click to sort by type"
          @click="setActiveJobFilter('planetary')"
        >
          <span class="stat-icon">🌍</span>
          <span class="stat-value"
            >{{ jobStats.planetary.active }}/{{
              jobStats.planetary.total
            }}</span
          >
        </span>
      </div>

      <div class="zoom-controls">
        <button @click="setScale('day')" :class="{ active: scale === 'day' }">
          Day
        </button>
        <button @click="setScale('week')" :class="{ active: scale === 'week' }">
          Week
        </button>
        <button
          @click="setScale('month')"
          :class="{ active: scale === 'month' }"
        >
          Month
        </button>
      </div>
    </div>

    <h2 class="header-title">Job Timeline</h2>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "../store";

const {
  jobsByCharacter,
  timelineScale,
  setTimelineScale,
  activeJobFilter,
  setActiveJobFilter,
} = useStore();

const scale = timelineScale;
const setScale = setTimelineScale;

// Job statistics
const jobStats = computed(() => {
  const stats = {
    industry: { active: 0, total: 0 },
    research: { active: 0, total: 0 },
    reaction: { active: 0, total: 0 },
    planetary: { active: 0, total: 0 },
  };

  jobsByCharacter.value.forEach((charJobs) => {
    charJobs.jobs.forEach((job) => {
      if (stats[job.type]) {
        stats[job.type].total++;
        if (job.status === "active") {
          stats[job.type].active++;
        }
      }
    });
  });

  return stats;
});
</script>

<style scoped>
.timeline-header {
  padding: 15px;
  border-bottom: 1px solid #dfd0b8;
  position: sticky;
  top: 0;
  background-color: #222831;
  z-index: 10;

  /* Делаем header контейнером Flex */
  display: flex;
  flex-direction: column; /* На широком экране: название сверху, контент снизу */
  gap: 10px; /* Отступ между названием и нижней строкой */
}
.header-title {
  margin: 0;
  color: #dfd0b8;
  font-size: 20px;
  /* Устанавливаем порядок 1, чтобы оно всегда было первым */
  order: 1;
}
.header-bottom-row {
  display: flex;
  justify-content: space-between; /* Распределение элементов по краям */
  align-items: center;
  flex-wrap: wrap; /* Разрешаем перенос на мобильных */
  order: 2; /* Располагается под названием */
}

.header-left h2 {
  margin: 0 0 10px 0;
  color: #dfd0b8;
  font-size: 20px;
}

.job-stats {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: rgba(148, 137, 121, 0.1);
  padding: 5px 8px; /* Уменьшен padding для компактности */
  border-radius: 6px;
  border: 1px solid rgba(223, 208, 184, 0.2);
  cursor: pointer; /* Курсор указателя для кликабельности */
  position: relative;
  transition: all 0.2s ease;
}

.stat-item:hover {
  background-color: rgba(148, 137, 121, 0.2);
  border-color: rgba(223, 208, 184, 0.4);
}

.stat-item.active {
  background-color: rgba(225, 170, 54, 0.2);
  border-color: #e1aa36;
  color: #e1aa36;
}

.stat-item.sort-indicator {
  position: relative;
}

.stat-icon {
  font-size: 16px;
}

.stat-value {
  font-size: 14px;
  font-weight: bold;
  color: #e1aa36;
}

.zoom-controls {
  display: flex;
  gap: 5px;
  margin-left: auto;
}

.zoom-controls button {
  background-color: #948979;
  color: #dfd0b8;
  border: 1px solid #dfd0b8;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zoom-controls button:hover {
  background-color: #a89f8f;
}

.zoom-controls button.active {
  background-color: #e1aa36;
  color: #222831;
  font-weight: bold;
}
/* ----------------------------------------------------------------- */
/* Стили для узкого экрана (Mobile) */
/* ----------------------------------------------------------------- */
@media (max-width: 768px) {
  .timeline-header {
    flex-direction: column; /* По-прежнему колонка, но с измененным порядком */
  }

  /* Верхняя строка на мобильном: Название и Зум */
  .header-title {
    /* Сбрасываем порядок, чтобы работать с блоком */
    order: unset;
    margin-bottom: 10px;
  }

  /* Элементы управления зумом поднимаем рядом с названием */
  .zoom-controls {
    order: 1; /* Перемещаем зум наверх */
    margin-left: 0;
  }

  /* Нижняя строка на мобильном: Только Статистика */
  .header-bottom-row {
    flex-direction: column; /* Переводим в колонку */
    align-items: flex-start; /* Выравнивание по левому краю */
    order: 2; /* Статистика идет под названием и зумом */
  }

  /* На мобильном экране, статистика занимает всю ширину */
  .job-stats {
    width: 100%;
    margin-bottom: 10px; /* Добавляем отступ после статистики */
  }

  /* На узком экране, название и зум должны быть на одной строке */
  .header-title {
    /* Создаем контейнер для первой строки (Название + Зум) */
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    /* Для того, чтобы зум встал рядом с названием, 
         мы объединяем их в один flex-контейнер, 
         а job-stats делаем отдельной строкой. */
  }

  /* Переопределение структуры для мобильного: 
     Мы вернем зум в header-title, чтобы они были в одной строке, 
     а job-stats оставим внизу. */
  /* НОВЫЙ ПОДХОД ДЛЯ МОБИЛЬНОГО (БОЛЕЕ ЧИСТЫЙ): */
  /* Вся структура должна быть переопределена как колонка: */
  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-title {
    display: flex; /* Делаем название и зум в одной строке */
    justify-content: space-between;
    width: 100%;
    margin-bottom: 5px;
  }

  .header-bottom-row {
    width: 100%;
    order: 3; /* Сдвигаем вниз */
  }

  /* Переносим zoom-controls в header-title для мобильного */
  /* Так как в HTML это сложно, вернемся к Flexbox order: */

  .zoom-controls {
    /* Чтобы зум встал на одну строку с заголовком: */
    position: absolute; /* Временное позиционирование для мобильной версии */
    top: 15px;
    right: 15px;
    margin-left: 0;
  }

  .header-title {
    /* Дадим заголовку место, чтобы он не перекрывал зум */
    padding-right: 150px; /* Примерно на ширину зум-контролов */
  }
}

/* ... (Остальные стили job-stats и zoom-controls без изменений) */
</style>
