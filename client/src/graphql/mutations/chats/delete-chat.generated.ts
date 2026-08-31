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
export type DeleteChatMutationVariables = Exact<{
  chatId: number
}>

export type DeleteChatMutation = {
  deleteChat:
    | { __typename: "Chat"; id: number }
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const DeleteChatDocument = gql`
  mutation DeleteChat($chatId: Int!) {
    deleteChat(chatId: $chatId) {
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
 * __useDeleteChatMutation__
 *
 * To run a mutation, you first call `useDeleteChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useDeleteChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useDeleteChatMutation({
 *   variables: {
 *     chatId: // value for 'chatId'
 *   },
 * });
 */
export function useDeleteChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<DeleteChatMutation, DeleteChatMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<DeleteChatMutation, DeleteChatMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<DeleteChatMutation, DeleteChatMutationVariables>(
    DeleteChatDocument,
    options,
  )
}
export type DeleteChatMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  DeleteChatMutation,
  DeleteChatMutationVariables
>
