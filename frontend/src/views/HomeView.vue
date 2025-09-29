<template>
  <div class="home">
    <h1>EVE Profitmaster</h1>
    <p>
      Добро пожаловать в приложение для отслеживания производства EVE Online
    </p>
  </div>
</template>

<script>
export default {
  name: "HomeView",
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
