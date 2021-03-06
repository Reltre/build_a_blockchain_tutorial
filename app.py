from node import Node
from network import Network
import getopt, sys

from textwrap import dedent
from flask import Flask, jsonify, request

# Instantiates our Node
app = Flask(__name__)
# Instantiate this app instance's Node
app_node = Node('http://localhost:5000')
# The netword where our nodes are stored, in a real world app this would be housed
# in a separate module
network = Network(app_node)

@app.route('/chain', methods=['GET'])
def full_chain():
    blockchain = app_node.blockchain
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    blockchain = app_node.blockchain
    index = blockchain.new_transaction(values['sender'],values['recipient'], values['amount'])
    response = { 'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/node/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    addresses = []
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for current_node in nodes:
        network.register_node(current_node)

    for current_node in network.nodes:
        addresses.append(current_node.raw_address)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(addresses),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = network.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': network.blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': network.blockchain.chain
        }

    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    blockchain = network.blockchain
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has minded a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

if __name__ == '__main__':
    port = getopt.getopt(sys.argv[1:], "p:")
    port = port[0][0][1]
    app.run(host='0.0.0.0', port=port)
