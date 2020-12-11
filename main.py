import aiohttp
import asyncio
import yaml


async def test(templates: list, iteration, processes):
    async with aiohttp.ClientSession() as session:
        for action in templates:
            if 'http' in action.keys():
                params = action.get('http')
                method = params['method']
                if method == 'GET':
                    async with session.get(params['url']) as response:
                        print(f"{params['title']}-processes:{processes}-iteration:{iteration}-{response.status == params['success']}")
                elif method == 'POST':
                    async with session.post(params['url'], json=params['body']) as response:
                        print(f"{params['title']}-processes:{processes}-iteration:{iteration}-{response.status == params['success']}")
                elif method == 'PATCH':
                    async with session.patch(params['url'], json=params['body']) as response:
                        print(f"{params['title']}-processes:{processes}-iteration:{iteration}-{response.status == params['success']}")
                elif method == 'DELETE':
                    get_url = params['url'][:-1]
                    async with session.get(get_url) as response:
                        id = await response.text()
                        id = eval(id)
                    async with session.delete(f"{params['url']}{id['id']}") as response:
                        print(f"{params['title']}-processes:{processes}-iteration:{iteration}-{response.status == params['success']}")

            else:
                await asyncio.sleep(action['sleep']['duration'])


async def main(templates):
    for iterator in range(templates['iterations']):
        for processes in range(templates['processes']):
            task = asyncio.create_task(test(templates['actions'], iterator, processes))
            await task


if __name__ == '__main__':
    with open('test.yaml') as f:
        templates = yaml.safe_load(f)
    asyncio.run(main(templates))

