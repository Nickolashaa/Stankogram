/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { SystemNotificationFieldsFragmentDoc } from "../../fragments/system-notifications.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type SystemNotificationIn = {
  text: string
}

export type UpdateSystemNotificationMutationVariables = Exact<{
  id: number
  input: Types.SystemNotificationIn
}>

export type UpdateSystemNotificationMutation = {
  updateSystemNotification:
    | { __typename: "ObjectNotFoundError"; message: string }
    | {
        __typename: "SystemNotification"
        id: number
        createdAt: string
        updatedAt: string
        text: string
      }
}

export const UpdateSystemNotificationDocument = gql`
  mutation UpdateSystemNotification($id: Int!, $input: SystemNotificationIn!) {
    updateSystemNotification(id: $id, input: $input) {
      __typename
      ... on SystemNotification {
        ...SystemNotificationFields
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
  ${SystemNotificationFieldsFragmentDoc}
`

/**
 * __useUpdateSystemNotificationMutation__
 *
 * To run a mutation, you first call `useUpdateSystemNotificationMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUpdateSystemNotificationMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUpdateSystemNotificationMutation({
 *   variables: {
 *     id: // value for 'id'
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUpdateSystemNotificationMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        UpdateSystemNotificationMutation,
        UpdateSystemNotificationMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          UpdateSystemNotificationMutation,
          UpdateSystemNotificationMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    UpdateSystemNotificationMutation,
    UpdateSystemNotificationMutationVariables
  >(UpdateSystemNotificationDocument, options)
}
export type UpdateSystemNotificationMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    UpdateSystemNotificationMutation,
    UpdateSystemNotificationMutationVariables
  >
