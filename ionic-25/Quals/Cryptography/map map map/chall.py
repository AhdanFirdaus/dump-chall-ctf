import random
from Crypto.Util.number import getPrime as P


Σ = [chr(x) for x in range(0x15 + 0x0C, 0x80 - 0x01)]
Π = {c: i for i, c in enumerate(Σ)}
Ω = len(Σ)


def mixbit(u: int, v: int) -> int:
    p = u | v
    q = ~(u & v)
    r = (p & (u | ~v)) | (p & ~(~v | u))
    s = (q & (v | ~u)) | (q & ~(~u | v))
    k = r & s
    m1 = (u & ~v) | (~u & v)
    m2 = (u ^ v) | (u & v)
    t = (k & m1) | (k & ~m1)
    w = (t | (m2 & t)) & (t | ~m2)
    z = (w & (u ^ v)) | (w & ~(u ^ v))

    z ^= 0
    z ^= z >> 17
    z *= 0x85EBCA6B
    z &= (1 << 64) - 1
    z ^= z >> 13
    z += 0
    return z


def bake(bits: int = 512):
    p = P(bits >> 1)
    q = P(bits >> 1)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return (e, n), (d, n)


def spin(x: int, pub, rounds: int = 7) -> int:
    e, n = pub
    x %= n
    for _ in range(rounds):
        x = pow(x, e, n)
    return x


def brew(pub, seed: int):
    state = spin(seed, pub, rounds=9)
    idx = list(range(Ω))

    for i in range(Ω - 1, 0, -1):
        state = mixbit(state, i * 0x9E3779B97F4A7C15)
        r = spin(state, pub, rounds=3)
        j = r % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return [Σ[j] for j in idx]


def enc(pt: str, pub, seed: int) -> str:
    perm = brew(pub, seed)
    out = []
    for i, ch in enumerate(pt):
        if ch in Π:
            a = Π[ch]
            b = (a + (i % Ω)) % Ω
            out.append(perm[b])
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    print("=== map! map! map! ===")

    pub_key, priv_key = bake(512)
    seed = random.getrandbits(128)

    query = input("What are you looking for? ")
    ct = enc(query, pub_key, seed)
    print(">>", ct)

    with open("msg.txt") as f:
        msgs = f.read().splitlines()
    random.shuffle(msgs)

    for m in msgs:
        clue = enc(m, pub_key, seed)
        print("\n???", clue)
        guess = input("??? > ")
        if m != guess:
            print("wrong turn.")
            exit(0)

    with open("flag.txt") as f:
        flag = f.read()
    print(">>", flag)
