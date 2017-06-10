import binascii
from Crypto.Cipher import AES

def get_byte(num, i):
    return (num >> (24 - i*8)) & 0xFF

def gen_tk(ik, counter):
    tk_data = bytes([
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0xFF,
        0, 0,
        get_byte(counter, 0),
        get_byte(counter, 1),
    ])
    tk = AES.new(ik, AES.MODE_ECB).encrypt(tk_data)
    return tk

def gen_eid(ik, k, counter):
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
    eid = AES.new(tk, AES.MODE_ECB).encrypt(eid_data)
    return eid
