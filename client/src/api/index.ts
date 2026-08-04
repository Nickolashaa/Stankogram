import createClient from "openapi-fetch"
import type { paths } from "./schema"

export const client = createClient<paths>({ baseUrl: "http://server:8000/api/" })
