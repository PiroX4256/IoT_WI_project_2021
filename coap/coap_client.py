import asyncio

import aiocoap
import parse
from aiocoap import *
from parse import *
import logging

logging.basicConfig(level=logging.INFO)
output_file_name = "dataset.dat"


def parsing(row, url):
    row = row.replace("'", "").replace('[', '').replace(']', '').replace(' ', '')
    result = parse("{}" + "||{}" * 6, row)
    if result is not None:
        coords = result[0]
        payload = '|'.join(result[i] for i in range(1, 7))
        print("Write this into dataset...")
        line = url.get('url') + '\t' + coords + '\t' + payload + '\n'
        with open(output_file_name, 'a+') as f:
            if not any(line == x.rstrip('\n') for x in f):
                f.write(line)
            else:
                print("Already there....")
        return True
    return False


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
        print(res)
        for r in res:
            temp = r.split(';')
            line_dict = {'url': temp[0].strip('>').strip('<'), 'obs': True if len(temp) == 3 else False}
            urls.append(line_dict)
        for url in urls:
            print(url)
            '''if url.get('obs'):
                request2 = Message(code=aiocoap.Code.GET,
                                   uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'), observe=0)
                obs_req = connection.request(request2)
                response2 = await obs_req.response
                if response2.payload.decode() != "":
                    print("GET")
                    observed = []
                    async for r in obs_req.observation:
                        print("Provo ad iterare")
                        print(r.payload.decode())
                        if r.payload.decode() in observed:
                            print("Ehi ma c'è già!")
                            break
                        observed.append(r.payload.decode())
                        if parsing(response2.payload.decode(), url):
                            break

                request2 = Message(code=aiocoap.Code.POST,
                                   uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'), observe=0)
                obs_req = connection.request(request2)
                response2 = await obs_req.response
                if response2.payload.decode() != "":
                    print("POST")
                    parsing(response2.payload.decode(), url)
                    async for r in obs_req.observation:
                        print("LUL")
                        print(r.payload)

                request2 = Message(code=aiocoap.Code.PUT,
                                   uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'), observe=0)
                obs_req = connection.request(request2)
                response2 = await obs_req.response
                if response2.payload.decode() != "":
                    print("PUT")
                    parsing(response2.payload.decode(), url)
                    async for r in obs_req.observation:
                        print("LUL")
                        print(r.payload)

                request2 = Message(code=aiocoap.Code.DELETE,
                                   uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'), observe=0)
                obs_req = connection.request(request2)
                response2 = await obs_req.response
                if response2.payload.decode() != "":
                    print("DELETE")
                    parsing(response2.payload.decode(), url)
                    async for r in obs_req.observation:
                        print("LUL")
                        print(r.payload)'''
            #else:
            request2 = Message(code=aiocoap.Code.GET,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'))
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("GET")
                print(response2.payload.decode())
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.POST,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'))
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("POST")
                print(response2.payload.decode())
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.PUT,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'))
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("PUT")
                print(response2.payload.decode())
                parsing(response2.payload.decode(), url)

            request2 = Message(code=aiocoap.Code.DELETE,
                               uri='coap://ec2-54-156-245-154.compute-1.amazonaws.com' + url.get('url'))
            response2 = await connection.request(request2).response
            if response2.payload.decode() != "":
                print("DELETE")
                print(response2.payload.decode())
                parsing(response2.payload.decode(), url)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
