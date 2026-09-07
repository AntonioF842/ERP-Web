<template>
  <router-link 
    :to="to" 
    class="p-4 rounded-xl border border-slate-200 bg-white hover:border-blue-500 hover:shadow-sm transition-all flex items-center justify-between group"
  >
    <div class="flex items-center gap-3">
      <div class="p-2.5 bg-slate-100 rounded-lg text-slate-600 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
        <i :class="[icon, 'text-lg']"></i>
      </div>
      <div>
        <p class="font-semibold text-slate-800 text-sm group-hover:text-blue-600 transition-colors">{{ title }}</p>
        <p class="text-xs text-slate-500">{{ description }}</p>
      </div>
    </div>
    <i class="pi pi-chevron-right text-slate-400 text-sm group-hover:text-blue-600 group-hover:translate-x-1 transition-all"></i>
  </router-link>
</template>

<script setup>
defineProps({
  to: String,
  title: String,
  description: String,
  icon: String
});
</script>