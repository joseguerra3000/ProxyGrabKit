from proxygrabkit import RotatingProxyClient
from proxygrabkit.proxyrotator import RotatingProxyException
#from proxygrabkit.proxy import ProxyFetcherAPI
from dotenv import load_dotenv
import os

# LOAD SETTINGS
load_dotenv()
API_KEY = os.getenv( 'ROTATING_PROXY_API_KEY' )

if API_KEY is None:
    raise Exception( 'API_KEY must ve provided.' )

rotator = RotatingProxyClient( api_key=API_KEY )


print(f'Using apiKey: {rotator.api_key}')

#rotator.set_filter( get=True, https=True )
rotator.set_filter( filter = { 
                        'get': True, # Proxy supports GET requests 
                        'city': 'New York', # Return only proxies from New York City	
                        }
                    )
try:
    proxy_info = rotator.get_proxy()
except RotatingProxyException as e:
    print(e)


for i in range(20):
    proxy_info = rotator.get_proxy()
    print( proxy_info.proxy )
    print( f'{proxy_info.city}, {proxy_info.country}' )
    print( proxy_info.connectionType )
    print( rotator.remaining_requests )
    print( '-----------------------' )