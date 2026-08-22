/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../base-types';

import gql from 'graphql-tag';
import { UserFieldsFragmentDoc } from '../../fragments/auth.generated';
import * as VueApolloComposable from '@vue/apollo-composable';
import * as VueCompositionApi from 'vue';
export type ReactiveFunction<TParam> = () => TParam;
export type EUserRole =
  | 'STUDENT'
  | 'TEACHER';

export type UserIn = {
  email: string;
  isAdmin: boolean;
  name: string;
  patronymic?: string | null | undefined;
  role: EUserRole;
  surname: string;
};

export type UserUpdateMutationVariables = Exact<{
  id: number;
  input: Types.UserIn;
}>;


export type UserUpdateMutation = { userUpdate:
    | { __typename: 'ObjectAlreadyExistsError', message: string }
    | { __typename: 'ObjectNotFoundError', message: string }
    | { __typename: 'User', id: number, createdAt: string, updatedAt: string, name: string, surname: string, patronymic: string | null, email: string, role: Types.EUserRole, isAdmin: boolean }
   };


export const UserUpdateDocument = gql`
    mutation UserUpdate($id: Int!, $input: UserIn!) {
  userUpdate(id: $id, input: $input) {
    __typename
    ... on User {
      ...UserFields
    }
    ... on ObjectAlreadyExistsError {
      message
    }
    ... on ObjectNotFoundError {
      message
    }
  }
}
    ${UserFieldsFragmentDoc}`;

/**
 * __useUserUpdateMutation__
 *
 * To run a mutation, you first call `useUserUpdateMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUserUpdateMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUserUpdateMutation({
 *   variables: {
 *     id: // value for 'id'
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUserUpdateMutation(options: VueApolloComposable.UseMutationOptions<UserUpdateMutation, UserUpdateMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<UserUpdateMutation, UserUpdateMutationVariables>> = {}) {
  return VueApolloComposable.useMutation<UserUpdateMutation, UserUpdateMutationVariables>(UserUpdateDocument, options);
}
export type UserUpdateMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<UserUpdateMutation, UserUpdateMutationVariables>;