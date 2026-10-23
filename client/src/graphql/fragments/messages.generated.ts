/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type MessageFieldsFragment = {
  id: number
  createdAt: string
  updatedAt: string
  text: string
  replyTo: { id: number; text: string; user: { id: number; name: string; surname: string } } | null
}

export const MessageFieldsFragmentDoc = gql`
  fragment MessageFields on Message {
    id
    createdAt
    updatedAt
    text
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
`
