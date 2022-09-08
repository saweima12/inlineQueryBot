import asyncio
import json
from meilisearch_python_async import Client

clinet = Client("http://localhost:7700", "meilisearch-master-key")


async def main():
    with open("./test.json", 'r') as fs:
        items = json.load(fs)
        await clinet.index("checked").add_documents(items)


asyncio.run(main())