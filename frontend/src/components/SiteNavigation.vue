<script setup>
import { RouterLink } from 'vue-router'
import Button from './TheButton.vue'
</script>

<template>
  <nav>
    <div class="logo">BenQual</div>
    <RouterLink to="/analyze">
      <Button>Analyze data</Button>
    </RouterLink>
  </nav>
</template>

<style lang="scss" scoped>
nav {
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #201c70;
  color: #fff;

  a {
    text-decoration: none;
  }

  .logo {
    font-family: 'Paytone One', sans-serif;
    font-size: 2em;
  }
}
</style>
