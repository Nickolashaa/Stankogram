/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { ChatFieldsFragmentDoc } from "../../fragments/chats.generated"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import { MessageFieldsFragmentDoc } from "../../fragments/messages.generated"
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

export type EMessageType = "TEXT"

export type EUserRole = "STUDENT" | "TEACHER"

export type MeChatsQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
  filters?: Types.ChatFiltersIn | null | undefined
}>

export type MeChatsQuery = {
  meChats:
    | {
        __typename: "ChatsMeta"
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
          lastMessage: {
            id: number
            createdAt: string
            text: string
            type: Types.EMessageType
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
          } | null
        }>
      }
    | { __typename: "UnauthorizedError"; message: string }
}

export const MeChatsDocument = gql`
  query MeChats($pagination: BasePaginationIn, $filters: ChatFiltersIn) {
    meChats(pagination: $pagination, filters: $filters) {
      __typename
      ... on ChatsMeta {
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
          lastMessage {
            ...MessageFields
            user {
              ...UserFields
            }
          }
        }
      }
      ... on UnauthorizedError {
        message
      }
    }
  }
  ${ChatFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
  ${MessageFieldsFragmentDoc}
`

/**
 * __useMeChatsQuery__
 *
 * To run a query within a Vue component, call `useMeChatsQuery` and pass it any options that fit your needs.
 * When your component renders, `useMeChatsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useMeChatsQuery({
 *   pagination: // value for 'pagination'
 *   filters: // value for 'filters'
 * });
 */
export function useMeChatsQuery(
  variables:
    | MeChatsQueryVariables
    | VueCompositionApi.Ref<MeChatsQueryVariables>
    | ReactiveFunction<MeChatsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
      > = {},
) {
  return VueApolloComposable.useQuery<MeChatsQuery, MeChatsQueryVariables>(
    MeChatsDocument,
    variables,
    options,
  )
}
export function useMeChatsLazyQuery(
  variables:
    | MeChatsQueryVariables
    | VueCompositionApi.Ref<MeChatsQueryVariables>
    | ReactiveFunction<MeChatsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MeChatsQuery, MeChatsQueryVariables>
      > = {},
) {
  return VueApolloComposable.useLazyQuery<MeChatsQuery, MeChatsQueryVariables>(
    MeChatsDocument,
    variables,
    options,
  )
}
export type MeChatsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  MeChatsQuery,
  MeChatsQueryVariables
>
