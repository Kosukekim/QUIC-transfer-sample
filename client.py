import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated

import urllib.request

import json

url = "http://localhost:8000"

class MyClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []
        self.stream_id = None
        self.reconnect_attempts = 0

    async def send_json(self, data:dict):
        if self.stream_id is None:
            self.stream_id = self._quic.get_next_available_stream_id()
        json_data = json.dumps(data).encode('utf-8')
        self._quic.send_stream_data(self.stream_id,json_data, end_stream=False)
        self.transmit()

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            message = event.data.decode()
            print(f"Received: {message}")
        if isinstance(event, ConnectionTerminated):
            print(f"Connection terminated: {event.error_code} - {event.reason_phrase}")
            self._connected = False


async def connection_start():
    configuration = QuicConfiguration(is_client=True,idle_timeout=10.0)
    configuration.verify_mode = False  # 開発環境用。本番環境では適切に設定すること
    req = urllib.request.Request(url)
    randomReadValue = 0
    try:
        while True:
            async with connect(
                "localhost",
                4433,
                configuration=configuration,
                create_protocol=MyClientProtocol
            ) as client:
                while client._connected:
                    with urllib.request.urlopen(req) as res:
                        randomReadValue = json.loads(res.read().decode('utf-8'))
                        randomReadValue["id"] = client._quic.host_cid.hex()
                        print(randomReadValue)
                    await client.send_json(randomReadValue)

                    await asyncio.sleep(2)
                client.close()
                await client.wait_closed()

    except Exception as e:
        print(f"Connection failed: {e}")



async def run_client():
    await connection_start()

if __name__ == "__main__":
    asyncio.run(run_client())