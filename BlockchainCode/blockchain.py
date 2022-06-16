import webbrowser
from hashlib import sha256
import json
import time
from Counter import Counter
import qrcode
from flask import Flask


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        if self.difficulty < 9:
            self.difficulty += 1
        return new_block.index

    def VerifyItem(self, data):
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.transactions)
        found = False
        for l_chain in chain_data:
            for j in l_chain:
                if j == data:
                    found = True
        if found:
            return "Verified"
        else:
            return "Fake"

def generate_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    link = "http://127.0.0.1:5000/check/" + data
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(data+".png")

app = Flask(__name__)
blockchain = Blockchain()
counter = Counter()
sneakers = []
links = ["https://gateway.pinata.cloud/ipfs/QmaKqqQKZsppjU3i66u5SM7Wkj9dWjzraUmchopTL13oUr/balenciaga.png",
         "https://gateway.pinata.cloud/ipfs/QmaKqqQKZsppjU3i66u5SM7Wkj9dWjzraUmchopTL13oUr/dunk.png",
         "https://gateway.pinata.cloud/ipfs/QmaKqqQKZsppjU3i66u5SM7Wkj9dWjzraUmchopTL13oUr/jordan.png",
         "https://gateway.pinata.cloud/ipfs/QmaKqqQKZsppjU3i66u5SM7Wkj9dWjzraUmchopTL13oUr/yeezy.png"]
for i in range(3):
    id = counter.count()
    generate_qrcode(id)
    blockchain.add_new_transaction((id, links[i]))
blockchain.mine()

# Check Blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

# Verify Authenticity
@app.route('/check/<param>',  methods=['GET'])
def VerifyItem(param):
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.transactions)
    found = False
    for l_chain in chain_data:
        for j in l_chain:
            if j[0] == param:
                link = j[1]
                found = True
    if found:
        webbrowser.open("real.html")
        time.sleep(3)
        webbrowser.open(link, new=0)
        return "Verified\n"
    else:
        webbrowser.open("fake.html")
        return "Fake\n"

# ADD new item to blockchain
@app.route('/create/<link>',  methods=['GET'])
def add_item(link):
    id = counter.count()
    generate_qrcode(id)
    blockchain.add_new_transaction((id, link))
    blockchain.mine()
    return "Uploaded"

app.run(debug=True, port=5000)

