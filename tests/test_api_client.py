
import unittest
from unittest.mock import patch, Mock

from app.api_client import send_request
from app.response_handler import get_status_message


class TestAPIClient(unittest.TestCase):

    @patch("app.api_client.requests.request")
    def test_get_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_request.return_value = mock_response

        response = send_request(
            "GET",
            "https://jsonplaceholder.typicode.com/posts/1"
        )

        self.assertEqual(response.status_code, 200)

        mock_request.assert_called_once_with(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers=None,
            json=None,
            timeout=15
        )

    @patch("app.api_client.requests.request")
    def test_post_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 201

        mock_request.return_value = mock_response

        body = {
            "title": "Test Post",
            "body": "Testing API",
            "userId": 1
        }

        response = send_request(
            "POST",
            "https://jsonplaceholder.typicode.com/posts",
            body=body
        )

        self.assertEqual(response.status_code, 201)

        mock_request.assert_called_once_with(
            method="POST",
            url="https://jsonplaceholder.typicode.com/posts",
            headers=None,
            json=body,
            timeout=15
        )

    @patch("app.api_client.requests.request")
    def test_put_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_request.return_value = mock_response

        body = {"title": "Updated Post"}

        response = send_request(
            "PUT",
            "https://jsonplaceholder.typicode.com/posts/1",
            body=body
        )

        self.assertEqual(response.status_code, 200)

        mock_request.assert_called_once()

    @patch("app.api_client.requests.request")
    def test_delete_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_request.return_value = mock_response

        response = send_request(
            "DELETE",
            "https://jsonplaceholder.typicode.com/posts/1"
        )

        self.assertEqual(response.status_code, 200)

        mock_request.assert_called_once()

    @patch("app.api_client.requests.request")
    def test_request_timeout(self, mock_request):
        import requests

        mock_request.side_effect = requests.exceptions.Timeout

        with self.assertRaises(requests.exceptions.Timeout):
            send_request(
                "GET",
                "https://example.com",
                timeout=1
            )

    def test_success_status_classification(self):
        self.assertEqual(
            get_status_message(200),
            "SUCCESS"
        )

    def test_client_error_classification(self):
        self.assertEqual(
            get_status_message(404),
            "CLIENT ERROR"
        )

    def test_server_error_classification(self):
        self.assertEqual(
            get_status_message(500),
            "SERVER ERROR"
        )


if __name__ == "__main__":
    unittest.main()
