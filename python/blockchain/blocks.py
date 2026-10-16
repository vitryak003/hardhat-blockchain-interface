import argparse
import json
import sys
from datetime import datetime, timezone

from web3 import Web3


def connect(rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 10}))
    if not web3.is_connected():
        raise ConnectionError("Cannot connect to Hardhat. Start npx hardhat node.")
    return web3


def get_all_blocks(web3):
    latest_number = web3.eth.block_number
    return [
        web3.eth.get_block(number, full_transactions=True)
        for number in range(latest_number + 1)
    ]


def main():
    parser = argparse.ArgumentParser(description="Print all blocks from Hardhat.")
    parser.add_argument("--rpc-url", default="http://127.0.0.1:8545")
    args = parser.parse_args()

    try:
        web3 = connect(args.rpc_url)
        blocks = get_all_blocks(web3)
        print(f"Chain ID: {web3.eth.chain_id}")
        print(f"Latest block: {blocks[-1]['number']}")
        print(f"Total blocks: {len(blocks)}")

        for block in blocks:
            timestamp = datetime.fromtimestamp(block["timestamp"], timezone.utc)
            print("=" * 72)
            print(f"Block #{block['number']}")
            print(f"Time (UTC): {timestamp.isoformat()}")
            print(f"Transactions: {len(block['transactions'])}")
            print(json.dumps(json.loads(Web3.to_json(block)), indent=2))
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
