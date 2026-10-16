import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blockchain.blocks import connect, get_all_blocks


class BlocksTests(unittest.TestCase):
    def test_all_blocks_and_parent_hashes(self):
        web3 = connect("http://127.0.0.1:8545")
        blocks = get_all_blocks(web3)
        self.assertEqual(len(blocks), web3.eth.block_number + 1)
        self.assertEqual(blocks[0]["number"], 0)
        for index, block in enumerate(blocks):
            self.assertEqual(block["number"], index)
            if index:
                self.assertEqual(block["parentHash"], blocks[index - 1]["hash"])
        self.assertGreaterEqual(len(blocks), 2)
        self.assertTrue(any(block["transactions"] for block in blocks))

    def test_terminal_output(self):
        script = Path(__file__).resolve().parents[1] / "blockchain" / "blocks.py"
        result = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        web3 = connect("http://127.0.0.1:8545")
        self.assertIn("Chain ID: 31337", result.stdout)
        self.assertIn(f"Total blocks: {web3.eth.block_number + 1}", result.stdout)
        for number in range(web3.eth.block_number + 1):
            self.assertIn(f"Block #{number}\n", result.stdout)

    def test_unavailable_node(self):
        script = Path(__file__).resolve().parents[1] / "blockchain" / "blocks.py"
        result = subprocess.run(
            [sys.executable, str(script), "--rpc-url", "http://127.0.0.1:1"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot connect to Hardhat", result.stderr)


if __name__ == "__main__":
    unittest.main()
