import asyncio

from ..core import JuliaAPI, get_api


class AsyncJuliaAPI(JuliaAPI):

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

    async def eval_async(self, src, *kwargs):
        chan = self.eval(f"""
        let chan = Channel(1)
            task = @async begin
                ans = let
                    {src}
                end
                put!(chan, ans)
            end
            bind(chan, task)
            chan
        end
        """)
        while not self.isready(chan):
            self.sleep(0.05)
            await asyncio.sleep(0)
        return self.take_b(chan)

    @classmethod
    def from_api(cls, api=None):
        if api is None:
            api = get_api()
        return cls(api.eval_str, api.api)
