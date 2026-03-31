import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HELIUS_API_KEY")
if not API_KEY:
    raise ValueError("HELIUS_API_KEY not found in environment variables")

RPC = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

MAX_SIGNATURES = 3

headers = {
    "Content-Type": "application/json"
}
def get_signatures(address):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, {"limit": MAX_SIGNATURES}]
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

    try:        #增加异常处理
        r = requests.post(RPC, json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.Timeout:
        print(f"Timeout fetching transaction: {signature}")
        return None
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except ValueError as e:  # JSON decode error
        print(f"Invalid JSON response: {e}")
        return None

    data = r.json()

    if "result" not in data:
        print("error:", data)
        return None

    return data["result"]