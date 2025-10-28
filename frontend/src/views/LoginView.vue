<template>
  <div class="Login">
    <h1>Отслеживание производства EVE Online</h1>
    <p>Войдите, чтобы начать отслеживать ваши производственные работы.</p>
    <a href="http://localhost:5000/sso/login">
      <button>Войти через EVE</button>
    </a>
  </div>
</template>

<script>
export default {
  name: "LoginView",
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
