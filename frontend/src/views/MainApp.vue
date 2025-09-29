<template>
  <div class="main-app">
    <header class="app-header">
      <h1>EVE Profitmaster</h1>
      <p>Основная страница приложения</p>
    </header>

    <main class="app-content">
      <div class="placeholder">
        <h2>Здесь будет основное содержимое приложения</h2>
        <p>Пока что страница пустая, но готова для разработки</p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "MainApp",
  mounted() {
    console.log("Основная страница приложения загружена");
  },
};
</script>

<style scoped>
.main-app {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 2rem;
  text-align: center;
}

.app-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

.app-header p {
  margin: 0;
  font-size: 1.2rem;
  opacity: 0.9;
}

.app-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.placeholder {
  background: white;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.placeholder h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.placeholder p {
  color: #7f8c8d;
  font-size: 1.1rem;
}
</style>
