from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate,PostResponse



app = FastAPI()

text_posts = {
    1: {"title": "Morning Thoughts", "content": "Starting the day with a fresh mindset and strong coffee"},
    2: {"title": "Tech Update", "content": "Exploring new backend frameworks and async patterns today"},
    3: {"title": "Learning Log", "content": "Practiced SQL joins and optimized some queries"},
    4: {"title": "Daily Note", "content": "Consistency beats intensity when building skills"},
    5: {"title": "Project Idea", "content": "Thinking of building a scalable notification system"},
    6: {"title": "Debugging Day", "content": "Fixed a tricky bug related to async event loop blocking"},
    7: {"title": "Backend Insights", "content": "Understanding caching strategies in distributed systems"},
    8: {"title": "Quick Update", "content": "Working on improving API response time and performance"},
    9: {"title": "Evening Reflection", "content": "Learned a lot about system design trade-offs today"},
    10: {"title": "Weekend Build", "content": "Planning to create a mini FastAPI project with Redis"}
}

@app.get("/posts")
def get_all_posts(limit:int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404,detail="Post not found")

    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostCreate:

    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post

@app.delete()