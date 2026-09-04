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
export type BasePaginationIn = {
  limit?: number | null | undefined
  offset?: number | null | undefined
}

export type EUserRole = "STUDENT" | "TEACHER"

export type MessageFiltersIn = {
  chatId: number
}

export type MessagesQueryVariables = Exact<{
  filters: Types.MessageFiltersIn
  pagination?: Types.BasePaginationIn | null | undefined
}>

export type MessagesQuery = {
  messages: {
    count: number
    messages: Array<{
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
    }>
  }
}

export const MessagesDocument = gql`
  query Messages($filters: MessageFiltersIn!, $pagination: BasePaginationIn) {
    messages(filters: $filters, pagination: $pagination) {
      count
      messages {
        ...MessageFields
        user {
          ...UserFields
        }
      }
    }
  }
  ${MessageFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
`

/**
 * __useMessagesQuery__
 *
 * To run a query within a Vue component, call `useMessagesQuery` and pass it any options that fit your needs.
 * When your component renders, `useMessagesQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useMessagesQuery({
 *   filters: // value for 'filters'
 *   pagination: // value for 'pagination'
 * });
 */
export function useMessagesQuery(
  variables:
    | MessagesQueryVariables
    | VueCompositionApi.Ref<MessagesQueryVariables>
    | ReactiveFunction<MessagesQueryVariables>,
  options:
    | VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
      > = {},
) {
  return VueApolloComposable.useQuery<MessagesQuery, MessagesQueryVariables>(
    MessagesDocument,
    variables,
    options,
  )
}
export function useMessagesLazyQuery(
  variables?:
    | MessagesQueryVariables
    | VueCompositionApi.Ref<MessagesQueryVariables>
    | ReactiveFunction<MessagesQueryVariables>,
  options:
    | VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MessagesQuery, MessagesQueryVariables>
      > = {},
) {
  return VueApolloComposable.useLazyQuery<MessagesQuery, MessagesQueryVariables>(
    MessagesDocument,
    variables,
    options,
  )
}
export type MessagesQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  MessagesQuery,
  MessagesQueryVariables
>
