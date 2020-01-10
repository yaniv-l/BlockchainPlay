# Create a blockchain
import datetime
import json
import hashlib
from Flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self.chain = {}
        self.create_block(proof = 1, previous_has = '0')

    def create_block(self, proof, previous_hash):
        block = { 'index' : len(self.chain) + 1,
                    'timestemp' : str(datetime.datetime.now()),
                    'proof' : proof,
                    'c': previous_has}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            if self.check_proof(self.hash_operation(new_proof, previous_proof)):
                return True
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
            if block['previous_hash'] =  self.hash(previous_block):
                return False
            # Check if proof is correct
            if self.check_proof(self.hash_operation(block['proof'], previous_proof['proof'])) is not True:
                return False
            # advancing to check next block in the chain
            previous_block = block
            block_index += 1

