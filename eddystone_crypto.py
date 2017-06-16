import binascii
from Crypto.Cipher import AES
import hashlib
import hkdf
import nacl.bindings

def get_byte(num, i):
    return (num >> (24 - i*8)) & 0xFF

def compute_shared_secret(priv, pub):
    print(b'pub: ' + binascii.hexlify(pub))
    print(b'priv: ' + binascii.hexlify(priv))
    secret = nacl.bindings.crypto_scalarmult(priv, pub)
    print(b'secret: ' + binascii.hexlify(secret))
    return secret

def compute_ik(shared_secret, service_public_key, beacon_public_key):
    salt = service_public_key + beacon_public_key
    prk = hkdf.hkdf_extract(salt, shared_secret, hash=hashlib.sha256)
    ik = hkdf.hkdf_expand(prk, b"", 32, hash=hashlib.sha256)[:16]
    print(b'shared: ' + binascii.hexlify(shared_secret))
    print(b'service: ' + binascii.hexlify(service_public_key))
    print(b'beacon: ' + binascii.hexlify(beacon_public_key))
    print(b'ik: ' + binascii.hexlify(ik))
    return ik

def compute_tk(ik, counter):
    tk_data = bytes([
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0xFF,
        0, 0,
        get_byte(counter, 0),
        get_byte(counter, 1),
    ])
    tk = AES.new(ik, AES.MODE_ECB).encrypt(tk_data)
    print(binascii.hexlify(tk))
    return tk

def compute_eid(ik, k, counter):
    # Clear lower K bits
    counter = (counter >> k) << k
    tk = compute_tk(ik, counter)
    eid_data = bytes([
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        k,
        get_byte(counter, 0),
        get_byte(counter, 1),
        get_byte(counter, 2),
        get_byte(counter, 3),
    ])
    eid = AES.new(tk, AES.MODE_ECB).encrypt(eid_data)[0:8]
    return eid
