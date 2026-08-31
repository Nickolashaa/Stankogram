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

export type CreateSystemNotificationMutationVariables = Exact<{
  input: Types.SystemNotificationIn
}>

export type CreateSystemNotificationMutation = {
  createSystemNotification: { id: number; createdAt: string; updatedAt: string; text: string }
}

export const CreateSystemNotificationDocument = gql`
  mutation CreateSystemNotification($input: SystemNotificationIn!) {
    createSystemNotification(input: $input) {
      ...SystemNotificationFields
    }
  }
  ${SystemNotificationFieldsFragmentDoc}
`

/**
 * __useCreateSystemNotificationMutation__
 *
 * To run a mutation, you first call `useCreateSystemNotificationMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateSystemNotificationMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateSystemNotificationMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateSystemNotificationMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        CreateSystemNotificationMutation,
        CreateSystemNotificationMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          CreateSystemNotificationMutation,
          CreateSystemNotificationMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    CreateSystemNotificationMutation,
    CreateSystemNotificationMutationVariables
  >(CreateSystemNotificationDocument, options)
}
export type CreateSystemNotificationMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    CreateSystemNotificationMutation,
    CreateSystemNotificationMutationVariables
  >
