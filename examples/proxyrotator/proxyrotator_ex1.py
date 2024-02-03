import os

from dotenv import load_dotenv
from proxygrabkit import RotatingProxyClient

# LOAD SETTINGS
load_dotenv()
API_KEY = os.getenv("ROTATING_PROXY_API_KEY", None)

if API_KEY is None:
    # API key is mandatory for use RotatingProxy API from ProxyRotator
    raise Exception("API_KEY must ve provided.")

proxy_fetcher = RotatingProxyClient(api_key=API_KEY)

proxy = proxy_fetcher.get_proxy()

print( proxy.proxy )
print( proxy.lastChecked )
