# from fastapi import FastAPI
import asyncio

# app=FastAPI()

async def abc():
    print("This is first line")
    await asyncio.sleep(4)
    print("2nd line ")
async def abcd():
    print("3th line ")
    await asyncio.sleep(3)
    print("welcome party")
    print("last line ")

# async def main():
#     await asyncio.gather(
#         abc(),
#         abcd()
#     )

async def main():
    await abc(),
    await abcd()

asyncio.run(main())