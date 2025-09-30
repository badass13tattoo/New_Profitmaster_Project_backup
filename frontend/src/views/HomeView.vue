<template>
  <div class="home">
    <h1>EVE Profitmaster</h1>
    <p>
      Добро пожаловать в приложение для отслеживания производства EVE Online
    </p>

    <div class="characters-section">
      <h2>Ваши персонажи</h2>
      <ul v-if="characters.length > 0" class="character-list">
        <li v-for="char in characters" :key="char.char_id">
          {{ char.name }}
        </li>
      </ul>
      <p v-else>У вас пока нет добавленных персонажей.</p>

      <a href="http://localhost:5000/sso/login">
        <button class="add-char-button">Добавить персонажа</button>
      </a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "HomeView",
  data() {
    return {
      characters: [],
    };
  },
  created() {
    this.fetchCharacters();
  },
  methods: {
    async fetchCharacters() {
      try {
        const response = await axios.get('http://localhost:5000/characters');
        this.characters = response.data.characters;
      } catch (error) {
        console.error("Ошибка при загрузке персонажей:", error);
      }
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

.home h1 {
  color: #141316;
  margin-bottom: 10px;
  font-size: 2.5rem;
  font-weight: 700;
}

.home p {
  color: #7f8c8d;
  font-size: 1.2rem;
  line-height: 1.6;
}
</style>
