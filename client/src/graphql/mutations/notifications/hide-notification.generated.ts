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
export type HideNotificationMutationVariables = Exact<{
  id: number
}>

export type HideNotificationMutation = { hideNotification: { message: string } | null }

export const HideNotificationDocument = gql`
  mutation HideNotification($id: Int!) {
    hideNotification(id: $id) {
      message
    }
  }
`

/**
 * __useHideNotificationMutation__
 *
 * To run a mutation, you first call `useHideNotificationMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useHideNotificationMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useHideNotificationMutation({
 *   variables: {
 *     id: // value for 'id'
 *   },
 * });
 */
export function useHideNotificationMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        HideNotificationMutation,
        HideNotificationMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          HideNotificationMutation,
          HideNotificationMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    HideNotificationMutation,
    HideNotificationMutationVariables
  >(HideNotificationDocument, options)
}
export type HideNotificationMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<HideNotificationMutation, HideNotificationMutationVariables>
