/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { SystemNotificationFieldsFragmentDoc } from "../../fragments/system-notifications.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type BasePaginationIn = {
  limit?: number | null | undefined
  offset?: number | null | undefined
}

export type SystemNotificationsQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
}>

export type SystemNotificationsQuery = {
  systemNotifications: {
    count: number
    systemNotifications: Array<{
      id: number
      createdAt: string
      updatedAt: string
      title: string
      text: string
    }>
  }
}

export const SystemNotificationsDocument = gql`
  query SystemNotifications($pagination: BasePaginationIn) {
    systemNotifications(pagination: $pagination) {
      count
      systemNotifications {
        ...SystemNotificationFields
      }
    }
  }
  ${SystemNotificationFieldsFragmentDoc}
`

/**
 * __useSystemNotificationsQuery__
 *
 * To run a query within a Vue component, call `useSystemNotificationsQuery` and pass it any options that fit your needs.
 * When your component renders, `useSystemNotificationsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useSystemNotificationsQuery({
 *   pagination: // value for 'pagination'
 * });
 */
export function useSystemNotificationsQuery(
  variables:
    | SystemNotificationsQueryVariables
    | VueCompositionApi.Ref<SystemNotificationsQueryVariables>
    | ReactiveFunction<SystemNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<
        SystemNotificationsQuery,
        SystemNotificationsQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          SystemNotificationsQuery,
          SystemNotificationsQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          SystemNotificationsQuery,
          SystemNotificationsQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useQuery<SystemNotificationsQuery, SystemNotificationsQueryVariables>(
    SystemNotificationsDocument,
    variables,
    options,
  )
}
export function useSystemNotificationsLazyQuery(
  variables:
    | SystemNotificationsQueryVariables
    | VueCompositionApi.Ref<SystemNotificationsQueryVariables>
    | ReactiveFunction<SystemNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<
        SystemNotificationsQuery,
        SystemNotificationsQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          SystemNotificationsQuery,
          SystemNotificationsQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          SystemNotificationsQuery,
          SystemNotificationsQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useLazyQuery<
    SystemNotificationsQuery,
    SystemNotificationsQueryVariables
  >(SystemNotificationsDocument, variables, options)
}
export type SystemNotificationsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  SystemNotificationsQuery,
  SystemNotificationsQueryVariables
>
