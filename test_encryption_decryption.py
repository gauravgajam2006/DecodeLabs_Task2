"""
Unit tests for encryption_decryption.py

Run with:
    python3 -m unittest test_encryption_decryption.py -v
"""

import unittest

from encryption_decryption import CaesarCipher, VigenereCipher, AtbashCipher


class TestCaesarCipher(unittest.TestCase):

    def setUp(self):
        self.cipher = CaesarCipher(shift=3)

    def test_encrypt_basic(self):
        self.assertEqual(self.cipher.encrypt("ABC"), "DEF")

    def test_wraparound_at_end_of_alphabet(self):
        self.assertEqual(self.cipher.encrypt("XYZ"), "ABC")

    def test_decrypt_reverses_encrypt(self):
        text = "Attack at Dawn!"
        encrypted = self.cipher.encrypt(text)
        self.assertEqual(self.cipher.decrypt(encrypted), text)

    def test_preserves_case(self):
        self.assertEqual(self.cipher.encrypt("Hello"), "Khoor")

    def test_preserves_non_alphabetic_characters(self):
        self.assertEqual(self.cipher.encrypt("Room 101!"), "Urrp 101!")

    def test_negative_and_large_shifts_normalise_correctly(self):
        self.assertEqual(CaesarCipher(-3).shift, 23)
        self.assertEqual(CaesarCipher(29).shift, 3)

    def test_brute_force_contains_correct_plaintext(self):
        text = "MEET ME AT NOON"
        encrypted = self.cipher.encrypt(text)
        results = self.cipher.brute_force(encrypted)
        self.assertEqual(len(results), 26)
        self.assertIn(text, results.values())

    def test_frequency_analysis_recovers_shift_on_realistic_text(self):
        # Natural English prose (not a pangram) of realistic memo length -
        # long enough for 'E' to reliably be the most frequent letter.
        message = (
            "This is a confidential internal memo. All employees must "
            "complete the mandatory security training module before the "
            "end of this quarter. Please contact the security team if you "
            "have any questions regarding the training requirements or "
            "deadlines."
        )
        cipher = CaesarCipher(shift=11)
        encrypted = cipher.encrypt(message)
        guessed_shift = CaesarCipher.frequency_analysis(encrypted)
        self.assertEqual(guessed_shift, 11)
        self.assertEqual(cipher.decrypt(encrypted, guessed_shift), message)

    def test_frequency_analysis_empty_text_returns_zero(self):
        self.assertEqual(CaesarCipher.frequency_analysis(""), 0)
        self.assertEqual(CaesarCipher.frequency_analysis("1234 !!!"), 0)


class TestVigenereCipher(unittest.TestCase):

    def test_encrypt_matches_known_textbook_example(self):
        # Classic reference example: ATTACKATDAWN / LEMON -> LXFOPVEFRNHR
        cipher = VigenereCipher("LEMON")
        self.assertEqual(cipher.encrypt("ATTACKATDAWN"), "LXFOPVEFRNHR")

    def test_encrypt_decrypt_roundtrip(self):
        cipher = VigenereCipher("KEY")
        text = "Attack at Dawn"
        encrypted = cipher.encrypt(text)
        self.assertEqual(cipher.decrypt(encrypted), text)

    def test_preserves_non_alphabetic_characters(self):
        cipher = VigenereCipher("KEY")
        encrypted = cipher.encrypt("Hi, Team!")
        self.assertEqual(cipher.decrypt(encrypted), "Hi, Team!")

    def test_rejects_non_alphabetic_key(self):
        with self.assertRaises(ValueError):
            VigenereCipher("KE Y1")

    def test_rejects_empty_key(self):
        with self.assertRaises(ValueError):
            VigenereCipher("")


class TestAtbashCipher(unittest.TestCase):

    def setUp(self):
        self.cipher = AtbashCipher()

    def test_a_maps_to_z(self):
        self.assertEqual(self.cipher.encrypt("A"), "Z")

    def test_preserves_case_and_mirrors_correctly(self):
        self.assertEqual(self.cipher.encrypt("Hello"), "Svool")

    def test_is_self_inverse(self):
        text = "Hello World"
        encrypted = self.cipher.encrypt(text)
        self.assertEqual(self.cipher.decrypt(encrypted), text)

    def test_preserves_non_alphabetic_characters(self):
        self.assertEqual(self.cipher.encrypt("Room 101!"), "Illn 101!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
