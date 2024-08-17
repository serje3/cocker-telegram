import json

import aiohttp


async def fetch(url, headers=None, data=None, method="POST"):
    if data is not None:
        data = json.dumps(data)

    print("INTERNAL REQUEST:", method, url, data)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                    method=method, url=url, data=data, headers=headers
            ) as resp:
                return await resp.json()
        except Exception as e:
            return f"An error occurred: {e}"

