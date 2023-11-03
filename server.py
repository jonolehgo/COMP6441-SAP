# uvicorn server:app --reload

from fastapi import FastAPI, Request
from database import make_query
from datetime import datetime
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data['username']
    password = data['password']
    return make_query(f"SELECT username from users where username='{username}' and password='{password}';")


@app.post("/locations")
async def locations(request: Request):
    data = await request.json()
    names = "(" + ", ".join(f"'{name}'" for name in data['names']) + ")"
    return make_query(f"SELECT name, lat, lon FROM locations WHERE name IN {names}")


@app.get("/blog")
async def blog(request: Request):
    return make_query(f"SELECT blog_id, blog_title, body, comments FROM blog WHERE blog_id = 1")


@app.post("/comment")
async def comment(request: Request):
    data = await request.json()
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    data['date'] = date
    existing_comments = json.dumps(get_comments())[:-1]
    new_comment = f', {{"name": "{data["name"]}", "date": "{data["date"]}", "comment": "{data["comment"]}"}}'
    query = f"UPDATE blog SET comments = '{existing_comments + new_comment}]'" + \
        "::jsonb WHERE blog_id = 1;"
    make_query(query, is_select=False)
    return "Comment added successfully"


def get_comments():
    """ helper function to get comments """
    exisiting_comments = make_query(
        f"SELECT comments FROM blog WHERE blog_id = 1")
    return exisiting_comments[0][0]
