from flask import Flask, jsonify
from solana.rpc.api import Client
from solana.publickey import PublicKey

app = Flask(__name__)
client = Client("https://api.mainnet-beta.solana.com")

RENT_RETURN_SOL = 0.002

def load_wallets():
    with open("wallets.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def count_token_accounts(wallet):
    pubkey = PublicKey(wallet)
    resp = client.get_token_accounts_by_owner(
        pubkey,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}
    )
    return len(resp["result"]["value"])

@app.route("/")
def index():
    wallets = load_wallets()
    total_accounts = 0
    details = {}

    for w in wallets:
        count = count_token_accounts(w)
        details[w] = count
        total_accounts += count

    return jsonify({
        "wallets_checked": len(wallets),
        "total_accounts": total_accounts,
        "return_sol": total_accounts * RENT_RETURN_SOL,
        "details": details
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
