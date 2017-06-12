import binascii
from Crypto.Cipher import AES
import hashlib
import hkdf
import nacl

def get_byte(num, i):
    return (num >> (24 - i*8)) & 0xFF

def compute_shared_secret(pub, priv):
    return nacl.bindings.crypto_scalarmult(pub, priv)

def compute_ik(shared_secret, service_public_key, beacon_public_key):
    salt = service_public_key + beacon_public_key
    prk = hkdf.hkdf_extract(salt, shared_secret, hash=hashlib.sha256)
    ik = hkdf.hkdf_expand(prk, b"", 32, hash=hashlib.sha256)[:16]
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
    return tk

def compute_eid(ik, k, counter):
    # Clear lower K bits
    counter = (counter >> k) << k
    tk = gen_tk(ik, counter)
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
