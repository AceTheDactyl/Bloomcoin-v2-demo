# Wallet Module Expansion Guide

**Module**: `bloomcoin/wallet/`  
**Purpose**: Key management, address derivation, transaction signing  
**Priority**: PHASE 6 (User Interface Layer)

---

## Overview

The wallet module handles cryptographic key management for BloomCoin users:

- **Ed25519** for digital signatures (fast, secure, deterministic)
- **Blake2b** for address derivation (faster than SHA256)
- **BIP39-compatible** mnemonics for key backup

---

## Phase 1: Key Pair Generation

### File: `keypair.py`

**Objective**: Ed25519 key generation and management.

### Implementation Steps

#### Step 1.1: Key Pair Structure

```python
from dataclasses import dataclass
from typing import Optional
import os
import hashlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization

@dataclass
class KeyPair:
    """
    Ed25519 key pair for BloomCoin wallet.
    
    Attributes:
        private_key: 32-byte private key
        public_key: 32-byte public key
        _ed25519_private: Cryptography library key object
    """
    private_key: bytes
    public_key: bytes
    _ed25519_private: Ed25519PrivateKey = None
    
    @classmethod
    def generate(cls, seed: bytes = None) -> 'KeyPair':
        """
        Generate new key pair.
        
        Args:
            seed: Optional 32-byte seed (for deterministic generation)
        
        Returns:
            New KeyPair
        """
        if seed:
            # Deterministic from seed
            if len(seed) < 32:
                seed = hashlib.sha256(seed).digest()
            private = Ed25519PrivateKey.from_private_bytes(seed[:32])
        else:
            # Random generation
            private = Ed25519PrivateKey.generate()
        
        public = private.public_key()
        
        private_bytes = private.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_bytes = public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        return cls(
            private_key=private_bytes,
            public_key=public_bytes,
            _ed25519_private=private
        )
    
    @classmethod
    def from_private_key(cls, private_key: bytes) -> 'KeyPair':
        """Reconstruct key pair from private key."""
        private = Ed25519PrivateKey.from_private_bytes(private_key)
        public = private.public_key()
        
        public_bytes = public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        return cls(
            private_key=private_key,
            public_key=public_bytes,
            _ed25519_private=private
        )
    
    def sign(self, message: bytes) -> bytes:
        """
        Sign a message.
        
        Returns:
            64-byte Ed25519 signature
        """
        return self._ed25519_private.sign(message)
    
    @staticmethod
    def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature.
        
        Returns:
            True if signature is valid
        """
        try:
            public = Ed25519PublicKey.from_public_bytes(public_key)
            public.verify(signature, message)
            return True
        except Exception:
            return False
```

#### Step 1.2: Mnemonic Support

```python
# BIP39 wordlist (English) - first 2048 words
# In practice, load from file
BIP39_WORDLIST = [
    "abandon", "ability", "able", "about", "above", ...
    # Full 2048-word list
]

def generate_mnemonic(strength: int = 128) -> str:
    """
    Generate BIP39-compatible mnemonic phrase.
    
    Args:
        strength: Entropy bits (128 = 12 words, 256 = 24 words)
    
    Returns:
        Space-separated mnemonic phrase
    """
    if strength not in (128, 160, 192, 224, 256):
        raise ValueError("Invalid strength")
    
    entropy = os.urandom(strength // 8)
    
    # Add checksum
    h = hashlib.sha256(entropy).digest()
    checksum_bits = strength // 32
    
    # Convert to binary string
    entropy_bits = bin(int.from_bytes(entropy, 'big'))[2:].zfill(strength)
    checksum = bin(h[0])[2:].zfill(8)[:checksum_bits]
    all_bits = entropy_bits + checksum
    
    # Convert to words
    words = []
    for i in range(0, len(all_bits), 11):
        index = int(all_bits[i:i+11], 2)
        words.append(BIP39_WORDLIST[index])
    
    return ' '.join(words)

def mnemonic_to_seed(mnemonic: str, passphrase: str = '') -> bytes:
    """
    Convert mnemonic to seed.
    
    Uses PBKDF2-HMAC-SHA512 per BIP39.
    
    Returns:
        64-byte seed
    """
    import hashlib
    
    salt = ('mnemonic' + passphrase).encode('utf-8')
    mnemonic_bytes = mnemonic.encode('utf-8')
    
    return hashlib.pbkdf2_hmac(
        'sha512',
        mnemonic_bytes,
        salt,
        iterations=2048,
        dklen=64
    )

def keypair_from_mnemonic(mnemonic: str, passphrase: str = '') -> KeyPair:
    """Generate key pair from mnemonic."""
    seed = mnemonic_to_seed(mnemonic, passphrase)
    return KeyPair.generate(seed=seed[:32])
```

---

## Phase 2: Address Derivation

### File: `address.py`

**Objective**: Derive addresses from public keys.

### Implementation Steps

#### Step 2.1: Address Format

```python
import hashlib
from typing import Optional

# Address prefix bytes
MAINNET_PREFIX = b'\x00'  # 'B' addresses
TESTNET_PREFIX = b'\x6f'  # 't' addresses

def public_key_to_address(
    public_key: bytes,
    testnet: bool = False
) -> str:
    """
    Derive address from public key.
    
    Format:
        1. Blake2b-256(public_key) -> 32 bytes
        2. Take first 20 bytes
        3. Add version prefix
        4. Base58Check encode
    
    Args:
        public_key: 32-byte Ed25519 public key
        testnet: Use testnet prefix
    
    Returns:
        Base58Check encoded address (starts with 'B' or 't')
    """
    # Hash public key
    h = hashlib.blake2b(public_key, digest_size=32).digest()
    
    # Take first 20 bytes (160 bits)
    payload = h[:20]
    
    # Add prefix
    prefix = TESTNET_PREFIX if testnet else MAINNET_PREFIX
    versioned = prefix + payload
    
    # Checksum (first 4 bytes of double-Blake2b)
    checksum = hashlib.blake2b(
        hashlib.blake2b(versioned, digest_size=32).digest(),
        digest_size=32
    ).digest()[:4]
    
    # Base58 encode
    return base58_encode(versioned + checksum)

def address_to_bytes(address: str) -> bytes:
    """
    Decode address to raw bytes.
    
    Returns:
        20-byte address payload (without prefix/checksum)
    """
    decoded = base58_decode(address)
    
    # Verify checksum
    payload = decoded[:-4]
    checksum = decoded[-4:]
    expected = hashlib.blake2b(
        hashlib.blake2b(payload, digest_size=32).digest(),
        digest_size=32
    ).digest()[:4]
    
    if checksum != expected:
        raise ValueError("Invalid address checksum")
    
    # Return payload without prefix
    return payload[1:]

def validate_address(address: str) -> bool:
    """Check if address is valid."""
    try:
        address_to_bytes(address)
        return True
    except Exception:
        return False
```

#### Step 2.2: Base58 Encoding

```python
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(data: bytes) -> str:
    """Base58 encode bytes."""
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    result = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        result = BASE58_ALPHABET[remainder] + result
    
    # Add leading '1's for zeros
    return '1' * leading_zeros + result

def base58_decode(s: str) -> bytes:
    """Base58 decode string to bytes."""
    # Count leading '1's
    leading_ones = 0
    for char in s:
        if char == '1':
            leading_ones += 1
        else:
            break
    
    # Convert from base58
    num = 0
    for char in s:
        num = num * 58 + BASE58_ALPHABET.index(char)
    
    # Convert to bytes
    result = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    
    # Add leading zeros
    return b'\x00' * leading_ones + result
```

---

## Phase 3: Transaction Signing

### File: `signer.py`

**Objective**: Sign transactions with wallet keys.

### Implementation Steps

#### Step 3.1: Transaction Signer

```python
from ..blockchain.transaction import Transaction, TxInput, TxOutput

class TransactionSigner:
    """
    Signs transactions with wallet keys.
    
    Supports:
    - Single signature
    - Multi-signature (future)
    - Hardware wallet integration (future)
    """
    
    def __init__(self, keypair: KeyPair):
        self.keypair = keypair
    
    def sign_transaction(self, tx: Transaction) -> Transaction:
        """
        Sign all inputs in transaction.
        
        Assumes all inputs belong to this wallet.
        
        Returns:
            Transaction with signatures filled in
        """
        # Get signing message
        message = tx.serialize_for_signing()
        
        # Sign each input
        signed_inputs = []
        for inp in tx.inputs:
            signature = self.keypair.sign(message)
            signed_inputs.append(TxInput(
                prev_tx=inp.prev_tx,
                output_index=inp.output_index,
                signature=signature
            ))
        
        return Transaction(
            version=tx.version,
            inputs=signed_inputs,
            outputs=tx.outputs,
            locktime=tx.locktime
        )
    
    def sign_input(
        self,
        tx: Transaction,
        input_index: int
    ) -> bytes:
        """
        Sign a specific input.
        
        For multi-party transactions where each signer
        controls different inputs.
        
        Returns:
            64-byte signature
        """
        message = tx.serialize_for_signing()
        return self.keypair.sign(message)
```

#### Step 3.2: Transaction Builder

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TransactionBuilder:
    """
    Builds transactions from UTXO set.
    
    Handles:
    - Input selection
    - Change output
    - Fee calculation
    """
    utxo_set: dict  # (txid, index) -> TxOutput
    keypair: KeyPair
    fee_rate: int = 1  # satoshis per byte
    
    def build(
        self,
        recipients: list[tuple[str, int]],  # (address, amount)
        change_address: str = None
    ) -> Optional[Transaction]:
        """
        Build a transaction.
        
        Args:
            recipients: List of (address, amount) tuples
            change_address: Address for change (default: own address)
        
        Returns:
            Unsigned transaction, or None if insufficient funds
        """
        from ..constants import PHI_QUAD
        
        # Calculate total needed
        total_out = sum(amount for _, amount in recipients)
        
        # Select inputs (simple: use all available)
        inputs = []
        total_in = 0
        
        my_address = public_key_to_address(self.keypair.public_key)
        my_address_bytes = address_to_bytes(my_address)
        
        for (txid, index), output in self.utxo_set.items():
            if output.address == my_address_bytes:
                inputs.append(TxInput(
                    prev_tx=txid,
                    output_index=index,
                    signature=b'\x00' * 64  # Placeholder
                ))
                total_in += output.amount
        
        # Estimate fee
        tx_size = 100 + len(inputs) * 100 + (len(recipients) + 1) * 40
        fee = tx_size * self.fee_rate
        
        if total_in < total_out + fee:
            return None  # Insufficient funds
        
        # Create outputs
        outputs = []
        for address, amount in recipients:
            outputs.append(TxOutput(
                amount=amount,
                address=address_to_bytes(address)
            ))
        
        # Change output
        change = total_in - total_out - fee
        if change > 0:
            change_addr = change_address or my_address
            outputs.append(TxOutput(
                amount=change,
                address=address_to_bytes(change_addr)
            ))
        
        return Transaction(
            version=1,
            inputs=inputs,
            outputs=outputs,
            locktime=0
        )
```

---

## Phase 4: Wallet Manager

### File: `wallet.py` (Main Integration)

**Objective**: Complete wallet functionality.

```python
from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Optional
from .keypair import KeyPair, generate_mnemonic, keypair_from_mnemonic
from .address import public_key_to_address, validate_address
from .signer import TransactionSigner, TransactionBuilder

@dataclass
class Wallet:
    """
    BloomCoin wallet.
    
    Manages:
    - Key pairs
    - Addresses
    - UTXO tracking
    - Transaction building and signing
    """
    name: str
    keypair: KeyPair
    utxo_set: dict = field(default_factory=dict)
    testnet: bool = False
    
    @property
    def address(self) -> str:
        """Primary receiving address."""
        return public_key_to_address(self.keypair.public_key, self.testnet)
    
    @property
    def balance(self) -> int:
        """Current balance in smallest units."""
        my_addr = address_to_bytes(self.address)
        return sum(
            out.amount for out in self.utxo_set.values()
            if out.address == my_addr
        )
    
    @classmethod
    def create(cls, name: str, testnet: bool = False) -> tuple['Wallet', str]:
        """
        Create new wallet with mnemonic backup.
        
        Returns:
            (wallet, mnemonic)
        """
        mnemonic = generate_mnemonic()
        keypair = keypair_from_mnemonic(mnemonic)
        wallet = cls(name=name, keypair=keypair, testnet=testnet)
        return wallet, mnemonic
    
    @classmethod
    def restore(cls, name: str, mnemonic: str, testnet: bool = False) -> 'Wallet':
        """Restore wallet from mnemonic."""
        keypair = keypair_from_mnemonic(mnemonic)
        return cls(name=name, keypair=keypair, testnet=testnet)
    
    def send(
        self,
        to_address: str,
        amount: int,
        fee_rate: int = 1
    ) -> Optional[bytes]:
        """
        Send funds to address.
        
        Returns:
            Transaction hash if successful, None if insufficient funds
        """
        if not validate_address(to_address):
            raise ValueError(f"Invalid address: {to_address}")
        
        builder = TransactionBuilder(
            utxo_set=self.utxo_set,
            keypair=self.keypair,
            fee_rate=fee_rate
        )
        
        tx = builder.build([(to_address, amount)])
        if tx is None:
            return None
        
        signer = TransactionSigner(self.keypair)
        signed_tx = signer.sign_transaction(tx)
        
        # Broadcast (requires network connection)
        # network.broadcast_tx(signed_tx)
        
        return signed_tx.hash
    
    def update_utxos(self, chain):
        """Scan chain for wallet UTXOs."""
        my_addr = address_to_bytes(self.address)
        self.utxo_set.clear()
        
        spent = set()
        
        for block in chain.iterate_blocks():
            for tx in block.transactions:
                # Mark spent outputs
                for inp in tx.inputs:
                    spent.add((inp.prev_tx, inp.output_index))
                
                # Add our outputs
                for i, out in enumerate(tx.outputs):
                    if out.address == my_addr:
                        if (tx.hash, i) not in spent:
                            self.utxo_set[(tx.hash, i)] = out
    
    def save(self, path: Path, password: str = None):
        """
        Save wallet to file.
        
        WARNING: Private key storage. Use encryption in production!
        """
        data = {
            'name': self.name,
            'private_key': self.keypair.private_key.hex(),
            'testnet': self.testnet
        }
        
        # In production, encrypt with password
        path.write_text(json.dumps(data))
    
    @classmethod
    def load(cls, path: Path, password: str = None) -> 'Wallet':
        """Load wallet from file."""
        data = json.loads(path.read_text())
        
        keypair = KeyPair.from_private_key(bytes.fromhex(data['private_key']))
        return cls(
            name=data['name'],
            keypair=keypair,
            testnet=data.get('testnet', False)
        )
```

---

## Security Considerations

### Key Storage

```python
# NEVER store private keys in plaintext in production!
# Use:
# - Hardware security modules (HSM)
# - Encrypted key stores (AES-256-GCM)
# - OS keychain integration
# - Hardware wallets (Ledger/Trezor)
```

### Memory Protection

```python
# Clear sensitive data from memory
import ctypes

def secure_zero(data: bytes):
    """Overwrite bytes in memory."""
    ptr = ctypes.cast(id(data) + 32, ctypes.POINTER(ctypes.c_char))
    for i in range(len(data)):
        ptr[i] = b'\x00'
```

### Mnemonic Handling

- Never log mnemonics
- Clear from memory after use
- Verify checksum before restoring

---

## Validation Checklist

- [ ] Key generation is deterministic from seed
- [ ] Mnemonic produces same keys across implementations
- [ ] Addresses validate correctly
- [ ] Signatures verify with public key
- [ ] Transaction signing produces valid signatures
- [ ] UTXO tracking is accurate
- [ ] Balance calculation is correct
- [ ] Change outputs work properly

---

## Next Module

After completing `wallet/`, proceed to `analysis/` for statistical tools.

---

*Your keys, your coins.* 🌸
