import random

def create_mapping():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    mapping = {}
    for i in range(len(alphabet)):
        mapping[alphabet[i]] = shuffled[i]
    return mapping

def encrypt(text, mapping):
    result = ""
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result

alphabet_mapping = create_mapping()
text = input("Enter text to encrypt: ")
encrypted_text = encrypt(text, alphabet_mapping)

print("Original text:", text)
print("Encrypted text:", encrypted_text)