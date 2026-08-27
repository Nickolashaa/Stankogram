/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type EUserRole = "STUDENT" | "TEACHER"

export type MarkChatReadMutationVariables = Exact<{
  chatId: number
}>

export type MarkChatReadMutation = {
  markChatRead:
    | {
        __typename: "ChatParticipant"
        id: number
        isAdmin: boolean
        isMuted: boolean
        lastReadAt: string | null
        user: {
          id: number
          createdAt: string
          updatedAt: string
          name: string
          surname: string
          patronymic: string | null
          email: string
          role: Types.EUserRole
          isAdmin: boolean
        }
      }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const MarkChatReadDocument = gql`
  mutation MarkChatRead($chatId: Int!) {
    markChatRead(chatId: $chatId) {
      __typename
      ... on ChatParticipant {
        id
        isAdmin
        isMuted
        lastReadAt
        user {
          ...UserFields
        }
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
  ${UserFieldsFragmentDoc}
`

/**
 * __useMarkChatReadMutation__
 *
 * To run a mutation, you first call `useMarkChatReadMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useMarkChatReadMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useMarkChatReadMutation({
 *   variables: {
 *     chatId: // value for 'chatId'
 *   },
 * });
 */
export function useMarkChatReadMutation(
  options:
    | VueApolloComposable.UseMutationOptions<MarkChatReadMutation, MarkChatReadMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<MarkChatReadMutation, MarkChatReadMutationVariables>
      > = {},
) {
  return VueApolloComposable.useMutation<MarkChatReadMutation, MarkChatReadMutationVariables>(
    MarkChatReadDocument,
    options,
  )
}
export type MarkChatReadMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  MarkChatReadMutation,
  MarkChatReadMutationVariables
>
