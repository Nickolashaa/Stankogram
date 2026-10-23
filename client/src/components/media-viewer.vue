<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue"
import type { AttachmentFieldsFragment } from "@/graphql/fragments/messages.generated"
import { formatSize } from "@/lib/media"
import { EAttachmentKind } from "@/graphql/base-types"
import NavIcon from "@/components/nav-icon.vue"

const props = defineProps<{
  attachments: AttachmentFieldsFragment[]
  index: number
}>()

const emit = defineEmits<{ close: [] }>()

const activeIndex = ref(props.index)

watch(
  () => props.index,
  (value) => {
    activeIndex.value = value
  },
)

const current = computed(() => props.attachments[activeIndex.value])

const hasMany = computed(() => props.attachments.length > 1)

function step(offset: number) {
  const count = props.attachments.length
  activeIndex.value = (activeIndex.value + offset + count) % count
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === "Escape") {
    emit("close")
    return
  }
  if (!hasMany.value) {
    return
  }
  if (event.key === "ArrowRight") {
    step(1)
  }
  if (event.key === "ArrowLeft") {
    step(-1)
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeydown)
})
</script>

<template>
  <Teleport to="body">
    <div
      v-if="current !== undefined"
      class="fixed inset-0 z-60 flex animate-appear flex-col bg-black/85 backdrop-blur-sm"
      @click.self="emit('close')"
    >
      <div class="flex shrink-0 items-center gap-3 px-4 py-3 text-white">
        <div class="flex min-w-0 flex-1 flex-col">
          <span class="truncate text-sm font-medium">{{ current.name }}</span>
          <span class="text-xs text-white/60">
            {{ formatSize(current.size) }}
            <template v-if="hasMany">
              · {{ activeIndex + 1 }} из {{ attachments.length }}
            </template>
          </span>
        </div>

        <a
          :href="current.downloadUrl"
          target="_blank"
          rel="noopener"
          class="press flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-white/80 hover:bg-white/15 hover:text-white"
          title="Скачать"
          aria-label="Скачать"
          @click.stop
        >
          <NavIcon name="download" :size="18" />
        </a>

        <button
          type="button"
          class="press flex h-9 w-9 shrink-0 cursor-pointer items-center justify-center rounded-full text-white/80 hover:bg-white/15 hover:text-white"
          title="Закрыть"
          aria-label="Закрыть"
          @click="emit('close')"
        >
          <NavIcon name="cancel" :size="18" />
        </button>
      </div>

      <div
        class="relative flex min-h-0 flex-1 items-center justify-center p-3"
        @click.self="emit('close')"
      >
        <button
          v-if="hasMany"
          type="button"
          class="press absolute left-2 z-10 flex h-11 w-11 cursor-pointer items-center justify-center rounded-full bg-black/40 text-white/80 hover:bg-black/60 hover:text-white"
          title="Предыдущее"
          aria-label="Предыдущее"
          @click.stop="step(-1)"
        >
          <NavIcon name="arrow-right" :size="20" class="rotate-180" />
        </button>

        <img
          v-if="current.kind === EAttachmentKind.Image"
          :key="current.id"
          :src="current.url"
          :alt="current.name"
          class="max-h-full max-w-full animate-pop rounded-card object-contain"
        />
        <video
          v-else
          :key="current.id"
          :src="current.url"
          :poster="current.thumbnailUrl ?? undefined"
          controls
          autoplay
          playsinline
          class="max-h-full max-w-full animate-pop rounded-card"
        />

        <button
          v-if="hasMany"
          type="button"
          class="press absolute right-2 z-10 flex h-11 w-11 cursor-pointer items-center justify-center rounded-full bg-black/40 text-white/80 hover:bg-black/60 hover:text-white"
          title="Следующее"
          aria-label="Следующее"
          @click.stop="step(1)"
        >
          <NavIcon name="arrow-right" :size="20" />
        </button>
      </div>
    </div>
  </Teleport>
</template>
