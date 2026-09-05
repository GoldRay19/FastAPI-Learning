import time
import asyncio
# def task():
#     time.sleep(3)
#     return "Done"

async def task():
    await asyncio.sleep(3)
    return "done"                           
