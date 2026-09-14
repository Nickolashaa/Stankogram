/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type UsersImportMutationVariables = Exact<{
  file: File
}>

export type UsersImportMutation = {
  usersImport:
    | { __typename: "InvalidInputError"; message: string }
    | {
        __typename: "UsersImportReport"
        total: number
        succeeded: number
        failed: number
        file: { filename: string; content: string }
      }
}

export const UsersImportDocument = gql`
  mutation UsersImport($file: Upload!) {
    usersImport(file: $file) {
      __typename
      ... on UsersImportReport {
        total
        succeeded
        failed
        file {
          filename
          content
        }
      }
      ... on InvalidInputError {
        message
      }
    }
  }
`

/**
 * __useUsersImportMutation__
 *
 * To run a mutation, you first call `useUsersImportMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUsersImportMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUsersImportMutation({
 *   variables: {
 *     file: // value for 'file'
 *   },
 * });
 */
export function useUsersImportMutation(
  options:
    | VueApolloComposable.UseMutationOptions<UsersImportMutation, UsersImportMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<UsersImportMutation, UsersImportMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<UsersImportMutation, UsersImportMutationVariables>(
    UsersImportDocument,
    options,
  )
}
export type UsersImportMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  UsersImportMutation,
  UsersImportMutationVariables
>
