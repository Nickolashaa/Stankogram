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
export type UserResetPasswordConfirmMutationVariables = Exact<{
  id: number
  code: string
}>

export type UserResetPasswordConfirmMutation = {
  userResetPasswordConfirm: { message: string } | null
}

export const UserResetPasswordConfirmDocument = gql`
  mutation UserResetPasswordConfirm($id: Int!, $code: String!) {
    userResetPasswordConfirm(id: $id, code: $code) {
      message
    }
  }
`

/**
 * __useUserResetPasswordConfirmMutation__
 *
 * To run a mutation, you first call `useUserResetPasswordConfirmMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUserResetPasswordConfirmMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUserResetPasswordConfirmMutation({
 *   variables: {
 *     id: // value for 'id'
 *     code: // value for 'code'
 *   },
 * });
 */
export function useUserResetPasswordConfirmMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        UserResetPasswordConfirmMutation,
        UserResetPasswordConfirmMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          UserResetPasswordConfirmMutation,
          UserResetPasswordConfirmMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    UserResetPasswordConfirmMutation,
    UserResetPasswordConfirmMutationVariables
  >(UserResetPasswordConfirmDocument, options)
}
export type UserResetPasswordConfirmMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    UserResetPasswordConfirmMutation,
    UserResetPasswordConfirmMutationVariables
  >
