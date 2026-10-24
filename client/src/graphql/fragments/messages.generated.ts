/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type EAttachmentKind = "FILE" | "IMAGE" | "VIDEO"

export type AttachmentFieldsFragment = {
  id: number
  kind: Types.EAttachmentKind
  name: string
  contentType: string
  size: number
  width: number | null
  height: number | null
  durationMs: number | null
  url: string
  thumbnailUrl: string | null
  downloadUrl: string
}

export type MessageFieldsFragment = {
  id: number
  createdAt: string
  updatedAt: string
  text: string
  attachments: Array<{
    id: number
    kind: Types.EAttachmentKind
    name: string
    contentType: string
    size: number
    width: number | null
    height: number | null
    durationMs: number | null
    url: string
    thumbnailUrl: string | null
    downloadUrl: string
  }>
  replyTo: { id: number; text: string; user: { id: number; name: string; surname: string } } | null
}

export const AttachmentFieldsFragmentDoc = gql`
  fragment AttachmentFields on Attachment {
    id
    kind
    name
    contentType
    size
    width
    height
    durationMs
    url
    thumbnailUrl
    downloadUrl
  }
`
export const MessageFieldsFragmentDoc = gql`
  fragment MessageFields on Message {
    id
    createdAt
    updatedAt
    text
    attachments {
      ...AttachmentFields
    }
    replyTo {
      id
      text
      user {
        id
        name
        surname
      }
    }
  }
  ${AttachmentFieldsFragmentDoc}
`
