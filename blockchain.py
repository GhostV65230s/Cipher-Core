import os
import json
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCKCHAIN_FILE = os.path.join(BASE_DIR, "blockchain.json")


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(d):
        block = Block(
            d["index"],
            d["timestamp"],
            d["data"],
            d["previous_hash"]
        )
        block.hash = d["hash"]
        return block


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        genesis = Block(
            0,
            datetime.now().isoformat(),
            {"event": "GENESIS"},
            "0"
        )
        self.chain = [genesis]
        self.save_chain()

    def load_chain(self):
        try:
            with open(BLOCKCHAIN_FILE, "r") as f:
                data = json.load(f)

            if not data:
                raise ValueError("Empty blockchain file")

            self.chain = [Block.from_dict(b) for b in data]

        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.create_genesis_block()

    def save_chain(self):
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=4)

    def add_block(self, data):
        prev = self.chain[-1]
        block = Block(
            prev.index + 1,
            datetime.now().isoformat(),
            data,
            prev.hash
        )
        self.chain.append(block)
        self.save_chain()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]

            if cur.hash != cur.calculate_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True
