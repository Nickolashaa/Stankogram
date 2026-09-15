/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { MessageFieldsFragmentDoc } from "../../fragments/messages.generated"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import { ChatFieldsFragmentDoc } from "../../fragments/chats.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type BasePaginationIn = {
  limit?: number | null | undefined
  offset?: number | null | undefined
}

export type EChatType = "PRIVATE" | "PUBLIC"

export type EUserRole = "STUDENT" | "TEACHER"

export type MeNotificationsQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
}>

export type MeNotificationsQuery = {
  meNotifications: {
    count: number
    notifications: Array<{
      id: number
      createdAt: string
      message: {
        id: number
        createdAt: string
        updatedAt: string
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
        chat: { id: number; createdAt: string; type: Types.EChatType; title: string }
      }
    }>
  }
}

export const MeNotificationsDocument = gql`
  query MeNotifications($pagination: BasePaginationIn) {
    meNotifications(pagination: $pagination) {
      count
      notifications {
        id
        createdAt
        message {
          ...MessageFields
          user {
            ...UserFields
          }
          chat {
            ...ChatFields
          }
        }
      }
    }
  }
  ${MessageFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
  ${ChatFieldsFragmentDoc}
`

/**
 * __useMeNotificationsQuery__
 *
 * To run a query within a Vue component, call `useMeNotificationsQuery` and pass it any options that fit your needs.
 * When your component renders, `useMeNotificationsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useMeNotificationsQuery({
 *   pagination: // value for 'pagination'
 * });
 */
export function useMeNotificationsQuery(
  variables:
    | MeNotificationsQueryVariables
    | VueCompositionApi.Ref<MeNotificationsQueryVariables>
    | ReactiveFunction<MeNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
      > = {},
) {
  return VueApolloComposable.useQuery<MeNotificationsQuery, MeNotificationsQueryVariables>(
    MeNotificationsDocument,
    variables,
    options,
  )
}
export function useMeNotificationsLazyQuery(
  variables:
    | MeNotificationsQueryVariables
    | VueCompositionApi.Ref<MeNotificationsQueryVariables>
    | ReactiveFunction<MeNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<MeNotificationsQuery, MeNotificationsQueryVariables>
      > = {},
) {
  return VueApolloComposable.useLazyQuery<MeNotificationsQuery, MeNotificationsQueryVariables>(
    MeNotificationsDocument,
    variables,
    options,
  )
}
export type MeNotificationsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  MeNotificationsQuery,
  MeNotificationsQueryVariables
>
