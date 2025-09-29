<template>
  <div class="Login">
    <h1>Отслеживание производства EVE Online</h1>
    <p>Войдите, чтобы начать отслеживать ваши производственные работы.</p>
    <!-- <a href="http://localhost:5000/login">
      <button>Войти через EVE</button>
    </a> -->
    <button @click="goToMainApp">Войти через EVE</button>
  </div>
</template>

<script>
export default {
  name: "LoginView",
  methods: {
    goToMainApp() {
      // Пропускаем авторизацию и переходим на главную страницу
      this.$router.push("/home");
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
