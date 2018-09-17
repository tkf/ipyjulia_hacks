from ipyjulia_hacks.py3.async_julia_api import AsyncJuliaAPI


async def main():
    ajl = AsyncJuliaAPI()
    print(await ajl.eval("1"))
    try:
        await ajl.eval('error("oops!")')
    except RuntimeError as err:
        print("Expected exception:")
        print(err)
    else:
        raise AssertionError("No exception!")


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
