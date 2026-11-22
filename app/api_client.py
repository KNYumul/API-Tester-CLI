
import requests


def send_request(method, url, headers=None, body=None, timeout=15):
    """
    Sends an HTTP request to the specified REST API endpoint.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: API endpoint
        headers: Optional request headers
        body: Optional JSON request body
        timeout: Maximum waiting time in seconds

    Returns:
        requests.Response object
    """

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=body,
        timeout=timeout
    )

    return response
