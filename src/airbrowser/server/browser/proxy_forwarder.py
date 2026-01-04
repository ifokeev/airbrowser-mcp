#!/usr/bin/env python3
"""Simple HTTP proxy forwarder with upstream authentication.

This script runs as a standalone process to forward HTTP/HTTPS proxy requests
to an authenticated upstream proxy. It adds Proxy-Authorization headers to
all outgoing requests.

Usage:
    python proxy_forwarder.py <local_port> <upstream_host> <upstream_port> <username> <password>
"""

import base64
import select
import socket
import sys
import threading


def create_auth_header(username: str, password: str) -> bytes:
    """Create Proxy-Authorization header value."""
    auth_str = f"{username}:{password}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    return f"Proxy-Authorization: Basic {auth_b64}\r\n".encode()


def add_proxy_auth(data: bytes, auth_header: bytes) -> bytes:
    """Add Proxy-Authorization header to HTTP request."""
    # Find the end of the first line (request line)
    first_line_end = data.find(b"\r\n")
    if first_line_end == -1:
        return data

    # Insert auth header after the first line
    return data[: first_line_end + 2] + auth_header + data[first_line_end + 2 :]


def pipe_data(src: socket.socket, dst: socket.socket):
    """Pipe data from src to dst until connection closes."""
    try:
        while True:
            data = src.recv(8192)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass


def handle_client(
    client: socket.socket,
    upstream_host: str,
    upstream_port: int,
    auth_header: bytes,
):
    """Handle a single client connection."""
    try:
        # Read initial request
        data = client.recv(8192)
        if not data:
            client.close()
            return

        # Connect to upstream proxy
        upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream.settimeout(30)
        upstream.connect((upstream_host, upstream_port))

        # Add auth header and forward request
        modified_data = add_proxy_auth(data, auth_header)
        upstream.sendall(modified_data)

        # Check if this is a CONNECT request (for HTTPS)
        if data.startswith(b"CONNECT"):
            # Wait for upstream response
            response = upstream.recv(8192)
            client.sendall(response)

            # If successful, start bidirectional piping
            if b"200" in response.split(b"\r\n")[0]:
                # Set sockets to non-blocking for select
                client.setblocking(False)
                upstream.setblocking(False)

                # Bidirectional pipe
                while True:
                    readable, _, _ = select.select([client, upstream], [], [], 30)
                    if not readable:
                        break

                    for sock in readable:
                        try:
                            data = sock.recv(8192)
                            if not data:
                                raise ConnectionError()
                            if sock is client:
                                upstream.sendall(data)
                            else:
                                client.sendall(data)
                        except Exception:
                            break
                    else:
                        continue
                    break
        else:
            # Regular HTTP request - just pipe the response back
            while True:
                response = upstream.recv(8192)
                if not response:
                    break
                client.sendall(response)

    except Exception:
        pass
    finally:
        try:
            client.close()
        except Exception:
            pass
        try:
            upstream.close()
        except Exception:
            pass


def run_proxy(
    local_port: int,
    upstream_host: str,
    upstream_port: int,
    username: str,
    password: str,
):
    """Run the proxy forwarder server."""
    auth_header = create_auth_header(username, password)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", local_port))
    server.listen(100)

    print(f"PROXY_READY:{local_port}", flush=True)

    while True:
        try:
            client, _ = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client, upstream_host, upstream_port, auth_header),
                daemon=True,
            )
            thread.start()
        except Exception:
            break


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: proxy_forwarder.py <local_port> <upstream_host> <upstream_port> <username> <password>",
            file=sys.stderr,
        )
        sys.exit(1)

    local_port = int(sys.argv[1])
    upstream_host = sys.argv[2]
    upstream_port = int(sys.argv[3])
    username = sys.argv[4]
    password = sys.argv[5]

    run_proxy(local_port, upstream_host, upstream_port, username, password)
