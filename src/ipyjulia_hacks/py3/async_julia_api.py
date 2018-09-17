from logging import getLogger
import asyncio

from cached_property import cached_property

from ..core import get_api
from ..core.wrappers import peal

logger = getLogger("async_julia_api")


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
        return self.sync.eval("""
        debug -> func -> function(args...; kwargs...)
            chan = Channel(1)
            task = @async try
                debug("Calling $func($args...; $kwargs...)")
                ans = func(args...; kwargs...)
                debug("typeof(ans) = $ans")
                put!(chan, (true, ans))
            catch err
                put!(chan, (false, err))
            end
            debug("task = $task")
            debug("chan = $chan")
            return chan
        end""")(logger.debug)

    async def _wait_async(self, chan):
        logger.debug("Waiting for %s", chan)
        jl_yield = self.sync.eval("yield", wrap=False)
        while not self.sync.isready(chan):
            logger.debug("Not ready: %s", chan)
            jl_yield()
            await asyncio.sleep(0)
        logger.debug("It's ready. Calling: take!(%s)", chan)
        ok, ans = self.sync.take_b(chan)
        if ok:
            return ans
        else:
            raise RuntimeError(ans)

    def wrapcall(self, callee, *args, **kwargs):
        afun = self._async_wrapper(peal(callee))
        chan = self.sync.wrapcall(peal(afun), *args, **kwargs)
        return self._wait_async(chan)

    def eval(self, src):
        return self.wrapcall(self.sync.include_string,
                             peal(self.sync.Main),
                             src)
