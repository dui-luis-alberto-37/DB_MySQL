from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

template = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="statics"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

