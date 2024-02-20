
from typing import Any, Dict

from .proxy import ProxyData, ProxyFetcherAPI
from dataclasses import dataclass

@dataclass
class ProxyRP(ProxyData):
    """Represents the information returned for a call to Rotating Proxy API.

    Inherits from the ProxyData class.
    """
    
    connectionType: str
    """The connection type of the proxy ("Residential", "Mobile", or "Datacenter")"""
    
    asn: str
    """ASN network"""
    
    isp: str
    """The Internet Service Provider (ISP) of the proxy."""
    
    randomUserAgent: str
    """A randomly generated user agent string for the proxy."""

class RotatingProxyClient(ProxyFetcherAPI):
    """
    Class for interacting with the Rotating Proxy API from proxyrotator.com.
    
    :param str api_key: The API key provided by proxyrotator.com for the Rotating Proxy API.    
    """
    
    _API_BASE = "http://falcon.proxyrotator.com:51337/"
    
    _VALID_PARAMS = [
        "apiKey",
        "get",
        "post",
        "cookies",
        "referer",
        "userAgent",
        "port",
        "city",
        "state",
        "country",
        "connectionType",
        "asn",
        "isp",
        "xml",
    ]

    def __init__(self, api_key: str) -> None:
        """Constructor of the RotatingProxyClient class.
        
        :param str api_key: The API key provided by proxyrotator.com for the Rotating Proxy API.
        
        .. code-block:: python
        
            rotator = RotatingProxyClient(api_key='xxxxxxxxxxxx')
        """
        
        super().__init__( RotatingProxyClient._API_BASE, RotatingProxyClient._VALID_PARAMS)
        self._api_key = api_key
        self._remaining_requests = None

    def set_filter(self, filter: Dict[str, Any] = {}, **kwargs) -> Dict[str, Any]:
        """
        Sets filters for obtaining the proxy.
        
        :param dict filter: A dictionary with the desired filters for the proxy.
        :param dict \*\*kwargs: Filters indicated individually.
        
        :return: A dict with the filters to be used.
        :rtype: Dict[str, Any]
        
        .. note::
            Valid options for filter:
                - 'get' (true): Proxy supports GET requests
                - 'post' (true): Proxy supports POST requests
                - 'cookies' (true): Proxy supports cookies
                - 'referer' (true): Proxy supports referer header
                - 'userAgent' (true): Proxy supports user-agent header
                - 'port' (integer): Return only proxies with specified port
                - 'city' (string): Return only proxies with specified city
                - 'state' (string): Return only proxies with specified state
                - 'country' (string): Return only proxies with specified country
                - 'connectionType' (string): "Residential", "Mobile", or "Datacenter"
                - 'asn' (string): Return only proxies on the specified ASN's network.
                - 'isp' (string): Return only proxies on the specified ISP's network.
        
        **Example 1:**
        
        .. code-block:: python
        
            rotator = RotatingProxyClient(api_key='xxxxxxxxxxxx')
            rotator.set_filter(get=True, city='New York')
        
        **Example 2:** 
        
        .. code-block:: python
        
            rotator = RotatingProxy( api_key = 'xxxxxxxxxxxx' )
            rotator.set_filter( filter = {
                                'get': True, # Proxy supports GET requests 
                                'city': 'New York', # Return only proxies from New York City	
                                }
                            )
        """

        self.clear_params()
        return self.set_params(filter, **kwargs)

    def get_proxy(self, filter: Dict[str, Any] = None) -> ProxyRP:
        """ Gets a proxy from the API.

        :param dict filter: The filter to apply when fetching the proxy.

        :return: The obtained proxy.
        :rtype: ProxyRP
        
        Examples
        
        .. code-block:: python

            rotator = RotatingProxy( api_key = 'xxxxxxxxxxxx' )
            rotator.set_filter( get = True, city = 'New York' )
            
            proxy = rotator.get_proxy()             
            print( proxy.proxy )
            print( proxy.get )
            print( proxy.city )

        """
        
        if filter is not None:
            self.set_filter(filter=filter)
            
        self.set_params( apiKey = self._api_key )

        body = self._request_proxy( format='JSON' )
        
        if body is None:
            return None
        
        if 'error' in body:
            self._remaining_requests = 0
            error = body['error']
            raise RotatingProxyException( error )

        self._remaining_requests = body["requestsRemaining"]
        return ProxyRP(
            source = 'RotatingProxyAPI',
            proxy = body["proxy"],
            ip = body["ip"],
            port = body["port"],
            connectionType = body["connectionType"],
            asn = body["asn"],
            isp = body['isp'],
            type = body['type'],
            lastChecked = body['lastChecked'],
            get = body['get'],
            post = body['post'],
            cookies = body['cookies'],
            referer = body['referer'],
            userAgent = body['userAgent'],
            city = body['city'],
            state = body['state'],
            country = body['country'],
            randomUserAgent = body['randomUserAgent'],
            requestsRemaining = body['requestsRemaining']
        )


    @property
    def remaining_requests(self) -> 'int | None':
        """ Get the number of remaining requests.
        
        :return: the number of remaining requests
        :rtype: int or None
        """
        return self._remaining_requests
    
    @property
    def api_key(self):
        """ Get the API key used for the Rotating Proxy API.
        
        :return: the API key used for the Rotating Proxy API.
        :rtype: str
        """
        return self._api_key


class RotatingProxyException(Exception):
    """Exception raised for errors related to the RotatingProxyClient.
    
    Inherits from the base Exception class.
    
    :param args: Variable-length argument list.
    """
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)        

    
