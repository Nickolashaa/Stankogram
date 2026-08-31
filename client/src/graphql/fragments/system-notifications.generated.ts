/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type SystemNotificationFieldsFragment = {
  id: number
  createdAt: string
  updatedAt: string
  title: string
  text: string
}

export const SystemNotificationFieldsFragmentDoc = gql`
  fragment SystemNotificationFields on SystemNotification {
    id
    createdAt
    updatedAt
    title
    text
  }
`
