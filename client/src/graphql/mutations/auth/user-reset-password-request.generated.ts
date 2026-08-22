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
export type UserResetPasswordRequestMutationVariables = Exact<{
  email: string
}>

export type UserResetPasswordRequestMutation = {
  userResetPasswordRequest: { message: string } | null
}

export const UserResetPasswordRequestDocument = gql`
  mutation UserResetPasswordRequest($email: String!) {
    userResetPasswordRequest(email: $email) {
      message
    }
  }
`

/**
 * __useUserResetPasswordRequestMutation__
 *
 * To run a mutation, you first call `useUserResetPasswordRequestMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUserResetPasswordRequestMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUserResetPasswordRequestMutation({
 *   variables: {
 *     email: // value for 'email'
 *   },
 * });
 */
export function useUserResetPasswordRequestMutation(
  options:
    | VueApolloComposable.UseMutationOptions<
        UserResetPasswordRequestMutation,
        UserResetPasswordRequestMutationVariables
      >
    | ReactiveFunction<
        VueApolloComposable.UseMutationOptions<
          UserResetPasswordRequestMutation,
          UserResetPasswordRequestMutationVariables
        >
      > = {},
) {
  return VueApolloComposable.useMutation<
    UserResetPasswordRequestMutation,
    UserResetPasswordRequestMutationVariables
  >(UserResetPasswordRequestDocument, options)
}
export type UserResetPasswordRequestMutationCompositionFunctionResult =
  VueApolloComposable.UseMutationReturn<
    UserResetPasswordRequestMutation,
    UserResetPasswordRequestMutationVariables
  >
