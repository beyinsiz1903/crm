"""Bounded image transport with pinned, public-only DNS and redirect checks."""
import asyncio
import ipaddress
import socket
import ssl

import httpcore
import httpx
from httpcore._backends.auto import AutoBackend

from site_safety import public_address


class PublicNetworkBackend(httpcore.AsyncNetworkBackend):
    def __init__(self):
        self.backend = AutoBackend()

    async def connect_tcp(self, host, port, timeout=None, local_address=None, socket_options=None):
        if port not in {80, 443}:
            raise ValueError('Only public HTTP(S) ports are permitted')
        try:
            addresses = [str(ipaddress.ip_address(host))]
        except ValueError:
            records = await asyncio.wait_for(asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM), timeout=5)
            addresses = list({row[4][0] for row in records})
        if not addresses or not all(public_address(address) for address in addresses):
            raise ValueError('Private/reserved image address rejected')
        # Connect to the validated address, not the hostname. httpcore still
        # supplies the original hostname for SNI and TLS certificate verification.
        return await self.backend.connect_tcp(addresses[0], port, timeout, local_address, socket_options)

    async def connect_unix_socket(self, *args, **kwargs):
        raise ValueError('Unix sockets are not allowed')

    async def sleep(self, seconds):
        await asyncio.sleep(seconds)


def image_client():
    transport = httpx.AsyncHTTPTransport(retries=0)
    transport._pool = httpcore.AsyncConnectionPool(ssl_context=ssl.create_default_context(), network_backend=PublicNetworkBackend(), max_connections=5)
    return httpx.AsyncClient(transport=transport, timeout=15, trust_env=False, follow_redirects=False)
