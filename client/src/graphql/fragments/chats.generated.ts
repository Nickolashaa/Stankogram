/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type EChatType = "PRIVATE" | "PUBLIC"

export type ChatFieldsFragment = {
  id: number
  createdAt: string
  type: Types.EChatType
  title: string
}

export const ChatFieldsFragmentDoc = gql`
  fragment ChatFields on Chat {
    id
    createdAt
    type
    title
  }
`
