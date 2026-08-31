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
export type LeaveChatMutationVariables = Exact<{
  chatId: number
}>

export type LeaveChatMutation = {
  leaveChat:
    | { __typename: "Chat"; id: number }
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const LeaveChatDocument = gql`
  mutation LeaveChat($chatId: Int!) {
    leaveChat(chatId: $chatId) {
      __typename
      ... on Chat {
        id
      }
      ... on InvalidInputError {
        message
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
`

/**
 * __useLeaveChatMutation__
 *
 * To run a mutation, you first call `useLeaveChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useLeaveChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useLeaveChatMutation({
 *   variables: {
 *     chatId: // value for 'chatId'
 *   },
 * });
 */
export function useLeaveChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<LeaveChatMutation, LeaveChatMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<LeaveChatMutation, LeaveChatMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<LeaveChatMutation, LeaveChatMutationVariables>(
    LeaveChatDocument,
    options,
  )
}
export type LeaveChatMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  LeaveChatMutation,
  LeaveChatMutationVariables
>
