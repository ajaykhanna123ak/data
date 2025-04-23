import asyncio
import logging
import pytest
from utils.decorators import log_resource_usage

logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO, logger="test_logger")
    yield caplog

def test_sync_function_logs(caplog):
    @log_resource_usage(logger)
    def dummy_sync():
        sum(i * i for i in range(10000))
        return "sync-done"

    result = dummy_sync()

    assert result == "sync-done"
    logs = caplog.text
    assert "[SYNC]" in logs
    assert "Function 'dummy_sync'" in logs
    assert "CPU:" in logs
    assert "Memory:" in logs

@pytest.mark.asyncio
async def test_async_function_logs(caplog):
    @log_resource_usage(logger)
    async def dummy_async():
        await asyncio.sleep(0.1)
        return "async-done"

    result = await dummy_async()

    assert result == "async-done"
    logs = caplog.text
    assert "[ASYNC]" in logs
    assert "Function 'dummy_async'" in logs
    assert "CPU:" in logs
    assert "Memory:" in logs
