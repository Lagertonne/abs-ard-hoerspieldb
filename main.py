from fastapi import FastAPI
from ard_lib import search_book

app = FastAPI()


@app.get("/search")
def search(query: str, author: str = "", mediaType: str = ""):
    results = search_book(query=query, author=author)

    result = {}
    result["matches"] = results
    return result