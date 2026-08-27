<script setup lang="ts">
import type { DayPeriod } from "@/lib/greeting"

defineProps<{
  period: DayPeriod
}>()
</script>

<template>
  <svg
    v-if="period === 'night'"
    viewBox="0 0 100 100"
    class="h-full w-full text-accent"
    fill="currentColor"
  >
    <mask id="moon-mask">
      <rect width="100" height="100" fill="white" />
      <circle cx="61" cy="41" r="23" fill="black" />
    </mask>
    <circle cx="48" cy="50" r="27" fill="currentColor" mask="url(#moon-mask)" />
    <circle class="star star-1" cx="18" cy="26" r="2.2" />
    <circle class="star star-2" cx="82" cy="32" r="1.6" />
    <circle class="star star-3" cx="78" cy="72" r="2" />
    <circle class="star star-4" cx="16" cy="74" r="1.4" />
  </svg>

  <svg v-else-if="period === 'evening'" viewBox="0 0 100 100" class="h-full w-full text-accent">
    <defs>
      <clipPath id="sunset-clip">
        <rect x="0" y="0" width="100" height="60" />
      </clipPath>
    </defs>
    <g clip-path="url(#sunset-clip)">
      <g
        class="sunset-rays"
        fill="none"
        stroke="currentColor"
        stroke-width="4"
        stroke-linecap="round"
      >
        <line x1="50" y1="6" x2="50" y2="17" />
        <line x1="19" y1="19" x2="27" y2="27" />
        <line x1="81" y1="19" x2="73" y2="27" />
        <line x1="6" y1="52" x2="17" y2="52" />
        <line x1="94" y1="52" x2="83" y2="52" />
      </g>
      <circle class="sunset-sun" cx="50" cy="56" r="21" fill="currentColor" />
    </g>
    <line
      x1="10"
      y1="60"
      x2="90"
      y2="60"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
      opacity="0.45"
    />
  </svg>

  <svg v-else viewBox="0 0 100 100" class="h-full w-full text-accent">
    <g class="sun-rays" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round">
      <line x1="50" y1="6" x2="50" y2="17" />
      <line x1="50" y1="83" x2="50" y2="94" />
      <line x1="6" y1="50" x2="17" y2="50" />
      <line x1="83" y1="50" x2="94" y2="50" />
      <line x1="19" y1="19" x2="27" y2="27" />
      <line x1="73" y1="73" x2="81" y2="81" />
      <line x1="19" y1="81" x2="27" y2="73" />
      <line x1="73" y1="27" x2="81" y2="19" />
    </g>
    <circle cx="50" cy="50" r="21" fill="currentColor" />
  </svg>
</template>

<style scoped>
.sun-rays {
  transform-box: view-box;
  transform-origin: 50% 50%;
  animation: spin 26s linear infinite;
}

.sunset-rays {
  transform-box: view-box;
  transform-origin: 50% 50%;
  animation: pulse-opacity 3s ease-in-out infinite;
}

.sunset-sun {
  transform-box: view-box;
  transform-origin: 50% 50%;
  animation: float 4s ease-in-out infinite;
}

.star {
  transform-box: fill-box;
  transform-origin: 50% 50%;
  animation: twinkle 2.4s ease-in-out infinite;
}

.star-2 {
  animation-delay: 0.5s;
}

.star-3 {
  animation-delay: 1s;
}

.star-4 {
  animation-delay: 1.6s;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@keyframes pulse-opacity {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.45;
  }
}

@keyframes twinkle {
  0%,
  100% {
    opacity: 0.35;
    transform: scale(0.85);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .sun-rays,
  .sunset-rays,
  .sunset-sun,
  .star {
    animation: none;
  }
}
</style>
