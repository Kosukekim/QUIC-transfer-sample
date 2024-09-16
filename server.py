# server.py
import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated

import json

def decodeDictAsJson(data: bytes) -> dict:
    return json.loads(data.decode('utf-8'))

class ServerSideQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quic = None

    def quic_event_received(self, event:QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            data = decodeDictAsJson(event.data)
            
            print(f"value is {data['value']}")
            
            # 通常の応答処理
            response = f"Server received: {data}".encode()
            self._quic.send_stream_data(event.stream_id, response, end_stream=False)
        elif isinstance(event, ConnectionTerminated):
            print(f"Connection terminated. Code:{event.error_code} Reason: {event.reason_phrase}")

async def run_server(host, port):
    configuration = QuicConfiguration(is_client=False)
    configuration.idle_timeout=30.0
    configuration.load_cert_chain("./cert/ssl_cert.pem", "./cert/ssl_key.pem")

    await serve(host, port, configuration=configuration, create_protocol=ServerSideQuicProtocol)

async def main():
    print("Server is starting...")
    await run_server('localhost', 4433)
    await asyncio.Future()  # サーバーを永続的に実行

if __name__ == "__main__":
    asyncio.run(main())
    
