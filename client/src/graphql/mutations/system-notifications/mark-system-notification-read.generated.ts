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
export type MarkSystemNotificationReadMutationVariables = Exact<{
  id: number
}>

export type MarkSystemNotificationReadMutation = {
  markSystemNotificationRead: { __typename: "ObjectNotFoundError"; message: string } | null
}

export const MarkSystemNotificationReadDocument = gql`
  mutation MarkSystemNotificationRead($id: Int!) {
    markSystemNotificationRead(id: $id) {
      __typename
      message
    }
  }
`

/**
 * __useMarkSystemNotificationReadMutation__
 *
 * To run a mutation, you first call `useMarkSystemNotificationReadMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useMarkSystemNotificationReadMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useMarkSystemNotificationReadMutation({
 *   variables: {
 *     id: // value for 'id'
 *   },
 * });
 */
export function useMarkSystemNotificationReadMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        MarkSystemNotificationReadMutation,
        MarkSystemNotificationReadMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          MarkSystemNotificationReadMutation,
          MarkSystemNotificationReadMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    MarkSystemNotificationReadMutation,
    MarkSystemNotificationReadMutationVariables
  >(MarkSystemNotificationReadDocument, options)
}
export type MarkSystemNotificationReadMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    MarkSystemNotificationReadMutation,
    MarkSystemNotificationReadMutationVariables
  >
