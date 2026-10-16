import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { network } from "hardhat";

describe("Counter", async () => {
  const { viem } = await network.connect();

  it("starts at zero", async () => {
    const counter = await viem.deployContract("Counter");
    assert.equal(await counter.read.x(), 0n);
  });

  it("increments by one", async () => {
    const counter = await viem.deployContract("Counter");
    await counter.write.inc();
    assert.equal(await counter.read.x(), 1n);
  });

  it("accumulates increments", async () => {
    const counter = await viem.deployContract("Counter");
    await counter.write.incBy([5n]);
    await counter.write.incBy([7n]);
    assert.equal(await counter.read.x(), 12n);
  });

  it("rejects zero without changing the value", async () => {
    const counter = await viem.deployContract("Counter");
    await counter.write.incBy([3n]);
    await assert.rejects(counter.write.incBy([0n]), /Increment must be positive/);
    assert.equal(await counter.read.x(), 3n);
  });

  it("emits the increment value", async () => {
    const counter = await viem.deployContract("Counter");
    const client = await viem.getPublicClient();
    const hash = await counter.write.incBy([9n]);
    const receipt = await client.waitForTransactionReceipt({ hash });
    const events = await client.getContractEvents({
      address: counter.address,
      abi: counter.abi,
      eventName: "Increment",
      fromBlock: receipt.blockNumber,
      toBlock: receipt.blockNumber,
      strict: true,
    });
    assert.equal(events.length, 1);
    assert.equal(events[0].args.by, 9n);
  });
});
