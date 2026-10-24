import { EAttachmentKind } from "@/graphql/base-types"

export const IMAGE_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
export const VIDEO_CONTENT_TYPES = ["video/mp4", "video/webm", "video/quicktime"]

const EXTENSION_CONTENT_TYPES: Record<string, string> = {
  pdf: "application/pdf",
  doc: "application/msword",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  xls: "application/vnd.ms-excel",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ppt: "application/vnd.ms-powerpoint",
  pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  odt: "application/vnd.oasis.opendocument.text",
  ods: "application/vnd.oasis.opendocument.spreadsheet",
  odp: "application/vnd.oasis.opendocument.presentation",
  rtf: "application/rtf",
  zip: "application/zip",
  "7z": "application/x-7z-compressed",
  rar: "application/vnd.rar",
  txt: "text/plain",
  csv: "text/csv",
}

export const FILE_CONTENT_TYPES = Object.values(EXTENSION_CONTENT_TYPES)

export const MEDIA_ACCEPT = [...IMAGE_CONTENT_TYPES, ...VIDEO_CONTENT_TYPES].join(",")

export const FILE_ACCEPT = [
  ...FILE_CONTENT_TYPES,
  ...Object.keys(EXTENSION_CONTENT_TYPES).map((extension) => `.${extension}`),
].join(",")

export const MAX_IMAGE_SIZE = 20 * 1024 * 1024
export const MAX_VIDEO_SIZE = 100 * 1024 * 1024
export const MAX_FILE_SIZE = 50 * 1024 * 1024

const THUMBNAIL_MAX_SIDE = 480
const THUMBNAIL_QUALITY = 0.72
const VIDEO_READY_TIMEOUT = 15000

export type ProbedMedia = {
  kind: EAttachmentKind
  contentType: string
  width: number | null
  height: number | null
  durationMs: number | null
  thumbnail: Blob | null
}

export function contentTypeOf(file: File): string {
  if (file.type !== "") {
    return file.type
  }
  const extension = file.name.split(".").pop()?.toLowerCase() ?? ""
  return EXTENSION_CONTENT_TYPES[extension] ?? ""
}

export function attachmentKind(contentType: string): EAttachmentKind | null {
  if (IMAGE_CONTENT_TYPES.includes(contentType)) {
    return EAttachmentKind.Image
  }
  if (VIDEO_CONTENT_TYPES.includes(contentType)) {
    return EAttachmentKind.Video
  }
  if (FILE_CONTENT_TYPES.includes(contentType)) {
    return EAttachmentKind.File
  }
  return null
}

export function maxSize(kind: EAttachmentKind): number {
  if (kind === EAttachmentKind.Image) {
    return MAX_IMAGE_SIZE
  }
  return kind === EAttachmentKind.Video ? MAX_VIDEO_SIZE : MAX_FILE_SIZE
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
      contentType: file.type,
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
      contentType: file.type,
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
  const contentType = contentTypeOf(file)
  const kind = attachmentKind(contentType)

  if (kind === null) {
    throw new Error("Такой тип файла отправить нельзя")
  }

  if (file.size > maxSize(kind)) {
    throw new Error(`Файл больше ${formatSize(maxSize(kind))}`)
  }

  if (kind === EAttachmentKind.Image) {
    return await probeImage(file)
  }

  if (kind === EAttachmentKind.Video) {
    return await probeVideo(file)
  }

  return {
    kind,
    contentType,
    width: null,
    height: null,
    durationMs: null,
    thumbnail: null,
  }
}

const KIND_LABELS: Record<EAttachmentKind, string> = {
  [EAttachmentKind.Image]: "Фото",
  [EAttachmentKind.Video]: "Видео",
  [EAttachmentKind.File]: "Файл",
}

export function attachmentsLabel(attachments: { kind: EAttachmentKind; name: string }[]): string {
  const single = attachments.length === 1 ? attachments[0] : undefined

  if (single === undefined) {
    return attachments.length > 1 ? `Вложения (${attachments.length})` : ""
  }

  return single.kind === EAttachmentKind.File ? single.name : KIND_LABELS[single.kind]
}

export function messagePreview(message: {
  text: string
  attachments: { kind: EAttachmentKind; name: string }[]
}): string {
  return message.text !== "" ? message.text : attachmentsLabel(message.attachments)
}
