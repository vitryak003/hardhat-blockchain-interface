import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const addresses = JSON.parse(
  await readFile("ignition/deployments/chain-31337/deployed_addresses.json", "utf8"),
);
const address = addresses["CounterModule#Counter"];
assert.match(address, /^0x[0-9a-fA-F]{40}$/);

const response = await fetch("http://127.0.0.1:8545", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "eth_getCode",
    params: [address, "latest"],
  }),
});
assert.equal(response.ok, true);
const result = await response.json();
assert.equal(result.error, undefined);
assert.match(result.result, /^0x[0-9a-fA-F]+$/);
console.log(`Counter deployed at ${address}`);
