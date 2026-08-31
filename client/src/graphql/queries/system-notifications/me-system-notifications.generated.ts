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

export type SystemNotificationFiltersIn = {
  onlyUnread?: boolean | null | undefined
}

export type MeSystemNotificationsQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
  filters?: Types.SystemNotificationFiltersIn | null | undefined
}>

export type MeSystemNotificationsQuery = {
  meSystemNotifications: {
    count: number
    systemNotifications: Array<{ id: number; createdAt: string; updatedAt: string; text: string }>
  }
}

export const MeSystemNotificationsDocument = gql`
  query MeSystemNotifications(
    $pagination: BasePaginationIn
    $filters: SystemNotificationFiltersIn
  ) {
    meSystemNotifications(pagination: $pagination, filters: $filters) {
      count
      systemNotifications {
        ...SystemNotificationFields
      }
    }
  }
  ${SystemNotificationFieldsFragmentDoc}
`

/**
 * __useMeSystemNotificationsQuery__
 *
 * To run a query within a Vue component, call `useMeSystemNotificationsQuery` and pass it any options that fit your needs.
 * When your component renders, `useMeSystemNotificationsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useMeSystemNotificationsQuery({
 *   pagination: // value for 'pagination'
 *   filters: // value for 'filters'
 * });
 */
export function useMeSystemNotificationsQuery(
  variables:
    | MeSystemNotificationsQueryVariables
    | VueCompositionApi.Ref<MeSystemNotificationsQueryVariables>
    | ReactiveFunction<MeSystemNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<
        MeSystemNotificationsQuery,
        MeSystemNotificationsQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          MeSystemNotificationsQuery,
          MeSystemNotificationsQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          MeSystemNotificationsQuery,
          MeSystemNotificationsQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useQuery<
    MeSystemNotificationsQuery,
    MeSystemNotificationsQueryVariables
  >(MeSystemNotificationsDocument, variables, options)
}
export function useMeSystemNotificationsLazyQuery(
  variables:
    | MeSystemNotificationsQueryVariables
    | VueCompositionApi.Ref<MeSystemNotificationsQueryVariables>
    | ReactiveFunction<MeSystemNotificationsQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<
        MeSystemNotificationsQuery,
        MeSystemNotificationsQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          MeSystemNotificationsQuery,
          MeSystemNotificationsQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          MeSystemNotificationsQuery,
          MeSystemNotificationsQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useLazyQuery<
    MeSystemNotificationsQuery,
    MeSystemNotificationsQueryVariables
  >(MeSystemNotificationsDocument, variables, options)
}
export type MeSystemNotificationsQueryCompositionFunctionResult =
  VueApolloComposable.UseQueryReturn<
    MeSystemNotificationsQuery,
    MeSystemNotificationsQueryVariables
  >
