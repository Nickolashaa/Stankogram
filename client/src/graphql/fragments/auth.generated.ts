/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
export type EUserRole = "STUDENT" | "TEACHER"

export type UserFieldsFragment = {
  id: number
  createdAt: string
  updatedAt: string
  name: string
  surname: string
  patronymic: string | null
  email: string
  role: Types.EUserRole
  isAdmin: boolean
}

export const UserFieldsFragmentDoc = gql`
  fragment UserFields on User {
    id
    createdAt
    updatedAt
    name
    surname
    patronymic
    email
    role
    isAdmin
  }
`
