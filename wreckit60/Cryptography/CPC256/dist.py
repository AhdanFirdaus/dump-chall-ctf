#Soal ctf LLL pada CP256-1299, pemain diminta untuk memulihkan private key λ dari dua tanda tangan yang dihasilkan dengan nonce lemah.
# program berikut akan dijalankan oleh melalui nc pada server. pemain akan menerima dua pesan, dua tanda tangan, dan public key. tugas pemain adalah memulihkan λ.

from sage.all import *
import random
from hashlib import sha256
from secret import FLAG
from cpc import CubicPellCurve

def sha2_as_integer(message: str) -> int:
    return int(sha256(message.encode()).hexdigest(), 16)

def generate_signature(msg, lam, B):
    sigma = sha2_as_integer(msg)
    alpha = random.randint(1, 2**B) 
    s = alpha + sigma * lam
    alphaG = alpha * G
    return (s, alphaG, sigma)

#parameter
p = 2**256 - 1299
phi = p**2 + p + 1
a = 7
curve = CubicPellCurve(p, a)
G = curve.point(4, 2, 1)
G = (p+1) * G 

lam = randint(1, phi)
pub = lam * G

# ==== Dua Pesan Berbeda ====
B = 256
msg1 = "hello world"
msg2 = "cryptography is fun"

s1, alphaG1, sigma1 = generate_signature(msg1, lam, B)
s2, alphaG2, sigma2 = generate_signature(msg2, lam, B)

# ==== Output ====
print(f"Public key: {pub}")
print(f"Message 1: {msg1}")
print(f"Signature 1: (s1={s1}, R1={alphaG1}, sigma1={sigma1})")
print(f"Message 2: {msg2}")
print(f"Signature 2: (s2={s2}, R2={alphaG2}, sigma2={sigma2})")

while True:
    guess = input("Your guess for the private key λ (in decimal): ")
    try:
        guess = int(guess)
        if guess == lam:
            print(f"Correct! Here is your flag: {FLAG}")
            break
        else:
            print("Incorrect, try again.")
    except ValueError:
        print("Please enter a valid integer.")
