# Project 2: Basic Encryption & Decryption Toolkit

**Cyber Security Internship — Task 2**

## Goal

Implement a simple encryption and decryption technique that demonstrates
encryption concepts, logic building, and data protection basics.

## Requirements Covered

| Requirement | Where it's implemented |
|---|---|
| Encrypt user text using basic logic (Caesar cipher or similar) | `CaesarCipher.encrypt()` — menu option `1` |
| Decrypt the encrypted text | `CaesarCipher.decrypt()` — menu option `1` |
| Display both encrypted and decrypted output | Every menu action prints Original / Encrypted / Decrypted side by side, with a round-trip check |

## Beyond the base requirement

The brief says "Caesar cipher **or similar**," so the toolkit implements three
classical ciphers instead of one, plus the tools a security engineer would
actually reach for to evaluate them:

- **Caesar Cipher** — the required fixed-shift substitution cipher
- **Vigenère Cipher** (bonus) — keyword-based polyalphabetic cipher, much
  harder to break than Caesar
- **Atbash Cipher** (bonus) — alphabet-mirroring cipher, its own inverse
- **Cryptanalysis** — brute-force (all 26 shifts) and frequency-analysis
  attacks that *break* a Caesar-encrypted message without knowing the key
- **File encryption/decryption** — run the cipher over a `.txt` file, not
  just typed input
- **Session logging** — every operation is logged with a timestamp and can
  be exported to a report file, useful as an audit trail

## Files

```
encryption_decryption.py        # main program (ciphers + interactive menu)
test_encryption_decryption.py   # unit tests (18 tests, all passing)
README.md                       # this file
```

## How to Run

Requires Python 3.10+ (standard library only — no installs needed).

```bash
python3 encryption_decryption.py
```

You'll see a menu:

```
  [1] Caesar Cipher - Encrypt & Decrypt
  [2] Vigenere Cipher - Encrypt & Decrypt (bonus)
  [3] Atbash Cipher - Encrypt & Decrypt (bonus)
  [4] Crack a Caesar-encrypted message (cryptanalysis)
  [5] Encrypt/Decrypt a text file
  [6] View session history / export report
  [0] Exit
```

## How to Test

```bash
python3 -m unittest test_encryption_decryption.py -v
```

All 18 tests should pass — covering encryption/decryption round trips,
case and punctuation preservation, alphabet wraparound, key validation,
and cryptanalysis accuracy.

## Sample Run (option 1 — Caesar Cipher)

```
Enter text to encrypt: Hello World
Enter shift key (1-25, default 3): 3
----------------------------------------------------------------
  Original Text  : Hello World
  Shift Key      : 3
  Encrypted Text : Khoor Zruog
  Decrypted Text : Hello World
  Round-trip OK? : Yes
```

## Sample Run (option 4 — Cryptanalysis)

Feed it a Caesar-encrypted message and it will try to recover the key
*without being told the shift*:

```
Enter Caesar-encrypted text to crack: Estd td l nzyqtopyetlw tyepcylw xpxz...

Frequency analysis best guess -> shift = 11
Decrypted (best guess) : This is a confidential internal memo...
```

Frequency analysis works by assuming the most common letter in the
ciphertext maps to 'E' (the most common letter in English). It's reliable
on realistic-length text but can guess wrong on short phrases — which is
itself a useful lesson, so option 4 also offers to print **all 26 possible
shifts** so the correct plaintext can always be spotted by eye. This is
exactly how the Caesar cipher was broken historically: its keyspace is
small enough (only 25 non-trivial keys) that it offers no real resistance
to a determined attacker.

## Security Note (Data Protection Basics)

Caesar, Vigenère, and Atbash are **teaching ciphers**, not production
security:

- Caesar has only 25 possible keys — trivial to brute-force in milliseconds.
- Vigenère is stronger but still breakable via frequency analysis once the
  key length is discovered (Kasiski examination).
- Atbash has no key at all — the "encryption" is public knowledge.

None of these should ever be used to protect real sensitive data. Real-world
data protection relies on:

- **Symmetric encryption** — AES-256, with a securely generated and stored key
- **Asymmetric encryption** — RSA or ECC, for key exchange and digital signatures
- **Hashing** — SHA-256 or bcrypt/Argon2 for passwords, to verify integrity
  without storing the original data
- **Transport security** — TLS, so data isn't sent in plaintext over a network
- **Key management** — the hardest part in practice; an algorithm is only as
  secure as the protection around its key

This toolkit is a controlled demonstration of *why* classical ciphers fail —
the cryptanalysis feature (option 4) is, in effect, a working proof of that
weakness.

## Possible Future Enhancements

- Add AES (via `cryptography` library) as a "real" cipher alongside the
  classical ones, to contrast weak vs. modern encryption side by side
- `argparse` support for non-interactive/scriptable use
- Kasiski examination to auto-detect Vigenère key length
