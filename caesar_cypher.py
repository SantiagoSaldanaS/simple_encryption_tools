
# Santiago Saldaña Subías - A01708446
# Diego Perea León - A01708350

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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


# Function to encode a message with a given key.
def cesar_encoder(message, key):

    # We prepare a variable to store the result.
    output = ''

    # We iterate for each character in the message to encode.
    for character in message:

        # If the letter is in the alphabet...
        if character in alphabet:

            # We shift it according to the key.
            shifted = (alphabet.index(character) + key) % len(alphabet)

            # We add it to the final output.
            output += alphabet[shifted]
        else:
            # If the character is not part of the alphabet (spaces, periods, etc.) we directly add it.
            output += character

    # We return the output (encoded message).
    return output


# Function to show all possible messages with the given keys.
def brute_force_cracker(message):

    # ANSI codes to try to make the key text more visible.
    BOLD = '\033[1m'
    RESET = '\033[0m'

    # We prepare a variable to store the result.
    result = ''

    # We iterate through the alphabet...
    for key in range(len(alphabet)):

        # We encode the message according to the key attempt we are on and store it.
        attempt = cesar_encoder(message.lower(), key)
        
        # We add the attempt to the output variable with the corresponding key (in bold).
        result += (f"{BOLD}Key {key:02d}:{RESET} {attempt}\n")
    
    # We return the output (all possible messages with all possible keys).
    return result


# Function to calculate how often a letter appears.
def calculate_frequencies(text, total_letters):
    # We will store the calculated frecuencies of each character in this variable.
    frecuencies = ''

    # We will keep track of how many times a letter appears in the letter_counts dictionary.
    letter_counts = {}
    
    # We iterate through the best found message.
    for char in text:

        # If the character is in the alphabet.
        if char in alphabet:

            # We add the times it has appeared to the dictionary given the current char.
            letter_counts[char] = letter_counts.get(char, 0) + 1
            
    # We sort the letters based on their score (we turn the dictionary into a list).
    sorted_letters = sorted(letter_counts.items(), key=lambda item: item[1], reverse=True)
    
    # We loop through the new list.
    for letter, count in sorted_letters:

        # We calculate the percentage of the letter.
        percentage = (count / total_letters) * 100

        # We add the percentage in the correct format to the output variable.
        frecuencies += (f"\n{letter.upper()}: {percentage:.1f}%")
    
    # We return the frecuencies table.
    return frecuencies


# Function to crack an encoded message based on frequency analysis.
def frequency_cracker(message):

    # We define a dictionary with how common each letter is in spanish.
    spanish_frequencies = {
        'e': 13.68, 'a': 12.53, 'o': 8.68, 's': 7.98, 'r': 6.87, 
        'n': 6.71, 'i': 6.25, 'd': 5.86, 'l': 4.97, 'c': 4.68, 
        't': 4.63, 'u': 3.93, 'm': 3.15, 'p': 2.51, 'b': 1.42, 
        'g': 1.01, 'v': 0.90, 'y': 0.90, 'q': 0.88, 'h': 0.70, 
        'f': 0.69, 'z': 0.52, 'j': 0.44, 'x': 0.22, 'w': 0.02, 'k': 0.01
    }
    
    # We will count the total amount of letters in the message.

    # total_letters will store the amount.
    total_letters = 0

    # We iterate through the message.
    for char in message.lower():

        # If the character is in the alphabet, we count it.
        if char in alphabet:
            total_letters += 1
            
    # If there are no letters, we return directly.
    if total_letters == 0:
        return 0, 0, message, ""


    # We will calculate the arbitrary maximum score with the given length of the message.
    max_possible_score = total_letters * max(spanish_frequencies.values())
    
    # We define some output variables to store the results.
    best_key = 0
    best_score = 0
    best_message = ""
    
    # We iterate through the alphabet (similar to the brute force method)...
    for key in range(len(alphabet)):

        # We will encode the message with the given key of the loop.
        attempt = cesar_encoder(message.lower(), key)
        
        # We will keep track of the score with raw_score.
        raw_score = 0

        # We will iterate through each character in the 'decoded' message.
        for character in attempt:
            
            # We will add the corresponding value of the dictionary of the char to the score.
            raw_score += spanish_frequencies.get(character, 0)
            
        # We normalize the score out of 100 limited by the max possible score.
        normalized_score = (raw_score / max_possible_score) * 100

        # If the current normalized score is better, it becomes the new best score.
        if normalized_score > best_score:

            # We update the best score, key, and message.
            best_score = normalized_score
            best_key = key
            best_message = attempt

    # We obtain the frequencies of the original message.
    message_frequencies = calculate_frequencies(message.lower(), total_letters)

    # We obtain the frequencies of the newly found message.
    found_frequencies = calculate_frequencies(best_message, total_letters)
    
    # Return the rounded best score, key, message, and the two frequencies.
    return round(best_score, 2), best_key, best_message, message_frequencies, found_frequencies


# Main program loop.
def main():

    # We print the menu gui.
    print("\n==========================================================\n" \
    "          Welcome to the Caesar cypher software"
    "\n==========================================================")

    # We will repeat this loop until the user chooses to terminate the program.
    while True:
        
        # We ask them what they wish to do.
        print("\n\nSelect what you wish to do.")
        
        # We force an integer answer into the variable answer.
        answer = force_answer_int("\n1) Encode into Caesar.\n2) Crack encoded Caesar.\n3) Quit.\n", "Selection (1-3)")
        
        if answer == 3:

            # We terminate the main loop and thus end the program.
            print("\nThanks for using the program.")
            break
        
        # If they wish to encode a message...
        elif answer == 1:

            message = input("\nMessage to Encode: ")

            key = force_answer_int('', "What key do you wish to use to encode the message (N)?")

            result = cesar_encoder(message.lower(), key)

            print(f"{message} encoded with the key: {key} is:\n{result}")

            # We place an input so the menu does not appear suddenly.
            input("\nPress Enter to Continue...")

        # If they wish to crack a message....
        elif answer == 2:

            crack_choice = force_answer_int("\n1) Manual Brute Force.\n2) Automatic Frequency Analysis.\n3) Both.\n4) Cancel.\n", "Selection (1-4)")

            
            if crack_choice <= 3 and crack_choice >= 1:
                
                # We ask for a message
                message = input("\nEncoded Message: ")

                if crack_choice == 1 or crack_choice == 3:
                    
                    result = brute_force_cracker(message)
                    
                    print("\nThese are all the possible messages using all available keys:\n" + result)
                
                if crack_choice == 2 or crack_choice == 3:

                    best_score, best_key, best_message, og_frecuencies, new_frequencies = frequency_cracker(message)

                    print("\nBased on a simple statistical analysis, these are the results of the most likely key and thus message:\n")

                    print(f"Top Score: {round(best_score, 2)} points")
                    print(f"Likely Key: {best_key:02d}")
                    print(f"Decoded Message:\n{best_message.upper()}")

                    print("\nOriginal Letter frecuencies:\n", og_frecuencies + "\n")
                    print("\nDecoded Letter fecuencies:\n", new_frequencies+ "\n")


                # We place an input so the menu does not appear suddenly.
                input("\nPress Enter to Continue...")
            elif crack_choice == 4:
                continue

            else:
                # The user selected an int out of range.
                print("\nError. Please select a valid option.")

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
