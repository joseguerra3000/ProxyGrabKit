
from proxygrabkit import GimmeProxyClient
from proxygrabkit.gimmeproxy import GimmeProxyException

proxy_fetcher = GimmeProxyClient()

proxy_fetcher.set_filter(get=True, user_agent=True)

p = proxy_fetcher.get_proxy()

while True:
    try:
        print( proxy_fetcher.get_proxy())
    except GimmeProxyException as e:
        print(e)
    
    
     
