# Santiago Saldaña Subías - A01708446
# Diego Perea León - A01708350

# Function to make sure the user is returning a valid whole number without text.
def force_answer_int(options, question):

    # We iterate until the user gives a valid answer.
    while True:

        # We showcase the options (if any) and ask for an input.
        print(options, end='')
        answer = input("\n" + question + ": ")

        # We use a try except block to catch any ValueErrors that might arise from converting
        # the user input if they provided a string.
        try:

            # We do not want decimals.
            if '.' in answer:
                print("\nError. Please use a whole number (no decimals).")

                # We continue the loop.
                continue
            
            # We remove any spaces for ease of conversion and try to convert the input to int.
            answer = int(answer.replace(' ', ''))

            # If successfull (no ValueError), we can return the answer and end the loop.
            return answer
            
        except ValueError:

            # If not successfull we try once again and rerun the loop.
            print("\nError. Please select a number.")


# Function to format the answer for ease of use.
def force_answer_str(question):

    # We iterate until a given answer is given.
    while True:

        # We ask for an input, and remove any spaces at the front, back (strip).
        # We also make the string uppercase for consistency.
        answer = input("\n" + question + ": ").strip().upper()

        # If we have an answer, we return the answer and end the loop.
        if answer:
            return answer
        else:
            # If we don't have an answer, we continue looping.
            print("\nError. Input cannot be empty.")


# Function that performs the repeating key XOR mathematical operation.
def xor_repeating_key(data_bytes, key_bytes):

    # We create an empty list of bytes to store the answer into.
    result = bytearray()
    
    # We loop through each byte in the data_bytes. i is the index and byte the current letter.
    for i, byte in enumerate(data_bytes):

        # We divide the current position i by the length of the key and take the remainder.
        # This loops the key over the message.
        current_key_byte = key_bytes[i % len(key_bytes)]

        # We append the XOR calculation to the result list.
        result.append(byte ^ current_key_byte)
        
    # We return the resulting bytes.
    return result


# Function to encrypt any message using XOR with a repeating key.
def encrypt_xor(plaintext, key):

    # We convert the plaintext string and key into bytes.
    data_bytes = plaintext.encode('utf-8')
    key_bytes = key.encode('utf-8')
    
    # We pass the bytes and the key to our core XOR function.
    encrypted_bytes = xor_repeating_key(data_bytes, key_bytes)

    # We convert the resulting bytes into an uppercase hexadecimal string.
    hex_result = encrypted_bytes.hex().upper()

    # We add a space every 2 characters for readability and return it.
    return ' '.join(hex_result[i:i+2] for i in range(0, len(hex_result), 2))


# Function to decrypt a hexadecimal message using XOR and a repeating key.
def decrypt_xor(cyphered_hex, key):

    # We use a try except block to catch invalid hexadecimal formats.
    try:
        # We remove any spaces the user might have inputted in the hex string.
        clean_hex = cyphered_hex.replace(" ", "")

        # We convert the clean hex string into bytes.
        data_bytes = bytes.fromhex(clean_hex)
        key_bytes = key.encode('utf-8')

        # We pass the bytes and the key to our core XOR function to decrypt.
        decrypted_bytes = xor_repeating_key(data_bytes, key_bytes)

        # We convert the decrypted bytes back to readable text, ignoring decoding errors.
        return decrypted_bytes.decode('utf-8', errors='ignore')

    except ValueError:

        # We return None if the user provided invalid hexadecimal characters.
        return None


# Function to brute force an XOR cipher testing all possible ASCII characters.
def xor_brute_force():

    # We ask the user what format their ciphertext is in.
    format_choice = force_answer_int("\n1) Hexadecimal\n2) Binary\n3) Decimal\n", "Select Ciphertext Format (1-3)")
    cyphered_text = input("\nEnter the cyphered message (with spaces): ").strip()

    # We convert the input into a list of strings separated by spaces.
    blocks = cyphered_text.split()
    cyphered_bytes = bytearray()

    # We use a try except block to catch conversion errors.
    try:
        # We convert the blocks into bytes based on the selected format.
        if format_choice == 1:

            # HEX
            for block in blocks:
                cyphered_bytes.append(int(block, 16))
        elif format_choice == 2:

            # BINARY
            for block in blocks:
                cyphered_bytes.append(int(block, 2))
        elif format_choice == 3:

            # DECIMAL
            for block in blocks:
                cyphered_bytes.append(int(block, 10))

        else:
            print("\nError. Invalid format selection.")
            return

    except ValueError:
        print("\nError. The message contains invalid characters for the selected format.")
        return

    print("\nBrute Force Results:")
    
    # We test all possible ASCII values (0 to 255).
    for key_val in range(256):
        
        # We create the key as a single byte.
        key_byte = bytes([key_val])
        
        # We pass the cyphered bytes and our single byte key to the core function.
        decyphered_bytes = xor_repeating_key(cyphered_bytes, key_byte)
        
        # We convert the resulting bytes into readable text, ignoring errors.
        output = decyphered_bytes.decode('ascii', errors='ignore')
        
        # We identify the character used (if readable).
        character_key = chr(key_val) if 32 <= key_val <= 126 else '.'
        
        # We print all results.
        print(f"Key: {key_val:03} (ASCII: '{character_key}') | Result: {output}")


# Function to encode using Vigenere (same as lab 3).
def encode_vigenere(message, key):
    
    # We ensure uppercase.
    message = message.upper()
    key = key.upper()
    
    encoded_message = ""
    index_key = 0
    
    # We iterate through the characters in the message.
    for character in message:

        # We only encode letters.
        if character.isalpha():

            # We turn the letter into its value from 0 to 25.
            value_message = ord(character) - ord('A')
            key_value = ord(key[index_key % len(key)]) - ord('A')
            
            # We apply the formula to encode Vigenère: (M + K) mod 26
            cyphered_value = (value_message + key_value) % 26
            
            # We convert it to a letter and add it to the final message.
            encoded_message += chr(cyphered_value + ord('A'))
            
            # We advance to the next character in the message.
            index_key += 1
        else:
            # If it is a symbol or space, we add it directly.
            encoded_message += character
            
    return encoded_message


# Function to handle OTP (One Time Pad) encryption (message and key length must match).
def otp_encrypt():

    # We iterate until the user gives a valid key length.
    while True:
        message = force_answer_str("Message to Encode")
        key = force_answer_str("Key")

        # We must check that the message and the key have the exact same length for OTP.
        # We remove spaces to check actual character length.
        clean_msg = message.replace(" ", "")
        clean_key = key.replace(" ", "")

        if len(clean_msg) == len(clean_key):

            # If lengths match, we break the loop and continue.
            break

        else:
            # If they don't match, we display an error and run the loop again.
            print(f"\nError. Message length ({len(clean_msg)}) and Key length ({len(clean_key)}) must be exactly the same for OTP.")

    # We ask the user which OTP cipher they wish to use.
    choice = force_answer_int("\n1) Vigenère OTP\n2) XOR OTP\n", "Select Cipher (1-2)")

    if choice == 1:

        # Vigenere encoder.
        output = encode_vigenere(message, key)
        print(f"\nEncoded OTP (Vigenere): {output}")

    elif choice == 2:

        # XOR encoder.
        output = encrypt_xor(message, key)
        print(f"\nEncoded OTP (XOR Hex): {output}")
        
    else:
        print("\nError. Invalid selection.")


# Function to help decypher two messages cyphered in the same OTP key.
def crib_drag_tool():

    print("As seen in class, if we two cyphered OTP messages that have the same key and " \
    "\nXOR them together with (C1 ^ C2) which equals (M1 ^ M2) we can try to guess words to"
    "\nsee if english text appears.")

    # We ask for the two ciphertexts.
    c1_hex = input("\nCiphertext 1 (Hex): ").replace(" ", "")
    c2_hex = input("\nCiphertext 2 (Hex): ").replace(" ", "")

    # We use a try except block to convert hex.
    try:
        c1_bytes = bytes.fromhex(c1_hex)
        c2_bytes = bytes.fromhex(c2_hex)

    except ValueError:
        print("\nError. Invalid hexadecimal format.")
        return

    # We ensure they are the same length for analysis.
    min_len = min(len(c1_bytes), len(c2_bytes))
    
    # We XOR C1 and C2 together.
    combined_xor = bytearray()
    for i in range(min_len):
        combined_xor.append(c1_bytes[i] ^ c2_bytes[i])

    # We loop infinitely so the user can try to 'guess' possible words.
    while True:
        guess = input("\nEnter a word to guess ('EXIT' or 'QUIT' to quit): ").upper()

        if guess == 'EXIT' or guess == 'QUIT':
            break

        guess_bytes = guess.encode('utf-8')

        print(f"\nUsing {guess}:")

        # We 'slide' the guessed word across the XOR string.
        for i in range(len(combined_xor) - len(guess_bytes) + 1):
            
            # We isolate the chunk of the combined string.
            chunk = combined_xor[i:i+len(guess_bytes)]
            
            # We apply XOR the chunk with our guess.
            result = xor_repeating_key(chunk, guess_bytes)
            
            # We decode and print the result.
            text_result = result.decode('ascii', errors='ignore')
            print(f"Position {i:02}: {text_result}")


# Main loop of the program.
def main():
    
    # We print the menu text.
    print("\n==========================================================\n" \
    "            Welcome to the XOR-OTP Software"
    "\n==========================================================")

    # We will repeat this loop until the user chooses to terminate the program.
    while True:
        
        # We ask them what type of conversion they wish to do.
        print("\nSelect what you wish to do.")
        
        menu_options = "\n1) Encode XOR\n2) Decode XOR\n3) Brute Force XOR\n4) Encode OTP\n5) Crib Drag (Message Reuse)\n6) Quit\n"
        answer = force_answer_int(menu_options, "Selection (1-6)")
        
        # If the answer is within our valid functional range, we group the code...
        if answer >= 1 and answer <= 5:

            if answer == 1:

                # We ask the user for the message and the key using our force functions.
                message = force_answer_str("Message to Encode")
                key = force_answer_str("Key")
                output = encrypt_xor(message, key)

                print(f"\nEncoded Message (Hex): {output}")

            elif answer == 2:

                # We ask the user for the hex ciphertext and the key.
                cyphered_message = force_answer_str("Hexadecimal Message to Decode")
                key = force_answer_str("Key")
                result = decrypt_xor(cyphered_message, key)

                if result is not None:
                    print(f"\nDecoded Message: {result}")
                else:
                    print("\nError. The cyphered message must be in valid hexadecimal format.")

            elif answer == 3:

                # We call the Brute Force function.
                xor_brute_force()

            elif answer == 4:

                # We call the OTP function.
                otp_encrypt()

            elif answer == 5:

                # We call the Crib Dragging tool for message reuse.
                crib_drag_tool()
            
            # We place an input so the menu does not appear suddenly.
            input("\nPress Enter to Continue...")   

        elif answer == 6:

            # We terminate the main loop and thus end the program.
            print("\nThanks for using the program.")
            break

        else:

            # The user selected an int out of range.
            print("\nError. Please select a valid option.")


# We check if this is being executed in main.
if __name__ == '__main__':

    # We use a try and except block to catch any execution terminations from the IDE to prevent
    # an error message from appearing.
    try:
        main()
        
    except KeyboardInterrupt:

        # The program ended.
        print("\nThanks for using the program.")
