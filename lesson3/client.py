import asyncio
from functools import partial
from signal import SIGINT, SIGTERM
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class ClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        # transport.write(self.message.encode())
        logging.info('Connected to the server!')

    def data_received(self, data):
        logging.info(f'Data received: {data.decode()}')

    def connection_lost(self, exc):
        logging.info('The server closed the connection')
        self.on_con_lost.set_result(True)


def immediate_exit(signal_enum, loop):
    logging.info(f"immediate_exit...")
    loop.stop()
    raise Exception("Close connection...")


async def start_client():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'
    
    for signal_enum in [SIGINT, SIGTERM]:
        exit_func = partial(immediate_exit, signal_enum=signal_enum, loop=loop)
        loop.add_signal_handler(signal_enum, exit_func)
    
    transport, protocol = await loop.create_connection(
        lambda: ClientProtocol(message, on_con_lost),
        '127.0.0.1', 8000
    )
    
    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(start_client())
