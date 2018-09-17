import asyncio

from ipyjulia_hacks.py3.async_julia_api import AsyncJuliaAPI


def jl_repeat(ajl, name, num):
    return ajl.eval(rf"""
        for i in 1:{num}
            print("{name} i = $i\n")
            # Using `print` instead of `println` here to force Julia to write
            # everything "at once".
            sleep(0.1)
        end
        return "{name} done"
    """)


# Ideally, the whole API should become asynchronous:
'''
async def jl_repeat(ajl, name, num):
    f = await ajl.eval("""function (name, num)
        for i in 1:num
            @show name, i
            sleep(0.1)
        end
        return "$name done"
    end""")
    return await f(name, num)
'''


async def py_repeat(name, num):
    for i in range(num):
        print(name, "i =", i)
        await asyncio.sleep(0.1)
    return f"{name} done"


async def main():
    loop = asyncio.get_event_loop()
    ajl = AsyncJuliaAPI()
    tasks, _ = await asyncio.wait(map(loop.create_task, [
        jl_repeat(ajl, "Julia [A]", 2),
        jl_repeat(ajl, "Julia [B]", 5),
        py_repeat("Python [A]", 2),
        py_repeat("Python [B]", 5),
    ]))
    for t in tasks:
        print(await t)


if __name__ == "__main__":
    import logging

    debug = False
    # debug = True
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
