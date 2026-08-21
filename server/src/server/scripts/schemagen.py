from ..graphql.schema import schema

if __name__ == "__main__":
    with open("schema.graphql", "w", encoding="utf-8") as f:
        f.write(schema.as_str() + "\n")
