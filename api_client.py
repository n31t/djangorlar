"""
API Client Module

This module provides a comprehensive API client for making HTTP requests
with authentication, retry logic, and response handling.
"""

import time
from typing import Dict, Any, Optional, List, Callable
from urllib.parse import urljoin, urlencode
from dataclasses import dataclass
from enum import Enum
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """HTTP methods enumeration."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class RequestConfig:
    """Configuration for API requests."""
    timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    follow_redirects: bool = True


@dataclass
class APIResponse:
    """Standardized API response object."""
    status_code: int
    data: Any
    headers: Dict[str, str]
    success: bool
    error_message: Optional[str] = None
    response_time: float = 0.0


class RateLimiter:
    """Simple rate limiter for API requests."""

    def __init__(self, max_requests: int, time_window: float):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def acquire(self) -> bool:
        """Attempt to acquire permission for a request."""
        current_time = time.time()

        # Remove old requests outside the time window
        self.requests = [req_time for req_time in self.requests
                        if current_time - req_time < self.time_window]

        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False

    def wait_if_needed(self) -> None:
        """Wait if rate limit is exceeded."""
        while not self.acquire():
            time.sleep(0.1)


class APIClient:
    """Comprehensive API client with advanced features."""

    def __init__(self, base_url: str, auth_token: Optional[str] = None,
                 config: Optional[RequestConfig] = None):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            auth_token: Optional authentication token
            config: Request configuration
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.config = config or RequestConfig()
        self.session_headers = {}
        self.rate_limiter = None
        self.request_hooks = []
        self.response_hooks = []

    def set_auth_token(self, token: str) -> None:
        """Set or update the authentication token."""
        self.auth_token = token

    def set_rate_limit(self, max_requests: int, time_window: float) -> None:
        """Configure rate limiting."""
        self.rate_limiter = RateLimiter(max_requests, time_window)

    def add_request_hook(self, hook: Callable) -> None:
        """Add a hook to be called before each request."""
        self.request_hooks.append(hook)

    def add_response_hook(self, hook: Callable) -> None:
        """Add a hook to be called after each response."""
        self.response_hooks.append(hook)

    def _build_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        headers.update(self.session_headers)

        if additional_headers:
            headers.update(additional_headers)

        return headers

    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Build the complete URL with query parameters."""
        url = urljoin(self.base_url, endpoint.lstrip('/'))

        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"

        return url

    def _execute_hooks(self, hooks: List[Callable], *args, **kwargs) -> None:
        """Execute a list of hooks."""
        for hook in hooks:
            try:
                hook(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Hook execution failed: {e}")

    def _make_request_mock(self, method: HTTPMethod, url: str,
                          headers: Dict[str, str], data: Optional[Any] = None) -> APIResponse:
        """
        Mock request implementation (replace with actual HTTP library).
        This is a placeholder - in production, use requests, httpx, or similar.
        """
        start_time = time.time()

        # Simulate API call
        logger.info(f"{method.value} {url}")
        time.sleep(0.1)  # Simulate network delay

        # Mock response
        response_time = time.time() - start_time

        return APIResponse(
            status_code=200,
            data={'message': 'Mock response', 'method': method.value},
            headers={'Content-Type': 'application/json'},
            success=True,
            response_time=response_time
        )

    def _request_with_retry(self, method: HTTPMethod, endpoint: str,
                           data: Optional[Any] = None,
                           params: Optional[Dict[str, Any]] = None,
                           headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a request with retry logic."""
        url = self._build_url(endpoint, params)
        request_headers = self._build_headers(headers)

        for attempt in range(self.config.max_retries):
            try:
                # Apply rate limiting if configured
                if self.rate_limiter:
                    self.rate_limiter.wait_if_needed()

                # Execute request hooks
                self._execute_hooks(self.request_hooks, method, url, data)

                # Make the actual request
                response = self._make_request_mock(method, url, request_headers, data)

                # Execute response hooks
                self._execute_hooks(self.response_hooks, response)

                if response.success:
                    return response

                # Retry on server errors (5xx)
                if response.status_code >= 500 and attempt < self.config.max_retries - 1:
                    logger.warning(f"Server error, retrying... (attempt {attempt + 1})")
                    time.sleep(self.config.retry_delay * (attempt + 1))
                    continue

                return response

            except Exception as e:
                logger.error(f"Request failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    return APIResponse(
                        status_code=0,
                        data=None,
                        headers={},
                        success=False,
                        error_message=str(e)
                    )

        return APIResponse(
            status_code=0,
            data=None,
            headers={},
            success=False,
            error_message="Max retries exceeded"
        )

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a GET request."""
        return self._request_with_retry(HTTPMethod.GET, endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: Optional[Any] = None,
             params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a POST request."""
        return self._request_with_retry(HTTPMethod.POST, endpoint, data=data,
                                       params=params, headers=headers)

    def put(self, endpoint: str, data: Optional[Any] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a PUT request."""
        return self._request_with_retry(HTTPMethod.PUT, endpoint, data=data,
                                       params=params, headers=headers)

    def patch(self, endpoint: str, data: Optional[Any] = None,
              params: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a PATCH request."""
        return self._request_with_retry(HTTPMethod.PATCH, endpoint, data=data,
                                       params=params, headers=headers)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make a DELETE request."""
        return self._request_with_retry(HTTPMethod.DELETE, endpoint, params=params, headers=headers)


def create_api_client(base_url: str, token: Optional[str] = None) -> APIClient:
    """Factory function to create a configured API client."""
    config = RequestConfig(timeout=30, max_retries=3)
    client = APIClient(base_url, auth_token=token, config=config)
    client.set_rate_limit(max_requests=100, time_window=60)
    return client
