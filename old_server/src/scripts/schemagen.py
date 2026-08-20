import json

from ..app import app

if __name__ == "__main__":
    with open("schema.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(app.openapi()))
