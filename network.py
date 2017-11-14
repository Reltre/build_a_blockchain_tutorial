import requests
from node import Node

class Network(object):

    def __init__(self, node):
        self.nodes = set()
        self.blockchain = node.blockchain


    def register_node(self, node_address):
        """
        Add a new node to the list of nodes

        :param node_address: <String> Node address such as 'http://192.168.0.5:5000'
        :return: None
        """
        node = Node(node_address)
        self.nodes.add(node)

    def resolves_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.blockchain.chain)

        # Grab and verify the chains from all the nodes in our network

        for node in neighbors:
            response = requests.get(f'http://{node.address.netloc}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and Blockchain.valid(blockchain.chain):
                    max_length = length
                    new_chain = blockchain

        # Replace our chain if we discovered a new, valid chain logner than ours
        if new_chain:
            self.blockchain = new_chain
            return True

        return False
