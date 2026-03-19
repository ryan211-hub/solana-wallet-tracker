import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HELIUS_API_KEY")

RPC = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"


headers = {
    "Content-Type": "application/json"
}
def get_signatures(address):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, {"limit": 10}]
    }

    try:

        response = requests.post(
            RPC,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        response.raise_for_status()

        return response.json()["result"]

    except Exception as e:

        print("RPC request failed:", e)
        return []


def get_transaction(signature):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            signature,
            {
                "encoding": "json",
                "maxSupportedTransactionVersion": 0
            }
        ]
    }

    r = requests.post(RPC, json=payload)

    data = r.json()

    if "result" not in data:
        print("error:", data)
        return None

    return data["result"]