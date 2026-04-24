
# Santiago Saldaña Subías - A01708446
# Diego Perea León - A01708350

# Dictionary that allows us to map numbers to letters when working with higher bases (11 = A, 12 = B, etc).
hex_map = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'A',
    11: 'B',
    12: 'C',
    13: 'D',
    14: 'E',
    15: 'F',
    16: 'G',
    17: 'H',
    18: 'I',
    19: 'J',
    20: 'K',
    21: 'L',
    22: 'M',
    23: 'N',
    24: 'O',
    25: 'P',
    26: 'Q',
    27: 'R',
    28: 'S',
    29: 'T',
    30: 'U',
    31: 'V',
    32: 'W',
    33: 'X',
    34: 'Y',
    35: 'Z',
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
        answer = input("\n" + question + ": ").strip().upper().replace(' ', '')

        # If we have an answer, we return the answer and end the loop.
        if answer:
            return answer
        else:
            # If we don't have an answer, we  continue looping.
            print("\nError. Input cannot be empty.")


# Function to force the user to input a valid base.
def force_valid_base():

    # We iterate until we are given a valid base.
    while True:

        # We force a whole number input.
        base = force_answer_int("", "Base to use (2-35)")

        # We check if the number is within the range the program allows for bases.
        if base >= 2 and base <= 35:

            # If it is greater/equal to 2, and lesser or equal to 35, we return the valid base.
            return base
        else:
            # If the base is not valid, we ask for it again and repeat the loop.
            print("\nError. Please select a valid base.")


# Function to convert (shift) any valid decimal number to another given base.
def dec2base(_number, base):

    # If the number is 0, we skip everything and just return 0.
    if _number == 0:
        return '0'

    # We check whether the number is positive or negative. If it is negative we
    # store this information into sign and then turn the number to positive.
    sign = 0
    
    # If the number is negative...
    if _number < 0:
        # Sign becomes 1 (True).
        sign = 1

        # We turn the number positive (its absolute value).
        number = abs(_number)
    else:
        # Else we do not modify the number.
        number = _number

    # Result will store the string value of each part of the conversion through each loop.
    result = ''

    try:
        # While the number is greater than 0 (we have not finished)...
        while number > 0:
            # The remainder will be the value that the number needs to get rid of in order to be
            # perfectly divided by the base.
            remainder = number % base

            # We reduce the number to the nearest down number that can be divided by the base as a whole.
            number = number // base

            # Adding all remainders will give us the new number on the new base (though we have to invert it).
            # When working with higher bases we need the dictionary to translate a remainder like 10, 11, etc. 
            # into A, B, etc.
            result += hex_map[remainder]

    except KeyError:
        # This happens if the base is too high (there is no equivalent value in the dictionary, so the base was greater than 35).
        return "\nError. This program does not support a base this high."
    
    # If the original number was negative, we add a - to the final result.
    if sign:
        result += '-'

    # We have to invert the string due to how we added the numbers (ex: turning 1011- to -1011).
    return(result[::-1])


# Function to convert any number with any given base into base 10 (decimal).
def base2dec(_number, base):
    
    # We check whether the number is positive or negative. If it is negative we
    # store this information into sign and then turn the number to positive.
    sign = 0

    # If the number is negative (starts with -)...
    if _number.startswith('-'):
        # Sign becomes 1 (True).
        sign = 1

        # We remove the - sign from the number so it does not cause any issues.
        num = _number.replace('-', '')
    else:
        # Else we do not touch it.
        num = _number

    # We invert the input string.
    inv_binary = str(num)[::-1]

    # We will store all the additions within result, which begins at 0.
    result = 0
    try:
        # We iterate through the whole string, a character at a time.
        for n in range(len(inv_binary)):
            
            # We turn the number inside the string at the nth position into an
            # integer according to the base (which allows us to convert for ex A into 10),
            # and then multiply that number with the base raised to the nth power.
            adding = int(inv_binary[n], base) * base**n

            # The result of the previous operation will be added to the final sum of all characters.
            result += adding

    except ValueError:

        # This will trigger if the base provied into int() does not match the character of the
        # string its trying to convert, if the number is too large, or if the number itself is not valid.
        return "\nError. Number too large or base is too high."

    # We return the sum of the value of all characters (the result).
    return result


def main():

    # We print the menu text.
    print("\n==========================================================\n" \
    "           Welcome to the base convertor software"
    "\n==========================================================")

    # We will repeat this loop until the user chooses to terminate the program.
    while True:
        
        # We ask them what type of conversion they wish to do.
        print("\n\nSelect what type of conversion you wish to do.")
        
        # We force an integer answer into the variable answer.
        answer = force_answer_int("\n1) Decimal to Binary.\n2) Binary to Decimal.\n3) Decimal to Hexadecimal.\n4) Hexadecimal to Decimal\n5) Decimal to Base\n6) Base to Decimal\n7) Quit\n", "Selection (1-7)")
        
        # If the answer involves converting a decimal, we group the code...
        if answer == 1 or answer == 3 or answer == 5:

            # We get a number.
            number = force_answer_int("", "Decimal to convert")
            
            # Presets for the types of conversions. The only change is the base.
            if answer == 1:

                # We convert the number to binary.
                print("Your conversion is:", dec2base(number, 2))

            elif answer == 3:

                # We convert the number to HEX.
                print("Your conversion is:", dec2base(number, 16))

            elif answer == 5:

                # We ask the user for a base, and then convert the number to that base.
                base = force_valid_base()
                print("Your conversion is:", dec2base(number, base))
            
            # We place an input so the menu does not appear suddenly.
            input("\nPress Enter to Continue...")

        # If the answer involves a possible string, we group the code...
        elif answer == 2 or answer == 4 or answer == 6:

            # We get the string.
            number_str = force_answer_str("Number to convert")
            
            # We change the base depending on the answer.
            if answer == 2:
                base = 2

            elif answer == 4:
                base = 16

            elif answer == 6:
                base = force_valid_base()

            # We convert thenumber to the given base
            print("Your conversion is:", base2dec(number_str, base))

            # We place an inputso the menu does not appear suddenly.
            input("\nPress Enter to Continue...")
        
        elif answer == 7:

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
