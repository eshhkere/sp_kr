from aiohttp import web
import aiohttp
import aiofiles

async def handle(request):
    page = request.query.get('page', '1')
    url = f'https://dental-first.ru/catalog/?PAGEN_1={page}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()

            lines = text.splitlines()
            lines = lines[:20]

            async with aiofiles.open('async_products.txt', 'a', encoding='utf-8') as f:
                for line in lines:
                    line = line.strip()
                    if line:
                        await f.write(line + '\n')

    return web.Response(text='OK')

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=8080)
