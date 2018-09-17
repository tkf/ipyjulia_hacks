import pytest

from ..examples import simple_async, background_tasks

example_modules = [
    simple_async,
    background_tasks,
]


@pytest.mark.asyncio
@pytest.mark.parametrize("module", example_modules)
async def test_some_asyncio_code(module, julia):
    await module.main()
