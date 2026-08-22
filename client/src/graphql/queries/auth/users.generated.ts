/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../../base-types"

import gql from "graphql-tag"
import { UserFieldsFragmentDoc } from "../../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type BasePaginationIn = {
  limit?: number | null | undefined
  offset?: number | null | undefined
}

export type EUserRole = "STUDENT" | "TEACHER"

export type UserFiltersIn = {
  isAdmin?: boolean | null | undefined
  role?: EUserRole | null | undefined
  searchQuery?: string | null | undefined
}

export type UsersQueryVariables = Exact<{
  pagination?: Types.BasePaginationIn | null | undefined
  filters?: Types.UserFiltersIn | null | undefined
}>

export type UsersQuery = {
  users: {
    count: number
    users: Array<{
      id: number
      createdAt: string
      updatedAt: string
      name: string
      surname: string
      patronymic: string | null
      email: string
      role: Types.EUserRole
      isAdmin: boolean
    }>
  }
}

export const UsersDocument = gql`
  query Users($pagination: BasePaginationIn, $filters: UserFiltersIn) {
    users(pagination: $pagination, filters: $filters) {
      count
      users {
        ...UserFields
      }
    }
  }
  ${UserFieldsFragmentDoc}
`

/**
 * __useUsersQuery__
 *
 * To run a query within a Vue component, call `useUsersQuery` and pass it any options that fit your needs.
 * When your component renders, `useUsersQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useUsersQuery({
 *   pagination: // value for 'pagination'
 *   filters: // value for 'filters'
 * });
 */
export function useUsersQuery(
  variables:
    | UsersQueryVariables
    | VueCompositionApi.Ref<UsersQueryVariables>
    | ReactiveFunction<UsersQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>
    | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>>
    | ReactiveFunction<VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>> = {},
) {
  return VueApolloComposable.useQuery<UsersQuery, UsersQueryVariables>(
    UsersDocument,
    variables,
    options,
  )
}
export function useUsersLazyQuery(
  variables:
    | UsersQueryVariables
    | VueCompositionApi.Ref<UsersQueryVariables>
    | ReactiveFunction<UsersQueryVariables> = {},
  options:
    | VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>
    | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>>
    | ReactiveFunction<VueApolloComposable.UseQueryOptions<UsersQuery, UsersQueryVariables>> = {},
) {
  return VueApolloComposable.useLazyQuery<UsersQuery, UsersQueryVariables>(
    UsersDocument,
    variables,
    options,
  )
}
export type UsersQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  UsersQuery,
  UsersQueryVariables
>
