"""
This package provides functionality for obtaining proxies from different sources.

Classes
-------
    - :class:`.proxyrotator.RotatingProxyClient`
    - :class:`.gimmeproxy.GimmeProxyClient`

"""

from .proxyrotator import RotatingProxyClient
from .gimmeproxy import GimmeProxyClient

__all__ = ['RotatingProxyClient', 'GimmeProxyClient']


__version__ = "0.1.5"

VERSION = __version__
