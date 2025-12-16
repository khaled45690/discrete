# RSA Encryption and Decryption
# Public Key (n, e) = (3233, 17)
# Private Key (n, d) = (3233, 2753)

# RSA Parameters
n = 3233
e = 17  # Public exponent
d = 2753  # Private exponent

# Manual modular exponentiation: (base^exp) % mod
def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

# Convert letter to number (A=01, B=02, ..., Z=26, space=00)
def letter_to_number(letter):
    letter = letter.upper()
    if letter == ' ':
        return 0
    code = ord(letter)
    if 65 <= code <= 90:  # A-Z
        return code - 64  # A=1, B=2, ..., Z=26
    return 0  # For any other character, treat as space

# Convert number to letter (01=A, 02=B, ..., 26=Z, 00=space)
def number_to_letter(num):
    if num == 0:
        return ' '
    if 1 <= num <= 26:
        return chr(64 + num)  # A=65, so 64+1=A
    return '?'

# Encrypt message using RSA
def encrypt_message(message):
    print("\n" + "="*60)
    print("ENCRYPTION PROCESS")
    print("="*60)
    print(f"Original message: '{message}'")
    print(f"Public Key (n, e) = ({n}, {e})")
    print("\nStep-by-step encryption:")
    print("-" * 60)
    
    encrypted = []
    
    # Pad message to even length
    if len(message) % 2 != 0:
        message += ' '
        print(f"Padded message: '{message}' (added space for even length)")
    
    # Process two letters at a time
    for i in range(0, len(message), 2):
        letter1 = message[i]
        letter2 = message[i + 1]
        
        num1 = letter_to_number(letter1)
        num2 = letter_to_number(letter2)
        
        # Combine two letters: first_letter * 100 + second_letter
        m = num1 * 100 + num2
        
        # Encrypt: c = m^e mod n
        c = mod_pow(m, e, n)
        encrypted.append(c)
        
        print(f"\nPair {i//2 + 1}: '{letter1}{letter2}'")
        print(f"  {letter1} -> {num1:02d}, {letter2} -> {num2:02d}")
        print(f"  Combined value m = {num1} * 100 + {num2} = {m}")
        print(f"  Encrypted: c = {m}^{e} mod {n} = {c}")
    
    print("\n" + "-" * 60)
    print(f"Encrypted blocks: {encrypted}")
    print("="*60)
    
    return encrypted

# Decrypt message using RSA
def decrypt_message(encrypted_blocks):
    print("\n" + "="*60)
    print("DECRYPTION PROCESS")
    print("="*60)
    print(f"Encrypted blocks: {encrypted_blocks}")
    print(f"Private Key (n, d) = ({n}, {d})")
    print("\nStep-by-step decryption:")
    print("-" * 60)
    
    decrypted = ""
    
    for idx, c in enumerate(encrypted_blocks):
        # Decrypt: m = c^d mod n
        m = mod_pow(c, d, n)
        
        # Split back into two letters
        letter1_num = m // 100
        letter2_num = m % 100
        
        letter1 = number_to_letter(letter1_num)
        letter2 = number_to_letter(letter2_num)
        
        decrypted += letter1 + letter2
        
        print(f"\nBlock {idx + 1}: {c}")
        print(f"  Decrypted: m = {c}^{d} mod {n} = {m}")
        print(f"  Split: {m} = {letter1_num} * 100 + {letter2_num}")
        print(f"  {letter1_num:02d} -> '{letter1}', {letter2_num:02d} -> '{letter2}'")
        print(f"  Pair: '{letter1}{letter2}'")
    
    decrypted = decrypted.strip()
    print("\n" + "-" * 60)
    print(f"Decrypted message: '{decrypted}'")
    print("="*60)
    
    return decrypted

# Main program
if __name__ == "__main__":
    print("\n" + "="*60)
    print("RSA ENCRYPTION/DECRYPTION DEMONSTRATION")
    print("="*60)
    print("Mapping: A=01, B=02, C=03, ..., Z=26, Space=00")
    print("Processing: Two letters at a time")
    print("="*60)
    
    # Get input from user
    message = input("\nEnter message to encrypt: ")
    
    # Encryption
    encrypted_blocks = encrypt_message(message)
    
    # Decryption
    decrypted_message = decrypt_message(encrypted_blocks)
    
    # Verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    print(f"Original:  '{message.upper()}'")
    print(f"Decrypted: '{decrypted_message}'")
    print(f"Match: {message.upper().strip() == decrypted_message}")
    print("="*60 + "\n")
