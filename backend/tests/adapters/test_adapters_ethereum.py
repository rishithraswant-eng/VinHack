import pytest
from app.adapters.ethereum import EthereumAdapter

def test_ethereum_detect_address():
    adapter = EthereumAdapter()
    
    # Valid checksummed
    assert adapter.detect_address("0x71C7656EC7ab88b098defB751B7401B5f6d8976F") == True
    # Valid lower case (still a valid hex address, is_address accepts it)
    assert adapter.detect_address("0x71c7656ec7ab88b098defb751b7401b5f6d8976f") == True
    
    # Invalid lengths/characters
    assert adapter.detect_address("0x71C7656EC7ab88b098defB751B7401B5f6d8976") == False
    assert adapter.detect_address("0xG1C7656EC7ab88b098defB751B7401B5f6d8976F") == False
    assert adapter.detect_address("") == False

def test_ethereum_normalize():
    adapter = EthereumAdapter()
    
    # Normalizes to checksum
    assert adapter.normalize_to_canonical("0x71c7656ec7ab88b098defb751b7401b5f6d8976f") == "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    assert adapter.normalize_to_canonical("0x71C7656EC7ab88b098defB751B7401B5f6d8976F") == "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    
    with pytest.raises(ValueError):
        adapter.normalize_to_canonical("invalid")
