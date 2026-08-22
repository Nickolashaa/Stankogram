import type { CodegenConfig } from "@graphql-codegen/cli"

const scalars = {
  DateTime: { input: "string", output: "string" },
  Void: { input: "null", output: "null" },
}

const config: CodegenConfig = {
  schema: "../server/schema.graphql",
  generates: {
    "src/graphql/base-types.ts": {
      plugins: ["typescript"],
      config: { scalars },
    },
    "src/graphql/": {
      documents: "src/graphql/**/*.gql",
      preset: "near-operation-file",
      presetConfig: {
        baseTypesPath: "base-types.ts",
      },
      plugins: ["typescript-operations", "typescript-vue-apollo"],
      config: {
        scalars,
        withCompositionFunctions: true,
        vueApolloComposableImportFrom: "@vue/apollo-composable",
        vueCompositionApiImportFrom: "vue",
      },
    },
  },
}

export default config
