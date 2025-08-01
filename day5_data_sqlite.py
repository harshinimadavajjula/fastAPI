from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

app = FastAPI()

# Step 1: Define the Post database model
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

# Step 2: Define models for request/response
class PostCreate(SQLModel):
    title: str
    content: str

class PostRead(PostCreate):
    id: int

# Step 3: Set up SQLite database engine
sqlite_url = "sqlite:///./posts.db"
engine = create_engine(sqlite_url, echo=True)

# Step 4: Create the table when app starts
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Step 5: Create a new post
@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate):
    new_post = Post(**post.dict())
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

# Step 6: Get all posts
@app.get("/posts/", response_model=List[PostRead])
def get_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
        return posts

# Step 7: Get a post by ID
@app.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

# Step 8: Update a post
@app.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, updated_post: PostCreate):
    with Session(engine) as session:
        existing_post = session.get(Post, post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        existing_post.title = updated_post.title
        existing_post.content = updated_post.content
        session.add(existing_post)
        session.commit()
        session.refresh(existing_post)
        return existing_post

# Step 9: Delete a post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        session.delete(post)
        session.commit()
        return {"message": "Post deleted successfully"}
