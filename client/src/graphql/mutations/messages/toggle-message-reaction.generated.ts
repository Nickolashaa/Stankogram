/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { MessageFieldsFragmentDoc } from "../../fragments/messages.generated"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type EUserRole = "STUDENT" | "TEACHER"

export type MessageReactionIn = {
  emoji: string
  messageId: number
}

export type ToggleMessageReactionMutationVariables = Exact<{
  input: Types.MessageReactionIn
}>

export type ToggleMessageReactionMutation = {
  toggleMessageReaction:
    | { __typename: "InvalidInputError" }
    | {
        __typename: "Message"
        id: number
        createdAt: string
        text: string
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
        reactions: Array<{ id: number; emoji: string; user: { id: number } }>
      }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const ToggleMessageReactionDocument = gql`
  mutation ToggleMessageReaction($input: MessageReactionIn!) {
    toggleMessageReaction(input: $input) {
      __typename
      ... on Message {
        ...MessageFields
        user {
          ...UserFields
        }
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
  ${MessageFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
`

/**
 * __useToggleMessageReactionMutation__
 *
 * To run a mutation, you first call `useToggleMessageReactionMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useToggleMessageReactionMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useToggleMessageReactionMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useToggleMessageReactionMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        ToggleMessageReactionMutation,
        ToggleMessageReactionMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          ToggleMessageReactionMutation,
          ToggleMessageReactionMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    ToggleMessageReactionMutation,
    ToggleMessageReactionMutationVariables
  >(ToggleMessageReactionDocument, options)
}
export type ToggleMessageReactionMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    ToggleMessageReactionMutation,
    ToggleMessageReactionMutationVariables
  >
