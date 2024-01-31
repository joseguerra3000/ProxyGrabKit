from dataclasses import dataclass
from typing import Dict, Any
import requests
from requests import Response

@dataclass
class Proxy:
    """ Represent the information returned for a call to proxyrotator API

    Attributes:
        proxy (str): proxy server
        ip (str): server's ip
        port (int): server's port
        connectionType (str): "Residential", "Mobile", or "Datacenter"
        asn (str): ASN network
        isp (str): Internet Service Provider
        type (str): ---
        lastChecked (str): Last check in seconds
        get (bool): Proxy support GET requests
        post (bool): Proxy support POST requests
        cookies (bool): Proxy support cookies
        referer (bool): Proxy support referer header
        userAgent (bool): Proxy support user-agent header
        city (str): City
        state (str): State
        country (str): Country
        randomUserAgent (str): -----
        requestsRemaining (int): Requests Remaining
    """

    proxy: str
    ip: str
    port: int
    connectionType: str
    asn: str
    isp: str
    type: str
    lastChecked: int
    get: bool
    post: bool
    cookies: bool
    referer: bool
    userAgent: bool
    city: str
    state: str
    country: str
    randomUserAgent: str
    requestsRemaining: int
    

class ProxyFetcher(object):
    def __init__(self) -> None:
        pass
    
    def set_filter(self, **kwargs):
        raise Exception( 'This function must be implemented by classes that inherit from ProxyFetcher' )
 
    def get_proxy(self) -> Proxy:
        raise Exception( 'This function must be implemented by classes that inherit from ProxyFetcher' )
    
class ProxyFetcherAPI(ProxyFetcher):
    def __init__(self, api_endpoint, valid_params) -> None:
        super().__init__()
        self._api_endpoint = api_endpoint
        self._valid_params = valid_params
        self._params = {}
	
    def set_params(self, params: Dict[str, Any] = {}, **kwargs) -> dict:
        """
        Set params for api call

        :kwargs dictionary with params used for request.

        """
        self._params = {}
        for k, v in params.items():
            if k in self._valid_params:
                self._params.update({k: v})

        for k, v in kwargs.items():
            if k in self._valid_params:
                self._params.update({k: v})

        return self._params

    def _request_proxy(self, format :str = 'JSON' ) -> 'Response | None':
        try:
            response = requests.get(url=self._api_endpoint, params=self._params)
            response.raise_for_status()
            
            if format == 'JSON':
                return response.json()
            else:
                return response.content
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
        
        return None
            
