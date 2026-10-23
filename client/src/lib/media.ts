import { EAttachmentKind } from "@/graphql/base-types"

export const IMAGE_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
export const VIDEO_CONTENT_TYPES = ["video/mp4", "video/webm", "video/quicktime"]

export const ATTACHMENT_ACCEPT = [...IMAGE_CONTENT_TYPES, ...VIDEO_CONTENT_TYPES].join(",")

export const MAX_IMAGE_SIZE = 20 * 1024 * 1024
export const MAX_VIDEO_SIZE = 100 * 1024 * 1024

const THUMBNAIL_MAX_SIDE = 480
const THUMBNAIL_QUALITY = 0.72
const VIDEO_READY_TIMEOUT = 15000

export type ProbedMedia = {
  kind: EAttachmentKind
  width: number
  height: number
  durationMs: number | null
  thumbnail: Blob
}

export function attachmentKind(contentType: string): EAttachmentKind | null {
  if (IMAGE_CONTENT_TYPES.includes(contentType)) {
    return EAttachmentKind.Image
  }
  if (VIDEO_CONTENT_TYPES.includes(contentType)) {
    return EAttachmentKind.Video
  }
  return null
}

export function maxSize(kind: EAttachmentKind): number {
  return kind === EAttachmentKind.Image ? MAX_IMAGE_SIZE : MAX_VIDEO_SIZE
}

export function formatSize(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} Б`
  }
  if (bytes < 1024 * 1024) {
    return `${Math.round(bytes / 1024)} КБ`
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} МБ`
}

export function formatDuration(durationMs: number): string {
  const total = Math.round(durationMs / 1000)
  const minutes = Math.floor(total / 60)
  const seconds = total % 60
  return `${minutes}:${String(seconds).padStart(2, "0")}`
}

function thumbnailSize(width: number, height: number): { width: number; height: number } {
  const side = Math.max(width, height)
  if (side <= THUMBNAIL_MAX_SIDE) {
    return { width, height }
  }
  const ratio = THUMBNAIL_MAX_SIDE / side
  return { width: Math.round(width * ratio), height: Math.round(height * ratio) }
}

async function toThumbnail(
  source: CanvasImageSource,
  width: number,
  height: number,
): Promise<Blob> {
  const size = thumbnailSize(width, height)
  const canvas = document.createElement("canvas")
  canvas.width = size.width
  canvas.height = size.height

  const context = canvas.getContext("2d")
  if (context === null) {
    throw new Error("Не удалось подготовить превью")
  }
  context.drawImage(source, 0, 0, size.width, size.height)

  return await new Promise<Blob>((resolve, reject) => {
    canvas.toBlob(
      (blob) =>
        blob === null ? reject(new Error("Не удалось подготовить превью")) : resolve(blob),
      "image/jpeg",
      THUMBNAIL_QUALITY,
    )
  })
}

async function probeImage(file: File): Promise<ProbedMedia> {
  const bitmap = await createImageBitmap(file)
  try {
    return {
      kind: EAttachmentKind.Image,
      width: bitmap.width,
      height: bitmap.height,
      durationMs: null,
      thumbnail: await toThumbnail(bitmap, bitmap.width, bitmap.height),
    }
  } finally {
    bitmap.close()
  }
}

function waitForVideo(video: HTMLVideoElement, event: "loadeddata" | "seeked"): Promise<void> {
  return new Promise((resolve, reject) => {
    const timeout = window.setTimeout(() => {
      cleanup()
      reject(new Error("Не удалось прочитать видео"))
    }, VIDEO_READY_TIMEOUT)

    function cleanup() {
      window.clearTimeout(timeout)
      video.removeEventListener(event, onDone)
      video.removeEventListener("error", onError)
    }

    function onDone() {
      cleanup()
      resolve()
    }

    function onError() {
      cleanup()
      reject(new Error("Не удалось прочитать видео"))
    }

    video.addEventListener(event, onDone, { once: true })
    video.addEventListener("error", onError, { once: true })
  })
}

async function probeVideo(file: File): Promise<ProbedMedia> {
  const source = URL.createObjectURL(file)
  const video = document.createElement("video")
  video.muted = true
  video.playsInline = true
  video.preload = "auto"
  video.src = source

  try {
    await waitForVideo(video, "loadeddata")

    const duration = Number.isFinite(video.duration) ? video.duration : 0
    video.currentTime = Math.min(0.2, duration / 2)
    await waitForVideo(video, "seeked")

    return {
      kind: EAttachmentKind.Video,
      width: video.videoWidth,
      height: video.videoHeight,
      durationMs: duration > 0 ? Math.round(duration * 1000) : null,
      thumbnail: await toThumbnail(video, video.videoWidth, video.videoHeight),
    }
  } finally {
    video.removeAttribute("src")
    video.load()
    URL.revokeObjectURL(source)
  }
}

export async function probeMedia(file: File): Promise<ProbedMedia> {
  const kind = attachmentKind(file.type)

  if (kind === null) {
    throw new Error("Можно отправлять только фото и видео")
  }

  if (file.size > maxSize(kind)) {
    throw new Error(`Файл больше ${formatSize(maxSize(kind))}`)
  }

  return kind === EAttachmentKind.Image ? await probeImage(file) : await probeVideo(file)
}

export function attachmentsLabel(attachments: { kind: EAttachmentKind }[]): string {
  if (attachments.length === 0) {
    return ""
  }

  if (attachments.length > 1) {
    return `Вложения (${attachments.length})`
  }

  return attachments[0]!.kind === EAttachmentKind.Image ? "Фото" : "Видео"
}

export function messagePreview(message: {
  text: string
  attachments: { kind: EAttachmentKind }[]
}): string {
  return message.text !== "" ? message.text : attachmentsLabel(message.attachments)
}
