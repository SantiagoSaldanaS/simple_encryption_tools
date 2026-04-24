
# Santiago Saldaña Subías - A01708446
# Diego Perea León - A01708350

from collections import Counter

# Frecuencias promedio de aparición de letras en el idioma español (A-Z)
spanish_frequencies = {
    'A': 12.53, 'B': 1.42, 'C': 4.68, 'D': 5.86, 'E': 13.68, 'F': 0.69, 'G': 1.01,
    'H': 0.70, 'I': 6.25, 'J': 0.44, 'K': 0.02, 'L': 4.97, 'M': 3.15, 'N': 6.71,
    'O': 8.68, 'P': 2.51, 'Q': 0.88, 'R': 6.87, 'S': 7.98, 'T': 4.63, 'U': 3.93,
    'V': 0.90, 'W': 0.01, 'X': 0.22, 'Y': 0.90, 'Z': 0.52
}

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

        # We ask for an input, and remove any spaces at the front, back (strip) or in-between (replace),
        # while also making the string uppercase.
        answer = input("\n" + question + ": ").strip().upper()

        # If we have an answer, we return the answer and end the loop.
        if answer:
            return answer
        else:
            # If we don't have an answer, we  continue looping.
            print("\nError. Input cannot be empty.")


# Function to ensure the user provides a valid Vigenère key (only letters).
def force_answer_key(question):

    # We iterate until a valid key is given.
    while True:

        # We ask for the input.
        answer = input("\n" + question + ": ")
        
        # We filter out spaces, numbers, and symbols, and make it uppercase.
        clean_key = "".join([c for c in answer if c.isalpha()]).upper()
        
        # If after filtering we have a valid string, we return it and end the loop.
        if clean_key:
            return clean_key
        else:
            # If it's empty (e.g., they only typed numbers or spaces), we show an error and continue the loop.
            print("\nError. The key must contain at least one valid letter.")


# Function to encode a message into vigenere using a key.
def encode_vigenere(message, key, decode=False):

    # decode is for when we want to use this functions to decode a vigenere cyphed message
    # by subtracting the key instead of adding it.
    
    # We make sure both the message and key are in uppercase.
    message = message.upper()
    key = key.upper()
    
    # We create variables for the output and index key.
    encoded_message = ""
    index_key = 0
    
    # We iterate through the characters in the message.
    for character in message:

        # We only encode letters (we ignore symbols, spaces, etc).
        if character.isalpha():

            # We turn the letter into its value from 0 to 25 (A=0, Z=25)
            value_message = ord(character) - ord('A')
            key_value = ord(key[index_key % len(key)]) - ord('A')
            
            # We check what exactly we want to do (encode / decode).
            if not decode:

                # We apply the formula to encode Vigenère: (M + K) mod 26
                cyphered_value = (value_message + key_value) % 26

            else:

                # We apply the formula to decode Vigenère: (M - K) mod 26
                cyphered_value = (value_message - key_value) % 26
            
            # We convert it to a letter and add it to the final message.
            encoded_message += chr(cyphered_value + ord('A'))
            
            # We advance to the next character in the message.
            index_key += 1
        else:
            # If it is a symbol or space, we add it directly.
            encoded_message += character
            
    return encoded_message


# Function to find the key length of a viginere encoded message using Kasiski.
def find_kasiski_length(message):
    
    # We will use kasiski's method to find the length of the key.
    lengths = []
    
    # We look for repeated sequences of three letters (trigrams).
    for i in range(len(message) - 2):
        trigram = message[i:i+3]
        for j in range(i + 3, len(message) - 2):
            if message[j:j+3] == trigram:
                lengths.append(j - i)
                
    if not lengths:

        # There were no discovered patterns.
        return 0
        

    # We find the factors of that length.
    factors = []
    for dist in lengths:

        # We test lengths from 2 to 20.
        for i in range(2, 21):
            if dist % i == 0:
                factors.append(i)
                
    # The most likely length will be the most common factor.
    if factors:
        likely_length = Counter(factors).most_common(1)[0][0]
        return likely_length
    
    return 0


# Function to find the viginere key of a message using its length and a frequency analysis.
def find_key(message, key_length):
    
    # We will analyse the frequencies of each block to find its key.
    found_key = ""
    
    # We separate the text into groups (columns) according to the length of the key.
    for i in range(key_length):
        block = message[i::key_length]
        
        # We initialize the two variables that will be used for testing each letter and
        # keeping track of the best score so far.
        best_letter = 'A'
        max_score = 0
        
        # We test the 26 possible letters of the block.
        for test_letter in range(26):
            current_score = 0
            
            # We decypher the block using the test key.
            decyphered_block = ""

            # We iterate throuch each character per block.
            for character in block:
                valor = (ord(character) - ord('A') - test_letter) % 26
                decyphered_block += chr(valor + ord('A'))
            
            # We count the letters and add the final score based on the language probabilities.
            count = Counter(decyphered_block)
            for character, amount in count.items():

                # We add the % of how common that decyphered letter is.
                current_score += amount * spanish_frequencies.get(character, 0)
                
            # We will keep the letter that generated the text that looks most like spanish.
            if current_score > max_score:
                max_score = current_score
                best_letter = chr(test_letter + ord('A'))
                
        found_key += best_letter
    
    # We return the best key.
    return found_key


# Function to crack (decoded) a vigenere encoded message.
def crack_vigenere(og_message):
    
    # We clean the text for the analysis.
    message = "".join([c for c in og_message.upper() if c.isalpha()])
    
    # We begin by using Kasiski to find the most likely length of the key.
    key_length = find_kasiski_length(message)
    
    # If the length was 0, the text was too short.
    if key_length == 0:

        print("\nThe text is too short for Kasiski.")
        return None
    
    
    # We realize a frequency analysis to find the best key.
    found_key = find_key(message, key_length)
    
    # We decode the message based on the best key found.
    found_message = encode_vigenere(og_message, found_key, decode=True)
    
    # We return the found key and message.
    return found_key, found_message


# Main loop of the program.
def main():
    
    # We print the menu text.
    print("\n==========================================================\n" \
    "              Welcome to the Vigénere software"
    "\n==========================================================")

    # We will repeat this loop until the user chooses to terminate the program.
    while True:
        
        # We ask them what type of conversion they wish to do.
        print("\n\nSelect what you wish to do.")
        
        # We force an integer answer into the variable answer.
        answer = force_answer_int("\n1) Encode Vigénere.\n2) Crack Vigénere.\n3) Quit\n", "Selection (1-3)")
        
        # If the answer involves converting a decimal, we group the code...
        if answer >= 1 and answer <= 2:

            if answer == 1:

                message = force_answer_str("Message to Encode")
                key = force_answer_key("Key")

                output = encode_vigenere(message, key)

                print(f"Encoded Message (using the key {key}): {output}")

            elif answer == 2:
                

                message = force_answer_str("Message to Decode")

                result = crack_vigenere(message)

                # We find out if the function was successfull.

                if result is not None:

                    # We can separate the key and decoded message
                    found_key, decoded_message = result
                    print(f"\nFound Key: {found_key}")
                    print(f"\nDecoded Message: {decoded_message}")
    
                else:
                    
                    # We could not find a result.
                    print("\nCould not be decoded or the text is too short to use Kasiski.")

            
            # We place an input so the menu does not appear suddenly.
            input("\nPress Enter to Continue...")   

        elif answer == 3:

            # We terminate the main loop and thus end the program.
            print("\nThanks for using the program.")
            break

        else:

            # The user selected an int out of range.
            print("\nError. Please select a valid option.")


# We check if this is being executed in main.
if __name__ == '__main__':

    # We use a try and except block to catch any execution terminations from the IDE to prevent
    # and error message from appearing.
    try:
        main()
        
    except KeyboardInterrupt:

        # The program ended.
        print("\nThanks for using the program.")
