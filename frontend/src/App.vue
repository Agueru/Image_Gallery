<script setup>
import ButtonsBar from './components/ButtonsBarComponent.vue';
import { RouterView } from 'vue-router'
import { useStore } from 'vuex';
import { onMounted } from 'vue';


const store = useStore();

onMounted(() => {
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');
  if (token && user) {
    store.commit('setUserLoggedIn', JSON.parse(user));
  }
});
</script>

<template>
  <ButtonsBar />
  <div class="content-container">
    <RouterView />
  </div>
</template>

<style scoped>
.content-container {
  margin-top: 50px;
}

</style>