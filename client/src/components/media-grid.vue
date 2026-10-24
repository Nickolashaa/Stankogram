<script setup lang="ts">
import { computed } from "vue"
import type { AttachmentFieldsFragment } from "@/graphql/fragments/messages.generated"
import { formatDuration } from "@/lib/media"
import { EAttachmentKind } from "@/graphql/base-types"
import NavIcon from "@/components/nav-icon.vue"

const SINGLE_MIN_RATIO = 0.6
const SINGLE_MAX_RATIO = 1.9

const props = defineProps<{ attachments: AttachmentFieldsFragment[] }>()

const emit = defineEmits<{ open: [index: number] }>()

const single = computed(() => (props.attachments.length === 1 ? props.attachments[0] : undefined))

const columns = computed(() => (props.attachments.length > 4 ? 3 : 2))

const singleRatio = computed(() => {
  const item = single.value
  if (item === undefined || item.width === null || item.height === null || item.height === 0) {
    return 1
  }
  return Math.min(Math.max(item.width / item.height, SINGLE_MIN_RATIO), SINGLE_MAX_RATIO)
})
</script>

<template>
  <div v-if="attachments.length > 0" class="mb-1.5 flex flex-col gap-1">
    <button
      v-if="single !== undefined"
      type="button"
      class="press relative w-full max-w-72 cursor-pointer overflow-hidden rounded-input bg-black/15"
      :style="{ aspectRatio: String(singleRatio) }"
      :aria-label="single.name"
      @click.stop="emit('open', 0)"
      @dblclick.stop
    >
      <img
        :src="single.thumbnailUrl ?? undefined"
        :alt="single.name"
        loading="lazy"
        decoding="async"
        class="h-full w-full object-cover"
      />
      <span
        v-if="single.kind === EAttachmentKind.Video"
        class="absolute inset-0 flex items-center justify-center"
      >
        <span
          class="flex h-12 w-12 items-center justify-center rounded-full bg-black/55 text-white backdrop-blur-sm"
        >
          <NavIcon name="play" :size="20" />
        </span>
      </span>
      <span
        v-if="single.kind === EAttachmentKind.Video && single.durationMs !== null"
        class="absolute right-1.5 bottom-1.5 rounded-full bg-black/60 px-1.5 py-0.5 text-[11px] font-medium text-white"
      >
        {{ formatDuration(single.durationMs) }}
      </span>
    </button>

    <div
      v-else
      class="grid w-full max-w-72 gap-1"
      :style="{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }"
    >
      <button
        v-for="(attachment, index) in attachments"
        :key="attachment.id"
        type="button"
        class="press relative aspect-square cursor-pointer overflow-hidden rounded-input bg-black/15"
        :aria-label="attachment.name"
        @click.stop="emit('open', index)"
        @dblclick.stop
      >
        <img
          :src="attachment.thumbnailUrl ?? undefined"
          :alt="attachment.name"
          loading="lazy"
          decoding="async"
          class="h-full w-full object-cover"
        />
        <span
          v-if="attachment.kind === EAttachmentKind.Video"
          class="absolute inset-0 flex items-center justify-center"
        >
          <span
            class="flex h-8 w-8 items-center justify-center rounded-full bg-black/55 text-white backdrop-blur-sm"
          >
            <NavIcon name="play" :size="14" />
          </span>
        </span>
        <span
          v-if="attachment.kind === EAttachmentKind.Video && attachment.durationMs !== null"
          class="absolute right-1 bottom-1 rounded-full bg-black/60 px-1.5 py-0.5 text-[10px] font-medium text-white"
        >
          {{ formatDuration(attachment.durationMs) }}
        </span>
      </button>
    </div>
  </div>
</template>
