/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { ChatFieldsFragmentDoc } from "../../fragments/chats.generated"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import { MessageFieldsFragmentDoc } from "../../fragments/messages.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type EChatType = "PRIVATE" | "PUBLIC"

export type EMessageType = "TEXT"

export type EUserRole = "STUDENT" | "TEACHER"

export type PrivateChatIn = {
  participantId: number
}

export type CreatePrivateChatMutationVariables = Exact<{
  input: Types.PrivateChatIn
}>

export type CreatePrivateChatMutation = {
  createPrivateChat:
    | {
        __typename: "Chat"
        id: number
        createdAt: string
        type: Types.EChatType
        title: string
        participants: Array<{
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
        }>
        lastMessage: {
          id: number
          createdAt: string
          text: string
          type: Types.EMessageType
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
        } | null
      }
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectAlreadyExistsError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const CreatePrivateChatDocument = gql`
  mutation CreatePrivateChat($input: PrivateChatIn!) {
    createPrivateChat(input: $input) {
      __typename
      ... on Chat {
        ...ChatFields
        participants {
          id
          isAdmin
          isMuted
          lastReadAt
          user {
            ...UserFields
          }
        }
        lastMessage {
          ...MessageFields
          user {
            ...UserFields
          }
        }
      }
      ... on InvalidInputError {
        message
      }
      ... on ObjectNotFoundError {
        message
      }
      ... on ObjectAlreadyExistsError {
        message
      }
    }
  }
  ${ChatFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
  ${MessageFieldsFragmentDoc}
`

/**
 * __useCreatePrivateChatMutation__
 *
 * To run a mutation, you first call `useCreatePrivateChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreatePrivateChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreatePrivateChatMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreatePrivateChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        CreatePrivateChatMutation,
        CreatePrivateChatMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          CreatePrivateChatMutation,
          CreatePrivateChatMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    CreatePrivateChatMutation,
    CreatePrivateChatMutationVariables
  >(CreatePrivateChatDocument, options)
}
export type CreatePrivateChatMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    CreatePrivateChatMutation,
    CreatePrivateChatMutationVariables
  >
