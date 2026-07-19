#!/usr/bin/env python3
"""
================================================================================
PROJECT 2: BASIC ENCRYPTION & DECRYPTION TOOLKIT
Cyber Security Internship Task

Goal:
    Implement encryption and decryption techniques that demonstrate core
    cryptography concepts, logic building, and data protection basics.

Key Requirements Covered:
    1. Encrypt user text using a basic logic (Caesar cipher)
    2. Decrypt the encrypted text
    3. Display both encrypted and decrypted output

Bonus additions (beyond the base requirement):
    - Vigenere and Atbash ciphers as alternative "or similar" techniques
    - Cryptanalysis module: brute-force + frequency-analysis cipher breaking
    - File encryption/decryption
    - Session logging with an exportable report (audit trail)

Module : encryption_decryption.py
================================================================================
"""

import os
import sys
from collections import Counter
from datetime import datetime


# ==============================================================================
# CIPHER IMPLEMENTATIONS
# ==============================================================================

class CaesarCipher:
    """
    Classical substitution cipher that shifts every letter of the alphabet
    by a fixed number of positions (the "key").

    Example (shift = 3): A -> D, B -> E, ..., Z -> C
    Non-alphabetic characters (spaces, digits, punctuation) pass through
    unchanged, and letter case is preserved.
    """

    ALPHABET_SIZE = 26

    def __init__(self, shift: int = 3):
        self.shift = shift % self.ALPHABET_SIZE

    def encrypt(self, plaintext: str, shift: int | None = None) -> str:
        """Encrypt plaintext using the Caesar cipher."""
        active_shift = self.shift if shift is None else shift % self.ALPHABET_SIZE
        return self._shift_text(plaintext, active_shift)

    def decrypt(self, ciphertext: str, shift: int | None = None) -> str:
        """Decrypt ciphertext that was Caesar-encrypted with the same shift."""
        active_shift = self.shift if shift is None else shift % self.ALPHABET_SIZE
        return self._shift_text(ciphertext, -active_shift)

    @staticmethod
    def _shift_text(text: str, shift: int) -> str:
        shifted = []
        for char in text:
            if char.isupper():
                shifted.append(chr((ord(char) - 65 + shift) % 26 + 65))
            elif char.islower():
                shifted.append(chr((ord(char) - 97 + shift) % 26 + 97))
            else:
                shifted.append(char)
        return "".join(shifted)

    def brute_force(self, ciphertext: str) -> dict[int, str]:
        """
        Cryptanalysis: try every one of the 26 possible shifts.
        Returns {shift: decrypted_text}. Demonstrates why a single-alphabet
        shift cipher is cryptographically weak - at most 25 keys need to be
        tried to guarantee a break, regardless of key length.
        """
        return {s: self._shift_text(ciphertext, -s) for s in range(self.ALPHABET_SIZE)}

    @staticmethod
    def frequency_analysis(ciphertext: str) -> int:
        """
        Cryptanalysis: estimate the shift key using English letter-frequency
        statistics, without brute forcing all keys or already knowing the key.
        Assumes the most frequent letter in the ciphertext maps to 'E', the
        most frequent letter in typical English text.
        """
        letters = [c.upper() for c in ciphertext if c.isalpha()]
        if not letters:
            return 0
        most_common_letter, _ = Counter(letters).most_common(1)[0]
        return (ord(most_common_letter) - ord("E")) % 26


class VigenereCipher:
    """
    Polyalphabetic substitution cipher that uses a repeating keyword to pick
    a different Caesar shift for every letter. This defeats simple frequency
    analysis, which is why it resisted cryptanalysis for centuries longer
    than the Caesar cipher.
    """

    def __init__(self, key: str):
        if not key or not key.isalpha():
            raise ValueError("Vigenere key must be a non-empty alphabetic string.")
        self.key = key.upper()

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using the keyword-driven Vigenere cipher."""
        return self._process(plaintext, direction=1)

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext that was Vigenere-encrypted with the same key."""
        return self._process(ciphertext, direction=-1)

    def _process(self, text: str, direction: int) -> str:
        result = []
        key_pos = 0
        key_len = len(self.key)
        for char in text:
            if char.isalpha():
                key_shift = ord(self.key[key_pos % key_len]) - 65
                shift = direction * key_shift
                base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - base + shift) % 26 + base))
                key_pos += 1
            else:
                result.append(char)
        return "".join(result)


class AtbashCipher:
    """
    Ancient substitution cipher (used in the Hebrew Bible) that mirrors the
    alphabet: A<->Z, B<->Y, C<->X, and so on. It is its own inverse, so the
    same function both encrypts and decrypts.
    """

    def encrypt(self, text: str) -> str:
        """Apply the Atbash mirror transform to encrypt text."""
        return self._mirror(text)

    def decrypt(self, text: str) -> str:
        """Apply the Atbash mirror transform to decrypt text (self-inverse)."""
        return self._mirror(text)

    @staticmethod
    def _mirror(text: str) -> str:
        mirrored = []
        for char in text:
            if char.isupper():
                mirrored.append(chr(90 - (ord(char) - 65)))
            elif char.islower():
                mirrored.append(chr(122 - (ord(char) - 97)))
            else:
                mirrored.append(char)
        return "".join(mirrored)


# ==============================================================================
# SESSION LOGGING (audit trail for a presentable, reviewable session)
# ==============================================================================

session_log = []


def log_operation(operation: str, cipher: str, text_in: str, text_out: str, extra: str = "") -> None:
    session_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operation,
        "cipher": cipher,
        "input": text_in,
        "output": text_out,
        "extra": extra,
    })


# ==============================================================================
# DISPLAY HELPERS
# ==============================================================================

def banner() -> None:
    print("\n" + "=" * 64)
    print("ENCRYPTION & DECRYPTION TOOLKIT".center(64))
    print("Project 2 - Cyber Security Internship".center(64))
    print("=" * 64)


def divider() -> None:
    print("-" * 64)


def show_result(pairs) -> None:
    """Pretty-print aligned label: value pairs."""
    width = max(len(label) for label, _ in pairs)
    for label, value in pairs:
        print(f"  {label.ljust(width)} : {value}")


# ==============================================================================
# MENU ACTIONS
# ==============================================================================

def action_caesar() -> None:
    divider()
    print("CAESAR CIPHER - Encrypt & Decrypt")
    divider()
    text = input("Enter text to encrypt: ").strip()
    if not text:
        print("No text entered.")
        return

    while True:
        raw = input("Enter shift key (1-25, default 3): ").strip()
        if raw == "":
            shift = 3
            break
        try:
            shift = int(raw)
            break
        except ValueError:
            print("Please enter a whole number.")

    cipher = CaesarCipher(shift)
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)

    divider()
    show_result([
        ("Original Text", text),
        ("Shift Key", cipher.shift),
        ("Encrypted Text", encrypted),
        ("Decrypted Text", decrypted),
        ("Round-trip OK?", "Yes" if decrypted == text else "No"),
    ])
    log_operation("Encrypt+Decrypt", "Caesar", text, encrypted, f"shift={cipher.shift}")


def action_vigenere() -> None:
    divider()
    print("VIGENERE CIPHER - Encrypt & Decrypt (keyword-based, bonus)")
    divider()
    text = input("Enter text to encrypt: ").strip()
    if not text:
        print("No text entered.")
        return

    key = input("Enter keyword (letters only, e.g. KEY): ").strip()
    try:
        cipher = VigenereCipher(key)
    except ValueError as err:
        print(f"Error: {err}")
        return

    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)

    divider()
    show_result([
        ("Original Text", text),
        ("Keyword", cipher.key),
        ("Encrypted Text", encrypted),
        ("Decrypted Text", decrypted),
        ("Round-trip OK?", "Yes" if decrypted == text else "No"),
    ])
    log_operation("Encrypt+Decrypt", "Vigenere", text, encrypted, f"key={cipher.key}")


def action_atbash() -> None:
    divider()
    print("ATBASH CIPHER - Encrypt & Decrypt (mirror alphabet, bonus)")
    divider()
    text = input("Enter text to encrypt: ").strip()
    if not text:
        print("No text entered.")
        return

    cipher = AtbashCipher()
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)

    divider()
    show_result([
        ("Original Text", text),
        ("Encrypted Text", encrypted),
        ("Decrypted Text", decrypted),
        ("Round-trip OK?", "Yes" if decrypted == text else "No"),
    ])
    log_operation("Encrypt+Decrypt", "Atbash", text, encrypted)


def action_crack() -> None:
    divider()
    print("CRACK A CAESAR-ENCRYPTED MESSAGE (Cryptanalysis)")
    divider()
    ciphertext = input("Enter Caesar-encrypted text to crack: ").strip()
    if not ciphertext:
        print("No text entered.")
        return

    cipher = CaesarCipher()
    guessed_shift = cipher.frequency_analysis(ciphertext)
    best_guess = cipher.decrypt(ciphertext, guessed_shift)
    print(f"\nFrequency analysis best guess -> shift = {guessed_shift}")
    print(f"Decrypted (best guess) : {best_guess}")

    show_all = input("\nShow all 26 possible shifts (brute force)? (y/n): ").strip().lower()
    if show_all == "y":
        divider()
        for shift, text in cipher.brute_force(ciphertext).items():
            marker = "   <-- likely match" if shift == guessed_shift else ""
            print(f"  Shift {shift:>2}: {text}{marker}")

    log_operation("Cryptanalysis", "Caesar", ciphertext, best_guess, f"guessed_shift={guessed_shift}")


def action_file() -> None:
    divider()
    print("ENCRYPT / DECRYPT A TEXT FILE (Caesar Cipher)")
    divider()
    path = input("Enter path to a .txt file: ").strip()
    if not os.path.isfile(path):
        print("File not found.")
        return

    mode = input("Encrypt or Decrypt this file? (e/d): ").strip().lower()
    if mode not in ("e", "d"):
        print("Please enter 'e' or 'd'.")
        return

    try:
        shift = int(input("Enter shift key: ").strip())
    except ValueError:
        print("Invalid shift key.")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    cipher = CaesarCipher(shift)
    processed = cipher.encrypt(content) if mode == "e" else cipher.decrypt(content)

    suffix = "_encrypted.txt" if mode == "e" else "_decrypted.txt"
    out_path = os.path.splitext(path)[0] + suffix
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(processed)

    print(f"\nDone. Output written to: {out_path}")
    log_operation("File " + ("Encrypt" if mode == "e" else "Decrypt"),
                  "Caesar", path, out_path, f"shift={shift}")


def export_report() -> str:
    filename = f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("ENCRYPTION & DECRYPTION TOOLKIT - SESSION REPORT\n")
        f.write("=" * 60 + "\n\n")
        for i, entry in enumerate(session_log, 1):
            f.write(f"{i}. [{entry['timestamp']}] {entry['operation']} ({entry['cipher']})\n")
            f.write(f"   Input : {entry['input']}\n")
            f.write(f"   Output: {entry['output']}\n")
            if entry["extra"]:
                f.write(f"   Info  : {entry['extra']}\n")
            f.write("\n")
    return filename


def action_history() -> None:
    divider()
    print("SESSION HISTORY")
    divider()
    if not session_log:
        print("No operations performed yet.")
        return

    for i, entry in enumerate(session_log, 1):
        print(f"{i}. [{entry['timestamp']}] {entry['operation']} ({entry['cipher']})")
        print(f"   Input : {entry['input']}")
        print(f"   Output: {entry['output']}")
        if entry["extra"]:
            print(f"   Info  : {entry['extra']}")

    export = input("\nExport this history to a report file? (y/n): ").strip().lower()
    if export == "y":
        filename = export_report()
        print(f"Report saved to: {filename}")


# ==============================================================================
# MAIN MENU
# ==============================================================================

MENU_OPTIONS = [
    ("1", "Caesar Cipher - Encrypt & Decrypt", action_caesar),
    ("2", "Vigenere Cipher - Encrypt & Decrypt (bonus)", action_vigenere),
    ("3", "Atbash Cipher - Encrypt & Decrypt (bonus)", action_atbash),
    ("4", "Crack a Caesar-encrypted message (cryptanalysis)", action_crack),
    ("5", "Encrypt/Decrypt a text file", action_file),
    ("6", "View session history / export report", action_history),
    ("0", "Exit", None),
]


def main() -> None:
    banner()
    actions = {key: fn for key, _, fn in MENU_OPTIONS}

    while True:
        print()
        for key, label, _ in MENU_OPTIONS:
            print(f"  [{key}] {label}")
        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("\nExiting. Stay secure!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSession ended.")
        sys.exit(0)
