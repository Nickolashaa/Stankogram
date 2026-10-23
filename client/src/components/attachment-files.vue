<script setup lang="ts">
import type { AttachmentFieldsFragment } from "@/graphql/fragments/messages.generated"
import { formatSize } from "@/lib/media"
import NavIcon from "@/components/nav-icon.vue"

defineProps<{ attachments: AttachmentFieldsFragment[] }>()
</script>

<template>
  <div v-if="attachments.length > 0" class="mb-1.5 flex flex-col gap-1">
    <a
      v-for="attachment in attachments"
      :key="attachment.id"
      :href="attachment.downloadUrl"
      target="_blank"
      rel="noopener"
      class="press flex w-full max-w-72 items-center gap-2.5 rounded-input bg-current/8 px-2.5 py-2 no-underline transition-opacity hover:opacity-80"
      :title="attachment.name"
      @click.stop
      @dblclick.stop
    >
      <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-current/12">
        <NavIcon name="file" :size="18" />
      </span>
      <span class="flex min-w-0 flex-col">
        <span class="truncate text-[13px] font-medium">{{ attachment.name }}</span>
        <span class="text-[11px] opacity-70">{{ formatSize(attachment.size) }}</span>
      </span>
      <NavIcon name="download" :size="16" class="ml-auto shrink-0 opacity-70" />
    </a>
  </div>
</template>
