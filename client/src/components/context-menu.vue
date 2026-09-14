<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref, watch } from "vue"

const props = defineProps<{
  x: number
  y: number
}>()

const emit = defineEmits<{
  close: []
}>()

defineOptions({ inheritAttrs: false })

const VIEWPORT_GAP = 8

const menuEl = ref<HTMLElement | null>(null)
const left = ref(props.x)
const top = ref(props.y)

function place() {
  const element = menuEl.value
  if (element === null) {
    return
  }
  left.value = Math.max(
    VIEWPORT_GAP,
    Math.min(props.x, window.innerWidth - element.offsetWidth - VIEWPORT_GAP),
  )
  top.value = Math.max(
    VIEWPORT_GAP,
    Math.min(props.y, window.innerHeight - element.offsetHeight - VIEWPORT_GAP),
  )
}

watch(
  () => [props.x, props.y],
  async () => {
    left.value = props.x
    top.value = props.y
    await nextTick()
    place()
  },
)

function handleEscape(event: KeyboardEvent) {
  if (event.key === "Escape") {
    emit("close")
  }
}

onMounted(async () => {
  window.addEventListener("keydown", handleEscape)
  window.addEventListener("resize", place)
  await nextTick()
  place()
})

onUnmounted(() => {
  window.removeEventListener("keydown", handleEscape)
  window.removeEventListener("resize", place)
})
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-40" @click="emit('close')" @contextmenu.prevent="emit('close')" />

    <div
      ref="menuEl"
      class="glass-strong hairline shadow-float fixed z-50 flex origin-top-left animate-pop flex-col gap-0.5 overflow-hidden rounded-card p-1.5"
      :style="{ top: `${top}px`, left: `${left}px` }"
      v-bind="$attrs"
    >
      <slot />
    </div>
  </Teleport>
</template>
