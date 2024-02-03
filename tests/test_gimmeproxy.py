import logging
import os
import unittest
import time

from dotenv import load_dotenv
from proxygrabkit import GimmeProxyClient
from proxygrabkit.gimmeproxy import GimmeProxyException


# LOAD SETTINGS
load_dotenv()
API_KEY = os.getenv("GIMME_PROXY_API_KEY", None)



def dict_isin( a: dict, b: dict ) -> bool:
    for k,v in a.items():
        if k not in b:
            return False
        if b[k] != v:
            return False
    
    return True


class TestGimmeProxy(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._filters = [
            {
                "get": True,  
                "referer": True,
            },
            {
                "get": True,  # Proxy supports GET requests
                "user-agent": True,
            },
            {
                "get": True,  # Proxy supports GET requests
                "post": True,
            },
            {
                "get": True,  # Proxy supports GET requests
                "post": True,
                "supportsHttps": True,
            },
        ]

    def test_filters_assignment(self):
        '''Test that filters are assigned correctly.
        '''
        proxy_fetcher = GimmeProxyClient(api_key=API_KEY)
        
        for f in self._filters:
            f_ret = proxy_fetcher.set_filter( filter=f, maxCheckPeriod=60*60*24 )
            #print(f'return: {f_ret}')
            time.sleep(2)
            self.assertTrue( dict_isin( f, f_ret )  )
            self.assertEqual( f_ret['maxCheckPeriod'], 60*60*24 )
            

    def test_remaining_requests(self):
        '''Test that the returned proxy it's compatible with filter
        '''
        pass


if __name__ == '__main__':
    unittest.main()