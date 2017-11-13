from blockchain import Blockchain
from uuid import uuid4
from urllib.parse import urlparse

class Node(object):

    def __init__(self, address):
        self.blockchain = Blockchain()
        self.raw_address = address
        self.address = urlparse(address)

        # Generate a globally unique address for this node
        self.id  = str(uuid4()).replace('-', '')
