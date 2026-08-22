import { ApolloClient, ApolloLink, HttpLink, InMemoryCache, from } from "@apollo/client/core"
import { setContext } from "@apollo/client/link/context"
import { onError } from "@apollo/client/link/error"
import { Observable } from "@apollo/client/utilities"
import { provideApolloClient } from "@vue/apollo-composable"
import { useAuthStore } from "@/stores/auth"

const httpLink = new HttpLink({
  uri: `${import.meta.env.VITE_API_URL}api`,
  credentials: "include",
})

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

export const apolloClient = new ApolloClient({
  link: from([errorLink as ApolloLink, authLink, httpLink]),
  cache: new InMemoryCache(),
})

provideApolloClient(apolloClient)
