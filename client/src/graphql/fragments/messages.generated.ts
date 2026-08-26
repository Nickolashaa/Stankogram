/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type EMessageType = "TEXT"

export type MessageFieldsFragment = {
  id: number
  createdAt: string
  text: string
  type: Types.EMessageType
}

export const MessageFieldsFragmentDoc = gql`
  fragment MessageFields on Message {
    id
    createdAt
    text
    type
  }
`
