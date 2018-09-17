import asyncio

from cached_property import cached_property

from ..core import get_api
from ..core.wrappers import peal


class AsyncJuliaAPI:

    """
    Asynchronous interface to Julia.
    """

    # Can I support other async libraries by?:
    """
    __pyloopinterface = asyncio

    @property
    def pyloopinterface(self):
        return self.__pyloopinterface

    @pyloopinterface.setattr
    def pyloopinterface(self, value):
        self.__pyloopinterface = value
    """

    def __init__(self, sync=None):
        self.sync = sync or get_api()

    @cached_property
    def _async_wrapper(self):
        return self.sync.eval("""func -> function(args...; kwargs...)
            chan = Channel(1)
            task = @async begin
                ans = func(args...; kwargs...)
                put!(chan, ans)
            end
            bind(chan, task)
            return chan
        end""")

    async def _wait_async(self, chan):
        while not self.sync.isready(chan):
            self.sync.sleep(0.05)
            await asyncio.sleep(0)
        return self.sync.take_b(chan)

    def wrapcall(self, callee, *args, **kwargs):
        afun = self._async_wrapper(peal(callee))
        chan = self.sync.wrapcall(peal(afun), *args, **kwargs)
        return self._wait_async(chan)

    def eval(self, src):
        return self.wrapcall(self.sync.include_string,
                             peal(self.sync.Main),
                             src)
