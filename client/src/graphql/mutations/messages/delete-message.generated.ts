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
export type DeleteMessageMutationVariables = Exact<{
  messageId: number
}>

export type DeleteMessageMutation = {
  deleteMessage:
    | { __typename: "Message"; id: number; chat: { id: number } }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const DeleteMessageDocument = gql`
  mutation DeleteMessage($messageId: Int!) {
    deleteMessage(messageId: $messageId) {
      __typename
      ... on Message {
        id
        chat {
          id
        }
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
`

/**
 * __useDeleteMessageMutation__
 *
 * To run a mutation, you first call `useDeleteMessageMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useDeleteMessageMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useDeleteMessageMutation({
 *   variables: {
 *     messageId: // value for 'messageId'
 *   },
 * });
 */
export function useDeleteMessageMutation(
  options:
    | VueApolloComposable.UseMutationOptions<DeleteMessageMutation, DeleteMessageMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          DeleteMessageMutation,
          DeleteMessageMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<DeleteMessageMutation, DeleteMessageMutationVariables>(
    DeleteMessageDocument,
    options,
  )
}
export type DeleteMessageMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  DeleteMessageMutation,
  DeleteMessageMutationVariables
>
