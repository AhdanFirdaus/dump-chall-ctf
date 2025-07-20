#!/usr/bin/python2.7
from Crypto.Cipher import AES
import Crypto.Random as wrth
import hashlib

key = wrth.get_random_bytes(7)
enc = AES.new(hashlib.sha256(key).digest(), AES.MODE_ECB).encrypt("ACE{***********}")

print("key: %s" % hex(hash(key))[2:])
print("enc: %s" % enc.encode('hex'))
