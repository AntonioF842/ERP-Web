<template>
  <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
    <div class="space-y-1">
      <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">{{ title }}</p>
      <h3 class="text-2xl font-bold text-slate-800">{{ value }}</h3>
      <p v-if="subtitle" class="text-xs text-slate-400">{{ subtitle }}</p>
    </div>
    <div :class="['p-3 rounded-xl flex items-center justify-center', colorClass]">
      <i :class="[icon, 'text-xl']"></i>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  icon: String,
  colorClass: {
    type: String,
    default: 'bg-blue-50 text-blue-600'
  }
});
</script>