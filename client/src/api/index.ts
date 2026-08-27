import { ApolloClient, ApolloLink, HttpLink, InMemoryCache, from, split } from "@apollo/client/core"
import { setContext } from "@apollo/client/link/context"
import { onError } from "@apollo/client/link/error"
import { GraphQLWsLink } from "@apollo/client/link/subscriptions"
import { Observable, getMainDefinition } from "@apollo/client/utilities"
import { provideApolloClient } from "@vue/apollo-composable"
import { createClient } from "graphql-ws"
import { useAuthStore } from "@/stores/auth"

function toWebSocketUrl(url: string): string {
  const resolved = new URL(url, window.location.origin)
  resolved.protocol = resolved.protocol === "https:" ? "wss:" : "ws:"
  return resolved.toString()
}

const httpLink = new HttpLink({
  uri: `${import.meta.env.VITE_API_URL}api`,
  credentials: "include",
})

const wsLink = new GraphQLWsLink(
  createClient({
    url: `${toWebSocketUrl(import.meta.env.VITE_API_URL)}api`,
    connectionParams: () => {
      const { accessToken } = useAuthStore()
      return accessToken !== undefined ? { Authorization: `Bearer ${accessToken}` } : {}
    },
  }),
)

const authLink = setContext((_operation, prevContext) => {
  const { accessToken } = useAuthStore()
  return {
    headers: {
      ...prevContext.headers,
      ...(accessToken !== undefined ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
  }
})

const UNAUTHORIZED_MESSAGES = new Set(["User is not authenticated", "User is not admin"])

const errorLink = onError(({ graphQLErrors, operation, forward }) => {
  if (
    graphQLErrors === undefined ||
    operation.operationName === "Refresh" ||
    !graphQLErrors.some((error) => UNAUTHORIZED_MESSAGES.has(error.message))
  ) {
    return
  }

  return new Observable((observer) => {
    const authStore = useAuthStore()
    authStore
      .refresh()
      .then(() => {
        const subscription = forward(operation).subscribe({
          next: observer.next.bind(observer),
          error: observer.error.bind(observer),
          complete: observer.complete.bind(observer),
        })
        return () => subscription.unsubscribe()
      })
      .catch((error: unknown) => observer.error(error))
  })
})

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query)
    return definition.kind === "OperationDefinition" && definition.operation === "subscription"
  },
  wsLink,
  from([errorLink as ApolloLink, authLink, httpLink]),
)

export const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
})

provideApolloClient(apolloClient)
