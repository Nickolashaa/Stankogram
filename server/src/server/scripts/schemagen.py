from ..graphql.schema import schema


def main() -> None:
    with open("schema.graphql", "w", encoding="utf-8") as f:
        f.write(schema.as_str() + "\n")
