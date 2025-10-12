import os
import sys
import random
import secrets
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

with open("flag.txt") as f:
    FLAG = f.read()

seed = os.urandom(1024)
random.seed(seed)
SERVER_SALT = secrets.token_bytes(32)

BLOCK_SIZE = 16
MASTER_KEY = hashlib.sha256(SERVER_SALT + FLAG.encode()).digest()


def aes_encrypt(plaintext_bytes: bytes) -> bytes:
    iv = secrets.token_bytes(16)
    cipher = AES.new(MASTER_KEY, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext_bytes, BLOCK_SIZE))
    return iv + ct


def aes_decrypt(iv_ct_bytes: bytes) -> bytes:
    if len(iv_ct_bytes) < 16 or len(iv_ct_bytes) % 16 != 0:
        raise ValueError("ciphertext length invalid")
    iv = iv_ct_bytes[:16]
    ct = iv_ct_bytes[16:]
    cipher = AES.new(MASTER_KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt


def make_coupon_payload(name: str, coupon_id: int) -> bytes:
    return f"{name}|{hex(coupon_id)}".encode("utf-8")


def parse_coupon_payload(pt_bytes: bytes):
    try:
        s = pt_bytes.decode("utf-8", errors="ignore")
        if "|" not in s:
            return None, None
        name, coupon_hex = s.rsplit("|", 1)
        coupon_id = int(coupon_hex, 16)
        return name, coupon_id
    except Exception:
        return None, None


def generate_token(r: int, n: int, c: int, e: int, master_key: bytes):
    MASK32 = 0xFFFFFFFF

    r &= MASK32
    n &= MASK32
    c &= MASK32
    e &= MASK32
    x = (r ^ 0x9E3779B1) & MASK32

    t = (n ^ 0x85EBCA6B) & MASK32
    t = ((t << 7) | (t >> (32 - 7))) & MASK32
    x = (x + t) & MASK32

    u = (c * 0xC2B2AE35) & MASK32
    u = ((u << 13) | (u >> (32 - 13))) & MASK32
    x ^= u
    x = (x + e) & MASK32

    x ^= x >> 16
    x = (x * 0x7FEB352D) & MASK32
    x ^= x >> 15
    x = (x * 0x846CA68B) & MASK32
    x ^= x >> 16
    x &= MASK32

    km = 0
    for i, b in enumerate(master_key[:32]):
        km = (km + ((b ^ i) * 0x045D9F3B)) & MASK32
        sh = (i % 31) + 1
        km = ((km << sh) | (km >> (32 - sh))) & MASK32

    x ^= km
    x ^= km

    return x & MASK32


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    print("\x1b[1;36m")
    print(
        "██╗    ██╗██╗███████╗██╗  ██╗███╗   ███╗███████╗██╗     ██╗   ██╗ ██████╗██╗  ██╗"
    )
    print(
        "██║    ██║██║██╔════╝██║  ██║████╗ ████║██╔════╝██║     ██║   ██║██╔════╝██║ ██╔╝"
    )
    print(
        "██║ █╗ ██║██║███████╗███████║██╔████╔██║█████╗  ██║     ██║   ██║██║     █████╔╝ "
    )
    print(
        "██║███╗██║██║╚════██║██╔══██║██║╚██╔╝██║██╔══╝  ██║     ██║   ██║██║     ██╔═██╗ "
    )
    print(
        "╚███╔███╔╝██║███████║██║  ██║██║ ╚═╝ ██║███████╗███████╗╚██████╔╝╚██████╗██║  ██╗"
    )
    print(
        " ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝"
    )
    print("\x1b[0m")


def main():
    while True:
        clear()
        print_title()
        print("Welcome!")
        print("\nMenu:")
        print("  1) Get coupon")
        print("  2) Redeem coupon")
        print("  3) Exit")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            name = input("Enter your name: ").strip()
            if len(name) <= 5:
                print("Name must be longer than 5 characters. Press Enter to continue.")
                input()
                continue
            if not name:
                print("Name cannot be empty. Press Enter to continue.")
                input()
                continue

            r = random.getrandbits(32)
            n = random.getrandbits(32)
            c = random.getrandbits(32)
            e = random.getrandbits(32)

            coupon_id = generate_token(r, n, c, e, MASTER_KEY)
            payload = make_coupon_payload(name, coupon_id)
            code = aes_encrypt(payload).hex()

            print("\n--- Coupon Info ---")
            print(f"Name: {name}")
            print(f"Secret Key : {r}.{n}.{c}.{e}")
            print(f"Your Code : {code}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            ct_hex = input("Enter Your Code : ").strip()
            if not ct_hex:
                print("No input. Press Enter to continue.")
                input()
                continue
            try:
                iv_ct = bytes.fromhex(ct_hex)
            except Exception:
                print("Invalid hex. Press Enter to continue.")
                input()
                continue

            try:
                pt = aes_decrypt(iv_ct)
            except Exception as e:
                print(f"Decryption failed: {e}")
                input("Press Enter to continue.")
                continue

            name, coupon_id = parse_coupon_payload(pt)
            if name is None or coupon_id is None:
                print("Invalid coupon format after decrypt. Press Enter.")
                input()
                continue

            r = random.getrandbits(32)
            n = random.getrandbits(32)
            c = random.getrandbits(32)
            e = random.getrandbits(32)

            jar_pick = generate_token(r, n, c, e, MASTER_KEY)

            print("\n========== Redeem Result ==========")
            print(f"Name   : {name}")

            if jar_pick == coupon_id:
                print("[✓] SUCCESS\n")
                print("Congratulations! You have successfully redeemed the coupon.")
                print(f"Flag  : {FLAG}")
            else:
                print("[✗] FAILED\n")
                print("Nice Try")
            print("===================================")

            sys.exit(0)

        elif choice == "3":
            print("Bye.")
            sys.exit(0)
        else:
            print("Unknown option. Press Enter.")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited.")
