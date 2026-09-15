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
export type MessagePositionQueryVariables = Exact<{
  messageId: number
}>

export type MessagePositionQuery = { messagePosition: number }

export const MessagePositionDocument = gql`
  query MessagePosition($messageId: Int!) {
    messagePosition(messageId: $messageId)
  }
`

/**
 * __useMessagePositionQuery__
 *
 * To run a query within a Vue component, call `useMessagePositionQuery` and pass it any options that fit your needs.
 * When your component renders, `useMessagePositionQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useMessagePositionQuery({
 *   messageId: // value for 'messageId'
 * });
 */
export function useMessagePositionQuery(
  variables:
    | MessagePositionQueryVariables
    | VueCompositionApi.Ref<MessagePositionQueryVariables>
    | ReactiveFunction<MessagePositionQueryVariables>,
  options:
    | VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
      > = {},
) {
  return VueApolloComposable.useQuery<MessagePositionQuery, MessagePositionQueryVariables>(
    MessagePositionDocument,
    variables,
    options,
  )
}
export function useMessagePositionLazyQuery(
  variables?:
    | MessagePositionQueryVariables
    | VueCompositionApi.Ref<MessagePositionQueryVariables>
    | ReactiveFunction<MessagePositionQueryVariables>,
  options:
    | VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MessagePositionQuery, MessagePositionQueryVariables>
      > = {},
) {
  return VueApolloComposable.useLazyQuery<MessagePositionQuery, MessagePositionQueryVariables>(
    MessagePositionDocument,
    variables,
    options,
  )
}
export type MessagePositionQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  MessagePositionQuery,
  MessagePositionQueryVariables
>
