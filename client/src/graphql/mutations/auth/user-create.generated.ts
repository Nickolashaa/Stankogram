/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type EUserRole = "STUDENT" | "TEACHER"

export type UserIn = {
  email: string
  isAdmin: boolean
  name: string
  patronymic?: string | null | undefined
  role: EUserRole
  surname: string
}

export type UserCreateMutationVariables = Exact<{
  input: Types.UserIn
}>

export type UserCreateMutation = {
  userCreate:
    | { __typename: "ObjectAlreadyExistsError"; message: string }
    | {
        __typename: "User"
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
}

export const UserCreateDocument = gql`
  mutation UserCreate($input: UserIn!) {
    userCreate(input: $input) {
      __typename
      ... on User {
        ...UserFields
      }
      ... on ObjectAlreadyExistsError {
        message
      }
    }
  }
  ${UserFieldsFragmentDoc}
`

/**
 * __useUserCreateMutation__
 *
 * To run a mutation, you first call `useUserCreateMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUserCreateMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUserCreateMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUserCreateMutation(
  options:
    | VueApolloComposable.UseMutationOptions<UserCreateMutation, UserCreateMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<UserCreateMutation, UserCreateMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<UserCreateMutation, UserCreateMutationVariables>(
    UserCreateDocument,
    options,
  )
}
export type UserCreateMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  UserCreateMutation,
  UserCreateMutationVariables
>
