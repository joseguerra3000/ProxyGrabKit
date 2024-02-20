
import requests
from dataclasses import dataclass
from typing import Dict, Any
from requests import HTTPError

@dataclass
class ProxyData:
    """Represents the information of a proxy server.
    
    """
    
    source: str
    """Service used to get the proxy server."""
    
    proxy: str
    """Proxy server(ip:port)."""
    
    ip: str
    """IP address of the proxy server."""
    
    port: int
    """Proxy server port."""
    
    type: str
    """Proxy server type."""

    lastChecked: int
    """Last time the proxy was checked (timestamp)."""
    
    get: bool
    """Whether the proxy supports GET requests."""
    
    post: bool
    """Whether the proxy supports POST requests."""
    
    cookies: bool
    """Whether the proxy supports cookies."""
    
    referer: bool
    """Whether the proxy supports referer."""
    
    userAgent: bool
    """Whether the proxy supports User-Agent."""
    
    city: str
    """City of the proxy server."""
    
    state: str
    """State of the proxy server."""
    
    country: str
    """Country of the proxy server."""
    
    requestsRemaining: int
    """Remaining allowed requests."""


class ProxyFetcher:
    """
    Base class for fetching proxies.
    
    
    """
    def __init__(self) -> None:
        pass
    
    def set_filter(self, **kwargs):
        """
        Sets filters for proxy retrieval.

        :param \*\*kwargs: Arbitrary keyword arguments for setting filters.
        :type \*\*kwargs: dict
        :raises Exception: This function must be implemented by classes that inherit from :class:`ProxyFetcher`.
        """
        raise Exception( 'This function must be implemented by classes that inherit from ProxyFetcher' )

    def get_proxy(self) -> ProxyData:
        """
        Retrieves a proxy.

        :return: ProxyData object representing the retrieved proxy.
        :rtype: ProxyData
        :raises Exception: This function must be implemented by classes that inherit from :class:`ProxyFetcher`.

        """
        raise Exception( 'This function must be implemented by classes that inherit from ProxyFetcher' )


class ProxyFetcherAPI(ProxyFetcher):
    """Base class for fetching proxies from web services.

    """
    
    def __init__(self, api_endpoint, valid_params) -> None:
        """
        Initializes the ProxyFetcherAPI object.

        :param api_endpoint: The endpoint URL of the API.
        :type api_endpoint: str
        :param valid_params: A list of valid parameters for the API request.
        :type valid_params: list
        """
        super().__init__()
        self._api_endpoint = api_endpoint
        self._valid_params = valid_params
        self._params = {}

    def clear_params(self):
        """
        Clears the parameters set for the API request.
        """
        self._params.clear()

    def set_params(self, params: Dict[str, Any] = {}, **kwargs) -> dict:
        """
        Sets parameters for the API call.
        
        :param params: Dictionary with parameters used for the request.
        :type params: dict
        :param \*\*kwargs: Additional keyword arguments with parameters for the request.
        :type \*\*kwargs: dict
        :return: A dictionary containing the set parameters.
        :rtype: dict
        """
        for k, v in params.items():
            if k in self._valid_params:
                self._params.update({k: v})
        
        for k, v in kwargs.items():
            if k in self._valid_params:
                self._params.update({k: v})
        
        return self._params

    def _request_proxy(self, format :str = 'JSON' ) -> 'dict | str':
        """
        Sends a request to the API endpoint to retrieve proxies.
        
        :param format: The format of the response ('JSON' or 'text'). Default is 'JSON'.
        :type format: str, optional
        :return: If format is 'JSON', returns a dictionary representing the response.
                If format is 'text', returns the response text as a string.
        :rtype: dict or str
        """
        try:
            response = requests.get(url=self._api_endpoint, params=self._params)
            response.raise_for_status()
            
        except HTTPError as e:
            print(f"{type(e).__name__}: {e}")
            
        except Exception as e:
            return f'{e}'
        
        if format == 'JSON':
            try:
                return response.json()
            except Exception:
                return str(response.text)
        else:
            return str(response.text)
