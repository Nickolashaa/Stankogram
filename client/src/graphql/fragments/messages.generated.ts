/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type MessageFieldsFragment = {
  id: number
  createdAt: string
  text: string
  reactions: Array<{ id: number; emoji: string; user: { id: number } }>
}

export const MessageFieldsFragmentDoc = gql`
  fragment MessageFields on Message {
    id
    createdAt
    text
    reactions {
      id
      emoji
      user {
        id
      }
    }
  }
`
