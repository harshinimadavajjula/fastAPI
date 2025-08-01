from fastapi import FastAPI
# import fastAPI.httpx as httpx
import httpx


app = FastAPI()

# Route to fetch GitHub user data
@app.get("/github/{username}")
async def get_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    # If user is not found
    if response.status_code != 200:
        return {"error": "User not found"}
    
    data = response.json()
    return {
        "username": data["login"],
        "name": data.get("name"),
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"],
        "profile_url": data["html_url"],
        "bio": data.get("bio"),
    }
