import json

from ..server import app

if __name__ == "__main__":
    with open("schema.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(app.openapi()))
