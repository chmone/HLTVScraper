from hltv_async_api import Hltv
import asyncio

async def main():
    print("HI")
    async with Hltv() as hltv:
        print("HELLO")
        print(await hltv.get_event_info(7148, 'PGL CS2 Major Copenhagen2024'))

if __name__ == '__main__':
    asyncio.run(main())