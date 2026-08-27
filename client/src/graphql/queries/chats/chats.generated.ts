/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { ChatFieldsFragmentDoc } from "../../fragments/chats.generated"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type BasePaginationIn = {
  limit?: number | null | undefined
  offset?: number | null | undefined
}

export type ChatFiltersIn = {
  type?: EChatType | null | undefined
}

export type EChatType = "PRIVATE" | "PUBLIC"

export type EUserRole = "STUDENT" | "TEACHER"

export type ChatsQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
  filters?: Types.ChatFiltersIn | null | undefined
}>

export type ChatsQuery = {
  chats: {
    count: number
    chats: Array<{
      id: number
      createdAt: string
      type: Types.EChatType
      title: string
      participants: Array<{
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
      }>
    }>
  }
}

export const ChatsDocument = gql`
  query Chats($pagination: BasePaginationIn, $filters: ChatFiltersIn) {
    chats(pagination: $pagination, filters: $filters) {
      count
      chats {
        ...ChatFields
        participants {
          id
          isAdmin
          isMuted
          user {
            ...UserFields
          }
        }
      }
    }
  }
  ${ChatFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
`

/**
 * __useChatsQuery__
 *
 * To run a query within a Vue component, call `useChatsQuery` and pass it any options that fit your needs.
 * When your component renders, `useChatsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useChatsQuery({
 *   pagination: // value for 'pagination'
 *   filters: // value for 'filters'
 * });
 */
export function useChatsQuery(
  variables:
    | ChatsQueryVariables
    | VueCompositionApi.Ref<ChatsQueryVariables>
    | ReactiveFunction<ChatsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>
    | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>>
    | ReactiveFunction<VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>> = {},
) {
  return VueApolloComposable.useQuery<ChatsQuery, ChatsQueryVariables>(
    ChatsDocument,
    variables,
    options,
  )
}
export function useChatsLazyQuery(
  variables:
    | ChatsQueryVariables
    | VueCompositionApi.Ref<ChatsQueryVariables>
    | ReactiveFunction<ChatsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>
    | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>>
    | ReactiveFunction<VueApolloComposable.UseQueryOptions<ChatsQuery, ChatsQueryVariables>> = {},
) {
  return VueApolloComposable.useLazyQuery<ChatsQuery, ChatsQueryVariables>(
    ChatsDocument,
    variables,
    options,
  )
}
export type ChatsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  ChatsQuery,
  ChatsQueryVariables
>
