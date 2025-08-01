from fastapi import FastAPI, Query
import httpx

app = FastAPI()

API_KEY = "d99472356b53cc7cb84df293f2febd0b"  # ← Replace this

@app.get("/weather")
async def get_weather(city: str = Query(..., description="City name")):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Failed to fetch weather: {response.status_code}",
            "details": response.text
        }
