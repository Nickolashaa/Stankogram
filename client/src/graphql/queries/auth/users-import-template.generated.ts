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
export type UsersImportTemplateQueryVariables = Exact<{ [key: string]: never }>

export type UsersImportTemplateQuery = {
  usersImportTemplate: { filename: string; content: string }
}

export const UsersImportTemplateDocument = gql`
  query UsersImportTemplate {
    usersImportTemplate {
      filename
      content
    }
  }
`

/**
 * __useUsersImportTemplateQuery__
 *
 * To run a query within a Vue component, call `useUsersImportTemplateQuery` and pass it any options that fit your needs.
 * When your component renders, `useUsersImportTemplateQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useUsersImportTemplateQuery();
 */
export function useUsersImportTemplateQuery(
  options:
    | VueApolloComposable.UseQueryOptions<
        UsersImportTemplateQuery,
        UsersImportTemplateQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          UsersImportTemplateQuery,
          UsersImportTemplateQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          UsersImportTemplateQuery,
          UsersImportTemplateQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useQuery<UsersImportTemplateQuery, UsersImportTemplateQueryVariables>(
    UsersImportTemplateDocument,
    {},
    options,
  )
}
export function useUsersImportTemplateLazyQuery(
  options:
    | VueApolloComposable.UseQueryOptions<
        UsersImportTemplateQuery,
        UsersImportTemplateQueryVariables
      >
    | VueCompositionApi.Ref<
        VueApolloComposable.UseQueryOptions<
          UsersImportTemplateQuery,
          UsersImportTemplateQueryVariables
        >
      >
    | ReactiveFunction<
        VueApolloComposable.UseQueryOptions<
          UsersImportTemplateQuery,
          UsersImportTemplateQueryVariables
        >
      > = {},
) {
  return VueApolloComposable.useLazyQuery<
    UsersImportTemplateQuery,
    UsersImportTemplateQueryVariables
  >(UsersImportTemplateDocument, {}, options)
}
export type UsersImportTemplateQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<
  UsersImportTemplateQuery,
  UsersImportTemplateQueryVariables
>
