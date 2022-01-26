import pkg_resources
__version__ = pkg_resources.get_distribution("sosi_blockchair").version

from .client import BlockchairEthClient
