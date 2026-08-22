/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../base-types';

import gql from 'graphql-tag';
import * as VueApolloComposable from '@vue/apollo-composable';
import * as VueCompositionApi from 'vue';
export type ReactiveFunction<TParam> = () => TParam;
export type RefreshMutationVariables = Exact<{ [key: string]: never; }>;


export type RefreshMutation = { refresh:
    | { __typename: 'JWTs', accessToken: string }
    | { __typename: 'ObjectNotFoundError', message: string }
    | { __typename: 'UnauthorizedError', message: string }
   };


export const RefreshDocument = gql`
    mutation Refresh {
  refresh {
    __typename
    ... on JWTs {
      accessToken
    }
    ... on UnauthorizedError {
      message
    }
    ... on ObjectNotFoundError {
      message
    }
  }
}
    `;

/**
 * __useRefreshMutation__
 *
 * To run a mutation, you first call `useRefreshMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useRefreshMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useRefreshMutation();
 */
export function useRefreshMutation(options: VueApolloComposable.UseMutationOptions<RefreshMutation, RefreshMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<RefreshMutation, RefreshMutationVariables>> = {}) {
  return VueApolloComposable.useMutation<RefreshMutation, RefreshMutationVariables>(RefreshDocument, options);
}
export type RefreshMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<RefreshMutation, RefreshMutationVariables>;