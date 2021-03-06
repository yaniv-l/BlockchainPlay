# Create a blockchain
import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = { 'index' : len(self.chain) + 1,
                    'timestamp' : str(datetime.datetime.now()),
                    'proof' : proof,
                    'previous_hash' : previous_hash }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            if self.check_proof(self.hash_operation(new_proof, previous_proof)):
                check_proof = True
            else:
              new_proof += 1
        return new_proof

    def hash_operation(self, new_proof, previous_proof):
        return hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

    def check_proof(self, hash_operation, check_char = '0000'):
        if hash_operation[:4] == check_char:
            return True
        else:
            return False

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Check if previous has is correct
            if block['previous_hash'] !=  self.hash(previous_block):
                return False
            # Check if proof is correct
            if self.check_proof(self.hash_operation(block['proof'], previous_block['proof'])) is not True:
                return False
            # advancing to check next block in the chain
            previous_block = block
            block_index += 1
        return True

# Creatting a web app
app = Flask(__name__)

# Creating a blockchain
blockchain = Blockchain()

# Mining a new blockchain
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = { 'message' : 'New block mined succssefuly!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'] }
    return jsonify(response), 200

# Getting the full chain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = { 'chain' : blockchain.chain,
                 'length' : len(blockchain.chain) }
    return jsonify(response), 200

# Is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = blockchain.is_chain_valid(blockchain.chain)
    return jsonify(response), 200

# run the web app
app.run(host = '0.0.0.0', port = 5000)