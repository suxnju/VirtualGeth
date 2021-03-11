from web3 import Web3

def keccak256(plain:str,is_hex:bool=False) -> str:
    if is_hex:
        return Web3.toHex(Web3.keccak(hexstr=plain)).lstrip("0x").ljust(64,"0")
    else:
        return Web3.toHex(Web3.keccak(text=plain)).lstrip("0x").ljust(64,"0")

if __name__ == "__main__":
    to_hash = "000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000007"
    # print(keccak256(to_hash))
    # print(Web3.toHex(Web3.keccak(hexstr=to_hash)))
    # print(Web3.toHex(Web3.keccak(text=to_hash)))

    print(
        Web3.toHex(Web3.keccak(hexstr="000000000000000000000000000000000000000000000000000000000000000a"+Web3.toHex(Web3.keccak(hexstr=to_hash)).lstrip("0x")))
    )