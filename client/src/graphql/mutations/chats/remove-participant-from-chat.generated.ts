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
export type RemoveParticipantFromChatMutationVariables = Exact<{
  chatId: number
  userId: number
}>

export type RemoveParticipantFromChatMutation = { removeParticipantFromChat: null | null }

export const RemoveParticipantFromChatDocument = gql`
  mutation RemoveParticipantFromChat($chatId: Int!, $userId: Int!) {
    removeParticipantFromChat(chatId: $chatId, userId: $userId)
  }
`

/**
 * __useRemoveParticipantFromChatMutation__
 *
 * To run a mutation, you first call `useRemoveParticipantFromChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useRemoveParticipantFromChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useRemoveParticipantFromChatMutation({
 *   variables: {
 *     chatId: // value for 'chatId'
 *     userId: // value for 'userId'
 *   },
 * });
 */
export function useRemoveParticipantFromChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        RemoveParticipantFromChatMutation,
        RemoveParticipantFromChatMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          RemoveParticipantFromChatMutation,
          RemoveParticipantFromChatMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    RemoveParticipantFromChatMutation,
    RemoveParticipantFromChatMutationVariables
  >(RemoveParticipantFromChatDocument, options)
}
export type RemoveParticipantFromChatMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    RemoveParticipantFromChatMutation,
    RemoveParticipantFromChatMutationVariables
  >
