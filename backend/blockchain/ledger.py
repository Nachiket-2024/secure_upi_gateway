# --- Imports ---
import hashlib
import time

# --- Block class represents one transaction record in the blockchain ---
class Block:
    """
    Represents a single transaction block in the blockchain.
    Each block contains transaction details and cryptographic hash.
    """

    def __init__(self, uid, mid, amount, previous_hash="0"):
        """
        Initializes a block with transaction data and computes its hash.

        Args:
            uid (str): User ID (payer)
            mid (str): Merchant ID (payee)
            amount (float): Transaction amount
            previous_hash (str): Hash of the previous block
        """
        self.uid = uid
        self.mid = mid
        self.amount = amount
        self.timestamp = str(time.time())       # Record current time of transaction
        self.previous_hash = previous_hash      # Link to previous block in chain
        self.hash = self.compute_hash()         # Current block's own hash

    def compute_hash(self):
        """
        Computes SHA-256 hash of the block contents.

        Returns:
            str: The hash string
        """
        # Concatenate key block fields into a single string
        block_string = self.uid + self.mid + str(self.amount) + self.timestamp + self.previous_hash

        # Generate SHA-256 hash and return hexadecimal string
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        """
        Converts the block to a dictionary for viewing/export.

        Returns:
            dict: Block data as dictionary
        """
        return {
            "uid": self.uid,
            "mid": self.mid,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "previous_hash": self.previous_hash
        }


# --- Blockchain class holds and manages the full chain ---
class Blockchain:
    """
    Represents a simplified blockchain to store and verify UPI transactions.
    """

    def __init__(self):
        """
        Initializes the blockchain with a genesis block.
        """
        self.chain = []  # List of blocks
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the first (genesis) block in the chain with dummy data.
        """
        genesis_block = Block(uid="0", mid="0", amount=0.0, previous_hash="0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Returns the latest block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, uid, mid, amount):
        """
        Adds a new transaction block to the chain.

        Args:
            uid (str): User ID of the payer
            mid (str): Merchant ID of the payee
            amount (float): Transaction amount
        """
        last_block = self.get_last_block()
        new_block = Block(uid, mid, amount, previous_hash=last_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Verifies integrity of the entire blockchain.

        Returns:
            bool: True if valid, False if tampered
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Recompute the hash and check
            if current.hash != current.compute_hash():
                return False

            # Check that previous_hash field matches actual hash of previous block
            if current.previous_hash != previous.hash:
                return False

        return True

    def to_list(self):
        """
        Converts the entire blockchain into a list of dicts (for viewing).
        """
        return [block.to_dict() for block in self.chain]
