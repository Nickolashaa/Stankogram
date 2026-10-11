<script setup lang="ts">
import { ref } from "vue"
import { useInfiniteScroll } from "@vueuse/core"

const props = defineProps<{
  title: string
  total?: number
  fill?: boolean
  canLoadMore?: boolean
  loadMore?: () => Promise<void>
}>()

const scrollContainer = ref<HTMLElement | null>(null)

const infiniteScroll = useInfiniteScroll(
  scrollContainer,
  async () => {
    await props.loadMore?.()
  },
  {
    distance: 200,
    canLoadMore: () => props.canLoadMore === true,
  },
)
</script>

<template>
  <div
    ref="scrollContainer"
    class="h-full min-h-0 px-4 py-6 lg:px-10 lg:py-10 xl:px-14"
    :class="fill ? 'overflow-hidden' : 'overflow-y-auto'"
  >
    <div class="flex animate-appear flex-col gap-6" :class="fill ? 'h-full min-h-0' : ''">
      <div
        class="flex shrink-0 flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="flex min-w-0 flex-col gap-0.5">
          <h1 class="m-0 text-2xl font-semibold tracking-tight text-main sm:text-3xl">
            {{ title }}
          </h1>
          <span v-if="total !== undefined" class="text-sm text-second">Всего: {{ total }}</span>
        </div>

        <div
          v-if="$slots.actions"
          class="flex w-full flex-col gap-2 sm:w-auto sm:flex-row sm:items-center"
        >
          <slot name="actions" />
        </div>
      </div>

      <div class="flex flex-col gap-4" :class="fill ? 'min-h-0 flex-1' : ''">
        <slot />
      </div>

      <Transition name="fade">
        <span
          v-if="infiniteScroll.isLoading.value"
          class="shrink-0 text-center text-sm text-second"
        >
          Загрузка...
        </span>
      </Transition>
    </div>
  </div>
</template>
