
# Basic example for use GimmeProxyClient

from proxygrabkit import GimmeProxyClient

# Declare a object of type GimmeProxyClient
proxy_fetcher = GimmeProxyClient()

# Get a random proxy
proxy = proxy_fetcher.get_proxy()

#print all properties 
for k,v in proxy.__dict__.items():
    print( f'{k}: {v}' )

