/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { AttachmentFieldsFragmentDoc } from "../../fragments/messages.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type AttachmentUploadIn = {
  chatId: number
  contentType: string
  durationMs?: number | null | undefined
  height?: number | null | undefined
  name: string
  size: number
  width?: number | null | undefined
}

export type EAttachmentKind = "FILE" | "IMAGE" | "VIDEO"

export type CreateAttachmentUploadMutationVariables = Exact<{
  input: Types.AttachmentUploadIn
}>

export type CreateAttachmentUploadMutation = {
  createAttachmentUpload:
    | {
        __typename: "AttachmentUpload"
        uploadUrl: string
        thumbnailUploadUrl: string | null
        attachment: {
          id: number
          kind: Types.EAttachmentKind
          name: string
          contentType: string
          size: number
          width: number | null
          height: number | null
          durationMs: number | null
          url: string
          thumbnailUrl: string | null
          downloadUrl: string
        }
      }
    | { __typename: "InvalidInputError"; message: string }
    | { __typename: "ObjectNotFoundError"; message: string }
}

export const CreateAttachmentUploadDocument = gql`
  mutation CreateAttachmentUpload($input: AttachmentUploadIn!) {
    createAttachmentUpload(input: $input) {
      __typename
      ... on AttachmentUpload {
        attachment {
          ...AttachmentFields
        }
        uploadUrl
        thumbnailUploadUrl
      }
      ... on InvalidInputError {
        message
      }
      ... on ObjectNotFoundError {
        message
      }
    }
  }
  ${AttachmentFieldsFragmentDoc}
`

/**
 * __useCreateAttachmentUploadMutation__
 *
 * To run a mutation, you first call `useCreateAttachmentUploadMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateAttachmentUploadMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateAttachmentUploadMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateAttachmentUploadMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        CreateAttachmentUploadMutation,
        CreateAttachmentUploadMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          CreateAttachmentUploadMutation,
          CreateAttachmentUploadMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    CreateAttachmentUploadMutation,
    CreateAttachmentUploadMutationVariables
  >(CreateAttachmentUploadDocument, options)
}
export type CreateAttachmentUploadMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    CreateAttachmentUploadMutation,
    CreateAttachmentUploadMutationVariables
  >
