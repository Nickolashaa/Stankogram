/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { ChatFieldsFragmentDoc } from "../../fragments/chats.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type ChatUpdateIn = {
  title: string
}

export type EChatType = "PRIVATE" | "PUBLIC"

export type UpdateChatMutationVariables = Exact<{
  chatId: number
  input: Types.ChatUpdateIn
}>

export type UpdateChatMutation = {
  updateChat:
    | { __typename: "Chat"; id: number; createdAt: string; type: Types.EChatType; title: string }
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const UpdateChatDocument = gql`
  mutation UpdateChat($chatId: Int!, $input: ChatUpdateIn!) {
    updateChat(chatId: $chatId, input: $input) {
      __typename
      ... on Chat {
        ...ChatFields
      }
      ... on InvalidInputError {
        message
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
  ${ChatFieldsFragmentDoc}
`

/**
 * __useUpdateChatMutation__
 *
 * To run a mutation, you first call `useUpdateChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUpdateChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUpdateChatMutation({
 *   variables: {
 *     chatId: // value for 'chatId'
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUpdateChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<UpdateChatMutation, UpdateChatMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<UpdateChatMutation, UpdateChatMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<UpdateChatMutation, UpdateChatMutationVariables>(
    UpdateChatDocument,
    options,
  )
}
export type UpdateChatMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  UpdateChatMutation,
  UpdateChatMutationVariables
>
