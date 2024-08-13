import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


class TestMainApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("httpx.AsyncClient.get")
    def test_healthcheck_lifespan(self, mock_get):
        # Mock the response for the healthcheck call during app startup
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "Service is up and running"}
        mock_get.return_value.__aenter__.return_value = mock_response

        # Test the healthcheck endpoint
        response = self.client.get("/api/healthcheck/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Service is up and running"})

    @patch("httpx.AsyncClient.get")
    def test_lifespan_startup_shutdown(self, mock_get):
        # Mock the response for the healthcheck call during app startup
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_get.return_value.__aenter__.return_value = mock_response

        # Trigger application startup and shutdown
        with TestClient(app):
            # This will automatically trigger the lifespan events
            pass

        # Ensure that the mocked HTTP GET request was called during startup
        mock_get.assert_called_once_with(
            "http://accounts:8000/accounts/api/healthcheck/",
            headers={"Host": "localhost"},
        )


if __name__ == "__main__":
    unittest.main()
