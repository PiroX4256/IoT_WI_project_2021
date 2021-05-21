import asyncio
import logging

import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():
    connection = await Context.create_client_context()

    request = Message(code=aiocoap.Code.GET, uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com/.well-known/core')

    try:
        response = await connection.request(request).response
    except Exception as e:
        print('Failed to retrieve values from coap')
        print(e)
    else:
        print('Result: %s\n%r' % (response.code, response.payload))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
