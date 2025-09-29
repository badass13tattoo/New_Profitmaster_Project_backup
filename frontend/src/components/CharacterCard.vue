<template>
  <div
    class="character-card"
    :class="{ collapsed: isCollapsed }"
    :title="isCollapsed ? character.name : ''"
  >
    <div class="card-content">
      <div class="left-section">
        <div class="portrait-container">
          <img
            :src="character.portrait"
            :alt="character.name"
            class="portrait"
          />
          <div v-if="hasCompletedJobs" class="completed-indicator">✓</div>
        </div>
      </div>

      <div v-if="!isCollapsed" class="right-section">
        <div class="character-name">
          {{ character.name }}
        </div>

        <div class="job-indicators">
          <div class="indicator">
            <span class="indicator-icon">🏭</span>
            <span class="indicator-value"
              >{{ character.industryJobs.active }}/{{
                character.industryJobs.total
              }}</span
            >
          </div>
          <div class="indicator">
            <span class="indicator-icon">🔬</span>
            <span class="indicator-value"
              >{{ character.researchJobs.active }}/{{
                character.researchJobs.total
              }}</span
            >
          </div>
          <div class="indicator">
            <span class="indicator-icon">⚗️</span>
            <span class="indicator-value"
              >{{ character.reactionJobs.active }}/{{
                character.reactionJobs.total
              }}</span
            >
          </div>
          <div class="indicator">
            <span class="indicator-icon">🌍</span>
            <span class="indicator-value"
              >{{ character.planetaryJobs.active }}/{{
                character.planetaryJobs.total
              }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  character: Object,
  isCollapsed: Boolean,
  hasCompletedJobs: Boolean,
});
</script>

<style scoped>
/* ЦВЕТА: бэкграунд - #393E46, текст/бордер - #DFD0B8, кнопки - #948979 */
.character-card {
  /* Устанавливаем базовые переменные для развернутого состояния */
  --portrait-size: 90px;
  --card-height: 90px; /* Фиксируем высоту для ровных отступов */

  display: flex;
  background-color: #393e46; /* цвет карточек персонажей [cite: 6] */
  border: 1px solid #dfd0b8; /* цвет текста и бордерлайнов  */
  border-radius: 8px; /* Скругленные углы  */
  padding: 15px;
  margin-bottom: 10px;
  color: #dfd0b8;
  transition: all 0.3s ease;
  cursor: pointer;
  height: var(--card-height); /* Используем переменную */
  width: 245px;
  position: relative;
}

.character-card.collapsed {
  /* Изменяем переменные для свернутого состояния */
  --portrait-size: 60px;
  --card-height: 60px;
  width: 60px;
  height: var(--card-height);
  padding: 5px;
  justify-content: center;
  align-items: center;
}

.card-content {
  display: flex;
  width: 100%;
  height: 100%; /* Устанавливаем 100% для заполнения высоты карточки (var(--card-height)) */
  align-items: flex-start;
  gap: 15px;
  position: relative; /* Для позиционирования кнопки удаления */
}

.left-section {
  /* Секция Портрета */
  flex-shrink: 0;
}

.portrait-container {
  position: relative;
  /* Используем переменную для динамического размера */
  width: var(--portrait-size);
  height: var(--portrait-size);
}

.portrait {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  object-fit: cover;
}

.right-section {
  /* Секция Имени и Индикаторов */
  display: flex;
  flex-direction: column;
  justify-content: flex-end; /* Прижимаем контент к низу */
  flex-grow: 1;
  /* Высота правой секции также должна зависеть от размера портрета */
  height: var(--portrait-size);
  min-width: 0; /* Важно для работы text-overflow: ellipsis */
}

.character-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 9px;
  text-align: left; /* Имя выровнено влево */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* Обрезание длинного имени */
}

/* ----------------------------------------------------------------- */
/* Индикатор завершенных работ (желтый мигающий квадратик с галочкой) [cite: 27] */
.completed-indicator {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  background-color: #e1aa36; /* Цвет Manufacturing, использован как яркий [cite: 26] */
  border-radius: 6px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  font-weight: 900;
  animation: flash 1.5s infinite;
}

@keyframes flash {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* ----------------------------------------------------------------- */
/* Блок Индикаторов Работ */
.job-indicators {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  width: 100%;
}

.indicator {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: rgba(223, 208, 184, 0.1);
  border-radius: 4px;
  padding: 2px 4px;
  border: 1px solid rgba(223, 208, 184, 0.2);
  gap: 3px;
  height: 20px;
}

.indicator-icon {
  font-size: 12px;
  flex-shrink: 0;
}

.indicator-value {
  font-size: 14px;
  font-weight: bold;
  color: #e1aa36; /* Использован яркий цвет */
}
</style>
