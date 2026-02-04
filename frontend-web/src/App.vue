<script setup lang="ts">
import { NConfigProvider, NMessageProvider, NDialogProvider, NLoadingBarProvider, darkTheme } from 'naive-ui'
import { RouterView } from 'vue-router'

const themeOverrides = {
  common: {
    primaryColor: '#0ea5e9',
    primaryColorHover: '#38bdf8',
    primaryColorPressed: '#0284c7',
    primaryColorSuppl: '#0ea5e9',
  }
}
</script>

<template>
  <NConfigProvider :theme="darkTheme" :theme-overrides="themeOverrides">
    <NLoadingBarProvider>
      <NDialogProvider>
        <NMessageProvider>
          <RouterView />
        </NMessageProvider>
      </NDialogProvider>
    </NLoadingBarProvider>
  </NConfigProvider>
</template>

<style>
#app {
  min-height: 100vh;
}
</style>
