<script setup lang="ts">
import { Icon } from '@iconify/vue'

defineProps({
  icon: String
})
</script>

<template>
  <button v-if="icon">
    <slot>Button</slot>
    <Icon :icon="icon" class="icon" />
  </button>
  <button v-else>
    <slot>Button</slot>
  </button>
</template>

<style lang="scss" scoped>
button {
  padding: 10px 15px;
  border: 1px solid #fff;
  background: #00a650;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;

  .icon {
    font-size: 1.2em;
  }
}
</style>
