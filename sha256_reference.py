"""
SHA-256 Reference Implementation

This is a pure Python implementation of SHA-256 based on NIST FIPS 180-4.
It provides a minimal but correct implementation suitable for educational purposes
and verification against standard test vectors.

Reference: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
"""

import struct


def _rightrotate(n, b):
    """Right rotate a 32-bit integer by b bits."""
    return ((n >> b) | (n << (32 - b))) & 0xffffffff


def _sha256(data):
    """
    Compute SHA-256 hash of data.
    Based on NIST FIPS 180-4.
    """
    # SHA-256 constants
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # Ensure data is bytes
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Pre-processing: adding padding bits
    msg_len = len(data) * 8  # length in bits
    msg = bytearray(data)
    msg.append(0x80)  # append bit '1' followed by zeros (as byte 0x80)
    
    # Append zeros until message length ≡ 448 (mod 512)
    while (len(msg) * 8) % 512 != 448:
        msg.append(0x00)
    
    # Append original message length as 64-bit big-endian integer
    msg.extend(struct.pack('>Q', msg_len))
    
    # Process the message in 512-bit chunks
    for chunk_start in range(0, len(msg), 64):
        chunk = msg[chunk_start:chunk_start + 64]
        
        # Break chunk into 16 32-bit big-endian words
        w = list(struct.unpack('>16I', chunk))
        
        # Extend w to 64 words
        for i in range(16, 64):
            s0 = _rightrotate(w[i-15], 7) ^ _rightrotate(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = _rightrotate(w[i-2], 17) ^ _rightrotate(w[i-2], 19) ^ (w[i-2] >> 10)
            w.append((w[i-16] + s0 + w[i-7] + s1) & 0xffffffff)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h_val = h
        
        # Main compression loop
        for i in range(64):
            S1 = _rightrotate(e, 6) ^ _rightrotate(e, 11) ^ _rightrotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h_val + S1 + ch + K[i] + w[i]) & 0xffffffff
            S0 = _rightrotate(a, 2) ^ _rightrotate(a, 13) ^ _rightrotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff
            
            h_val = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff
        
        # Add compressed chunk to hash values
        h[0] = (h[0] + a) & 0xffffffff
        h[1] = (h[1] + b) & 0xffffffff
        h[2] = (h[2] + c) & 0xffffffff
        h[3] = (h[3] + d) & 0xffffffff
        h[4] = (h[4] + e) & 0xffffffff
        h[5] = (h[5] + f) & 0xffffffff
        h[6] = (h[6] + g) & 0xffffffff
        h[7] = (h[7] + h_val) & 0xffffffff
    
    # Produce the final hash value as a 256-bit number
    return ''.join(f'{x:08x}' for x in h)


def sha256(data=b''):
    """Compute SHA-256 hash of data."""
    return _sha256(data)


if __name__ == '__main__':
    # Test vectors from NIST FIPS 180-4
    test_vectors = [
        (b'', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
        (b'abc', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'),
        (b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
         '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1'),
    ]
    
    print("SHA-256 Test Vectors (NIST FIPS 180-4):")
    print("=" * 80)
    
    all_pass = True
    for data, expected in test_vectors:
        result = sha256(data)
        passed = result == expected
        all_pass = all_pass and passed
        status = "PASS" if passed else "FAIL"
        print(f"[{status}]")
        print(f"  Input:    {repr(data)}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        print()
    
    print("=" * 80)
    print(f"Overall: {'All tests passed!' if all_pass else 'Some tests failed!'}")
