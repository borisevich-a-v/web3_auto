from .chains import era
from web3 import Web3


def get_balance(web3: Web3, address: str, token: era.Tokens) -> float:
    if token is era.Tokens.ETH:
        return float(web3.eth.get_balance(address))

    if token in era.Tokens:
        token_adr = Web3.to_checksum_address(token.value)
        contract = web3.eth.contract(address=token_adr, abi=era.ABI.ERC20)
        balance = contract.functions.balanceOf(address).call()
        return float(balance)

    raise ValueError(f"Token {token} was not defined")
