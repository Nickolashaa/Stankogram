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

export type MessageIn = {
  chatId: number
  text: string
}

export type CreateMessageMutationVariables = Exact<{
  input: Types.MessageIn
}>

export type CreateMessageMutation = {
  createMessage:
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
      }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const CreateMessageDocument = gql`
  mutation CreateMessage($input: MessageIn!) {
    createMessage(input: $input) {
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
 * __useCreateMessageMutation__
 *
 * To run a mutation, you first call `useCreateMessageMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateMessageMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateMessageMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateMessageMutation(
  options:
    | VueApolloComposable.UseMutationOptions<CreateMessageMutation, CreateMessageMutationVariables>
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          CreateMessageMutation,
          CreateMessageMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<CreateMessageMutation, CreateMessageMutationVariables>(
    CreateMessageDocument,
    options,
  )
}
export type CreateMessageMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<
  CreateMessageMutation,
  CreateMessageMutationVariables
>
