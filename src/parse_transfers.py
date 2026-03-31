import base64

TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
SYSTEM_PROGRAM = "11111111111111111111111111111111"


# SPL Token 指令类型常量
INSTRUCTION_TRANSFER = 3            #Transfer 指令
INSTRUCTION_TRANSFER_CHECKED = 12   #TransferChecked 指令


def decode_token_transfer(data_base64):

    # 防御：必须是字符串
    if not isinstance(data_base64, str):
        return None

    # 防御：长度必须合理（base64最小长度）
    if len(data_base64) < 8:
        return None

    try:
        raw = base64.b64decode(data_base64)
    except Exception:
        return None

    if len(raw) < 9:
        return None

    instruction_type = raw[0]

    # 只处理 transfer
    if instruction_type not in [INSTRUCTION_TRANSFER, INSTRUCTION_TRANSFER_CHECKED]:
        return None

    amount = int.from_bytes(raw[1:9], "little")

    return amount


def get_pubkey(account):
    if isinstance(account, dict):
        return account.get("pubkey")
    return account


def parse_token_transfer(tx):

    result = []

    if not tx:
        print("parse_token_transfer(): result is None or empty")
        return result

    message = tx.get("transaction", {}).get("message", {})
    print("parse_token_transfer() : MESSAGE:", message )
    # 应该检查交易是否成功
    meta = tx.get("meta", {})
    if meta.get("err"):
        # 交易失败，可能不需要解析或标记为失败
        print("Transaction failed:", meta["err"])

    account_keys_raw = message.get("accountKeys", [])
    account_keys = [get_pubkey(a) for a in account_keys_raw]

    instructions = list(message.get("instructions", []))

    # inner instructions
    for inner_block in meta.get("innerInstructions", []):
        instructions.extend(inner_block.get("instructions", []))

    for ins in instructions:

        # ✅ parsed 优先
        if "parsed" in ins:
            parsed = ins["parsed"]

            if parsed.get("type") in ["transfer", "transferChecked"]:
                info = parsed.get("info", {})

                result.append({
                    "source": info.get("source"),
                    "destination": info.get("destination"),
                    "amount": int(info.get("amount", 0)),
                    "mint": info.get("mint")
                })
            continue

        # fallback: raw decode
        program_idx = ins.get("programIdIndex")
        if program_idx is None or program_idx >= len(account_keys):
            continue

        program_id = account_keys[program_idx]

        if program_id != TOKEN_PROGRAM:
            continue

        data = ins.get("data")
        if not data:
            continue

        amount = decode_token_transfer(data)

        if amount is None:
            continue

        accounts = ins.get("accounts", [])
        if len(accounts) < 2:
            continue

        result.append({
            "source": account_keys[accounts[0]],
            "destination": account_keys[accounts[1]],
            "amount": amount,
            "mint": None,
        })

    return result