# 🔐 Basic Encryption & Decryption Toolkit

A Python-based educational cryptography toolkit that demonstrates classical encryption and decryption techniques, basic cryptanalysis, file processing, and session auditing.

Built as **Project 2 of a Cyber Security Internship**, this project focuses on understanding the fundamental concepts behind substitution ciphers, encryption/decryption workflows, cryptanalysis, and basic data protection logic.

> ⚠️ **Educational Disclaimer:** The ciphers implemented in this project are classical cryptographic techniques and are **not suitable for protecting sensitive or production data**. Modern applications should use established cryptographic standards and libraries such as AES or ChaCha20.

---

## 📌 Project Overview

The **Basic Encryption & Decryption Toolkit** provides an interactive command-line interface for encrypting and decrypting text using multiple classical cipher algorithms.

The project includes:

* Caesar Cipher
* Vigenère Cipher
* Atbash Cipher
* Caesar Cipher brute-force analysis
* Frequency-analysis-based cryptanalysis
* Text file encryption and decryption
* Session history tracking
* Exportable session reports
* Automated unit testing

The project goes beyond the basic requirement of implementing a single encryption technique by combining multiple classical cryptography concepts into one structured toolkit.

---

## ✨ Features

### 🔄 Caesar Cipher

A substitution cipher that shifts letters by a configurable number of positions.

**Example:**

```text
Plaintext : ABC XYZ
Shift     : 3
Encrypted : DEF ABC
```

Features include:

* Custom shift keys
* Automatic shift normalization
* Negative shift support
* Large shift support
* Case preservation
* Preservation of spaces, digits, and punctuation
* Encryption and decryption support

---

### 🔑 Vigenère Cipher

A keyword-based polyalphabetic substitution cipher.

**Example:**

```text
Plaintext : ATTACKATDAWN
Key       : LEMON
Ciphertext: LXFOPVEFRNHR
```

Features include:

* Custom alphabetic keywords
* Case preservation
* Non-alphabetic character preservation
* Input validation
* Encryption and decryption support

---

### 🔁 Atbash Cipher

A mirror substitution cipher that reverses the alphabet.

```text
A ↔ Z
B ↔ Y
C ↔ X
```

**Example:**

```text
Plaintext : Hello
Encrypted : Svool
```

Because Atbash is self-inverse, the same transformation can be used for both encryption and decryption.

---

### 🧠 Caesar Cipher Cryptanalysis

The toolkit includes basic methods for analyzing Caesar-encrypted messages.

#### Brute-Force Analysis

Attempts all 26 possible shifts and returns every possible decrypted result.

```text
Shift 0  → ...
Shift 1  → ...
Shift 2  → ...
...
Shift 25 → ...
```

This demonstrates why Caesar cipher is cryptographically weak: its keyspace is extremely small.

#### Frequency Analysis

Attempts to estimate the Caesar shift by analyzing letter frequencies and assuming that the most frequent ciphertext letter corresponds to the commonly occurring English letter `E`.

> Frequency analysis is statistical and may not always produce the correct result, especially with short or unusual text.

---

### 📄 Text File Encryption & Decryption

The toolkit can process `.txt` files using the Caesar cipher.

Supported operations:

* Encrypt text files
* Decrypt encrypted text files
* Automatically generate output filenames
* Preserve UTF-8 text encoding

Example:

```text
input.txt
    ↓
input_encrypted.txt
    ↓
input_decrypted.txt
```

---

### 📋 Session History & Audit Logging

Every completed operation can be recorded in an in-memory session log.

Each log entry includes:

* Timestamp
* Operation performed
* Cipher used
* Input data
* Output data
* Additional information such as shift or key

Session history can also be exported as a timestamped text report.

Example:

```text
session_report_20260719_213000.txt
```

This demonstrates the concept of maintaining a basic audit trail for security-related operations.

---

## 🖥️ Interactive CLI

The application provides a menu-driven command-line interface.

```text
================================================
          ENCRYPTION & DECRYPTION TOOLKIT
        Project 2 - Cyber Security Internship
================================================

[1] Caesar Cipher - Encrypt & Decrypt
[2] Vigenere Cipher - Encrypt & Decrypt
[3] Atbash Cipher - Encrypt & Decrypt
[4] Crack a Caesar-encrypted message
[5] Encrypt/Decrypt a text file
[6] View session history / export report
[0] Exit
```

---

## 🧪 Unit Testing

The project includes automated unit tests covering the major cipher implementations.

The test suite verifies:

### Caesar Cipher

* Basic encryption
* Alphabet wraparound
* Encryption/decryption round trips
* Case preservation
* Non-alphabetic character preservation
* Negative and large shift normalization
* Brute-force key coverage
* Frequency analysis
* Empty input handling

### Vigenère Cipher

* Known textbook encryption example
* Encryption/decryption round trips
* Preservation of non-alphabetic characters
* Invalid key rejection
* Empty key rejection

### Atbash Cipher

* Alphabet mirroring
* Case preservation
* Self-inverse behavior
* Non-alphabetic character preservation

Run the tests with:

```bash
python3 -m unittest test_encryption_decryption.py -v
```

On Windows, you can also use:

```bash
python -m unittest test_encryption_decryption.py -v
```

---

## 📂 Project Structure

```text
.
├── encryption_decryption.py
├── test_encryption_decryption.py
└── README.md
```

After exporting a session report:

```text
.
├── encryption_decryption.py
├── test_encryption_decryption.py
├── README.md
└── session_report_YYYYMMDD_HHMMSS.txt
```

---

## ⚙️ Requirements

* Python 3.9 or newer
* No external dependencies required

The project uses only Python's standard library, including:

* `unittest`
* `os`
* `sys`
* `collections`
* `datetime`

---

## 🚀 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

Replace the repository URL with your actual GitHub repository URL.

---

### 2. Run the Application

```bash
python encryption_decryption.py
```

On some systems:

```bash
python3 encryption_decryption.py
```

---

### 3. Select an Operation

Use the interactive menu to:

1. Encrypt and decrypt text using Caesar Cipher
2. Encrypt and decrypt text using Vigenère Cipher
3. Encrypt and decrypt text using Atbash Cipher
4. Perform basic Caesar cipher cryptanalysis
5. Encrypt or decrypt a text file
6. View or export session history
7. Exit the application

---

## 🔐 Security Concepts Demonstrated

This project demonstrates several foundational cybersecurity concepts:

| Concept                   | Implementation                     |
| ------------------------- | ---------------------------------- |
| Substitution Ciphers      | Caesar and Atbash                  |
| Polyalphabetic Encryption | Vigenère Cipher                    |
| Key-Based Encryption      | Shift values and keywords          |
| Cryptanalysis             | Brute-force and frequency analysis |
| Data Transformation       | Text and file encryption           |
| Input Validation          | Vigenère key validation            |
| Audit Logging             | Session history                    |
| Automated Testing         | Python `unittest`                  |

---

## 📊 Security Limitations

This toolkit is designed for **education and experimentation**, not real-world security.

### Caesar Cipher

The Caesar cipher is extremely weak because:

* It has only 26 possible shifts
* Brute-force attacks are trivial
* Frequency analysis can often reveal the key

### Atbash Cipher

Atbash does not use a secret key and has a fixed transformation, making it unsuitable for secure communication.

### Vigenère Cipher

Although stronger than a simple Caesar cipher, classical Vigenère encryption is still vulnerable to cryptanalysis and should not be used to protect sensitive data.

### File Encryption

The file encryption feature uses the Caesar cipher and therefore should **not** be considered secure file encryption.

For real-world applications, use modern, peer-reviewed cryptographic algorithms and secure key-management practices.

---

## 🧠 What I Learned

Through this project, I explored:

* How classical substitution ciphers work
* The difference between encryption and decryption
* Key-based cryptographic transformations
* Alphabet wraparound logic
* Case-preserving text processing
* Brute-force cryptanalysis
* Frequency-analysis concepts
* File input/output operations
* Input validation
* Session auditing and logging
* Automated unit testing
* The limitations of classical cryptographic algorithms

---

## 🔮 Future Improvements

Potential future improvements include:

* Add modern encryption using AES-GCM
* Add secure password-based key derivation using PBKDF2 or Argon2
* Add authenticated encryption
* Add binary file support
* Add a graphical user interface
* Add JSON or CSV report export
* Add configurable logging levels
* Add more cryptanalysis techniques
* Add command-line arguments using `argparse`
* Add test coverage reporting
* Add CI testing with GitHub Actions

---

## ⚠️ Disclaimer

This project is intended strictly for **educational and cybersecurity learning purposes**.

The classical ciphers implemented in this toolkit are not suitable for protecting confidential, sensitive, or production data. Do not use this project as a replacement for modern cryptographic libraries or industry-standard encryption algorithms.

---

## 👨‍💻 Author

**Gaurav Gajam**

Computer Engineering Student | Cybersecurity & Software Development Enthusiast

---

## ⭐ Acknowledgements

This project was developed as part of a cybersecurity internship task focused on:

> **Basic Encryption & Decryption**

The implementation extends the original requirements by adding multiple classical ciphers, cryptanalysis capabilities, file processing, session auditing, and automated unit testing.
