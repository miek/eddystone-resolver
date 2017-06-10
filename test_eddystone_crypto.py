import binascii
import unittest
from eddystone_crypto import gen_eid

class TestEddystoneCrypto(unittest.TestCase):
    def test_eid(self):
        tests = [
            ['a2c873f26ebae374d9f7efbcd922ca1c', 9, 1258098495, 'ca8db2444f89ec78'],
            ['6e93678f9afa8214a4a4eadefa6743cd', 13, 2569247988, '3deb9e6836f38314'],
            ['e2d10c4ec66c53750fba51597193de2f', 9, 65536, '9d8ba7d1bd78b089'],
            ['ff13b262328beea97ac45aa14ac85c56', 15, 4294967295, 'a760539518d97522'],
            ['ef7593a5192c81eb79c0ee7c35d7440a', 2, 3721760299, 'eef8baae2fd4b815'],
            ['38a24ddc7ef73348035bef16d1931352', 6, 3897629132, 'ff3713dab2b86c72'],
            ['3c3f34117c7e49d984528d3ffa9adae3', 9, 1141546105, '55d55138cdcebf08'],
        ]
        for test in tests:
            self.assertEqual(
                gen_eid(binascii.unhexlify(test[0]), test[1], test[2]),
                binascii.unhexlify(test[3])
            )
