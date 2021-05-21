import asyncio
import logging
import time

import aiocoap
import parse
from aiocoap import *
from parse import *

logging.basicConfig(level=logging.INFO)
output_file_name = "dataset.dat"


def parsing(row, url):
    row = row.replace("'", "").replace('[', '').replace(']', '').replace(' ', '')
    print(row)
    result = parse("{}" + "||{}" * 6, row)
    if result is not None:
        coords = result[0]
        payload = '|'.join(result[i] for i in range(1, 7))
        print("Write this into dataset...")
        line = url + '\t' + coords + '\t' + payload + '\n'
        with open(output_file_name, 'a+') as f:
            if not any(line == x.rstrip('\n') for x in f):
                f.write(line)
            else:
                print("Already there....")


async def main():
    connection = await Context.create_client_context()

    request = Message(code=aiocoap.Code.GET, uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com/.well-known/core')
    try:
        response = await connection.request(request).response
    except Exception as e:
        print('Failed to retrieve values from coap')
        print(e)
    else:
        urls = []
        res = response.payload
        res = (res.decode()).split(",")
        for r in res:
            urls.append(r.split(';')[0].strip('>').strip('<'))
        for url in urls:
            print(url)
            request2 = Message(code=aiocoap.Code.GET,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url)
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("GET")
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.POST,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url)
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("POST")
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.PUT,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url)
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("PUT")
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.DELETE,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url)
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("DELETE")
                parsing(response2.payload.decode(), url)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
