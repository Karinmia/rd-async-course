"""
Async server which generates random data about weather 
and sends it to all connected clients.
"""

import asyncio
import json
import logging
import random

SUPPORTED_CITIES = ['Kyiv', 'Lviv', 'Kharkiv', 'Lisbon', 'Toronto', 'Oslo', 'Tokyo', 'London']

connected_clients: list[asyncio.StreamWriter] = []

def generate_data() -> dict:
    """Generate random data about weather"""
    
    return {
        'city': random.choice(SUPPORTED_CITIES),
        'temperature_celcius': random.randrange(start=-15, stop=30),
        'wind_speed': round(random.uniform(1, 20), 1),
        'rain_probability': random.randint(0, 100)
    }


async def handle_client(_, writer: asyncio.StreamWriter):
    """Accept and handle client connection"""
    
    addr = writer.get_extra_info("peername")
    logging.info(f"Accepted a new connection from: {addr}")
    connected_clients.append(writer)


async def send_data_to_client(conn_writer: asyncio.StreamWriter, data):
    try:
        if conn_writer.is_closing():
            connected_clients.remove(conn_writer)
        else:
            conn_writer.write(data)
            await conn_writer.drain()
    except ConnectionResetError:
        addr = conn_writer.get_extra_info("peername")
        logging.info(f"Failed to send data to client at {addr}")

        connected_clients.remove(conn_writer)


async def broadcast_handler():
    # generate data to broadcast
    data = generate_data()
    prepared_data = json.dumps(data).encode()

    tasks = [
        send_data_to_client(conn_writer, prepared_data)
        for conn_writer in connected_clients
    ]
    await asyncio.gather(*tasks)
    logging.info(f"Broadcasted to {len(connected_clients)} clients...")


async def broadcast():
    """Send weather forecast to all connected clients."""
    
    while True:
        if not connected_clients:
            logging.info("No connected clients...")
            await asyncio.sleep(random.randint(2, 5))
            continue
        
        asyncio.create_task(broadcast_handler())
        
        await asyncio.sleep(random.randint(2, 5))


async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    server = await asyncio.start_server(handle_client, "localhost", 8000)
    logging.info("*** Started server at http://localhost:8000")
    
    asyncio.create_task(broadcast())
    
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
