import pytest

from app.adapters.bitcoin import BitcoinAdapter


def test_bitcoin_detect_address():
    adapter = BitcoinAdapter()
    
    # Valid Base58 P2PKH
    assert adapter.detect_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == True
    # Valid Base58 P2SH
    assert adapter.detect_address("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") == True
    
    # Valid Bech32 P2WPKH
    assert adapter.detect_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == True
    # Valid Bech32m P2TR
    assert adapter.detect_address("bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297") == True
    
    # Invalid addresses
    assert adapter.detect_address("bc1invalid") == False
    assert adapter.detect_address("1InvalidBase58_O0I") == False
    assert adapter.detect_address("") == False
    assert adapter.detect_address("0x71C7656EC7ab88b098defB751B7401B5f6d8976F") == False

def test_bitcoin_normalize():
    adapter = BitcoinAdapter()
    
    # Base58 should remain case-sensitive
    assert adapter.normalize_to_canonical("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    
    # Bech32 should be lowercase
    assert adapter.normalize_to_canonical("BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4") == "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
    
    with pytest.raises(ValueError):
        adapter.normalize_to_canonical("invalid")
