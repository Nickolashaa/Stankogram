/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
  T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never }
import * as Types from "../base-types"

import gql from "graphql-tag"
import { MessageFieldsFragmentDoc } from "../fragments/messages.generated"
import { UserFieldsFragmentDoc } from "../fragments/auth.generated"
import * as VueApolloComposable from "@vue/apollo-composable"
import * as VueCompositionApi from "vue"
export type ReactiveFunction<TParam> = () => TParam
export type EUserRole = "STUDENT" | "TEACHER"

export type EventsSubscriptionVariables = Exact<{ [key: string]: never }>

export type EventsSubscription = {
  events: {
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
    chat: { id: number }
  }
}

export const EventsDocument = gql`
  subscription Events {
    events {
      ...MessageFields
      user {
        ...UserFields
      }
      chat {
        id
      }
    }
  }
  ${MessageFieldsFragmentDoc}
  ${UserFieldsFragmentDoc}
`

/**
 * __useEventsSubscription__
 *
 * To run a query within a Vue component, call `useEventsSubscription` and pass it any options that fit your needs.
 * When your component renders, `useEventsSubscription` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the subscription, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/subscription.html#options;
 *
 * @example
 * const { result, loading, error } = useEventsSubscription();
 */
export function useEventsSubscription(
  options:
    | VueApolloComposable.UseSubscriptionOptions<EventsSubscription, EventsSubscriptionVariables>
    | VueCompositionApi.Ref<
        VueApolloComposable.UseSubscriptionOptions<EventsSubscription, EventsSubscriptionVariables>
      >
    | ReactiveFunction<
        VueApolloComposable.UseSubscriptionOptions<EventsSubscription, EventsSubscriptionVariables>
      > = {},
) {
  return VueApolloComposable.useSubscription<EventsSubscription, EventsSubscriptionVariables>(
    EventsDocument,
    {},
    options,
  )
}
export type EventsSubscriptionCompositionFunctionResult = VueApolloComposable.UseSubscriptionReturn<
  EventsSubscription,
  EventsSubscriptionVariables
>
