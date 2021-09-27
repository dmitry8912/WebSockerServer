from unittest import TestCase
from unittest.mock import create_autospec, Mock, MagicMock
import asyncio

import src.main
from src.main import clients, config, broadcast


# Patch to make Mock awaitable
async def async_magic():
    pass

Mock.__await__ = lambda x: async_magic().__await__()


class Test(TestCase):
    def setUp(self) -> None:
        self.ws_mock = Mock()
        self.loop = asyncio.get_event_loop()
        src.main.clients = set([self.ws_mock])

    # Test to ensure that send was called
    def test_broadcast(self):
        self.loop.run_until_complete(broadcast('test'))
        self.ws_mock.send.assert_called()


