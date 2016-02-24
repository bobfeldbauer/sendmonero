# sendmonero.py
Basic commandline python utility to send Monero (XMR) via simplewallet with JSON-RPC.

Modified from https://github.com/moneroexamples/python-json-rpc, src/simplewallet_basic_rpc_call_04.py

Some exchanges or service providers require specifying payment ids, but otherwise you usually want a random one.

# Example usage: sendmonero.py <destination address> <amount> [payment id]

destination address and amount are required, payment id is optional and will be generated if it isn't provided.
