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
export type ChatParticipantIn = {
  chatId: number
  isAdmin: boolean
  isMuted: boolean
  userId: number
}

export type EUserRole = "STUDENT" | "TEACHER"

export type AddParticipantToChatMutationVariables = Exact<{
  input: Types.ChatParticipantIn
}>

export type AddParticipantToChatMutation = {
  addParticipantToChat:
    | {
        __typename: "ChatParticipant"
        id: number
        isAdmin: boolean
        isMuted: boolean
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
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectAlreadyExistsError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const AddParticipantToChatDocument = gql`
  mutation AddParticipantToChat($input: ChatParticipantIn!) {
    addParticipantToChat(input: $input) {
      __typename
      ... on ChatParticipant {
        id
        isAdmin
        isMuted
        user {
          ...UserFields
        }
      }
      ... on ObjectNotFoundError {
        message
      }
      ... on ObjectAlreadyExistsError {
        message
      }
      ... on InvalidInputError {
        message
      }
    }
  }
  ${UserFieldsFragmentDoc}
`

/**
 * __useAddParticipantToChatMutation__
 *
 * To run a mutation, you first call `useAddParticipantToChatMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useAddParticipantToChatMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useAddParticipantToChatMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useAddParticipantToChatMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        AddParticipantToChatMutation,
        AddParticipantToChatMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          AddParticipantToChatMutation,
          AddParticipantToChatMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    AddParticipantToChatMutation,
    AddParticipantToChatMutationVariables
  >(AddParticipantToChatDocument, options)
}
export type AddParticipantToChatMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    AddParticipantToChatMutation,
    AddParticipantToChatMutationVariables
  >
