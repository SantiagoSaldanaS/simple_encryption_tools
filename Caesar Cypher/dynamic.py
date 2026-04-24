alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# ==========================================================
# 1. HELPER FUNCTIONS
# ==========================================================
def calculate_frequencies(text, total_letters):
    frequencies_output = ''
    letter_counts = {}
    
    for char in text:
        if char in alphabet:
            letter_counts[char] = letter_counts.get(char, 0) + 1
            
    sorted_letters = sorted(letter_counts.items(), key=lambda item: item[1], reverse=True)
    
    for letter, count in sorted_letters:
        percentage = (count / total_letters) * 100
        frequencies_output += (f"\n{letter.upper()}: {percentage:.1f}%")
        
    return frequencies_output

# ==========================================================
# 2. ENCODERS
# ==========================================================
def cesar_encoder(message, key):
    output = ''
    for character in message:
        if character in alphabet:
            shifted = (alphabet.index(character) + key) % len(alphabet)
            output += alphabet[shifted]
        else:
            output += character
    return output

def dynamic_encoder(message, key_sequence):
    output = ""
    key_index = 0 
    
    for char in message.lower():
        if char in alphabet:
            current_key = key_sequence[key_index % len(key_sequence)]
            shifted = (alphabet.index(char) + current_key) % len(alphabet)
            output += alphabet[shifted]
            key_index += 1 
        else:
            output += char
    return output

# ==========================================================
# 3. MATH ENGINE (INDEX OF COINCIDENCE)
# ==========================================================
def calculate_ioc(text):
    N = len(text)
    if N <= 1:
        return 0.0
        
    ioc_sum = 0
    for char in alphabet:
        f = text.count(char)
        ioc_sum += f * (f - 1)
        
    return ioc_sum / (N * (N - 1))

def guess_key_length(message, max_length=15):
    clean_message = "".join([c for c in message.lower() if c in alphabet])
    best_length = 1
    best_avg_ioc = 0.0
    
    print("--- Analyzing Index of Coincidence ---")
    
    for length_to_test in range(1, max_length + 1):
        total_ioc = 0
        for i in range(length_to_test):
            column_text = clean_message[i::length_to_test]
            total_ioc += calculate_ioc(column_text)
            
        avg_ioc = total_ioc / length_to_test
        
        if avg_ioc > best_avg_ioc:
            best_avg_ioc = avg_ioc
            best_length = length_to_test
            
    print(f"Detected highest IoC ({best_avg_ioc:.4f}) at a key length of: {best_length}\n")
    return best_length

# ==========================================================
# 4. CRACKERS
# ==========================================================
def frequency_cracker(message):
    # UPDATED FOR ENGLISH LETTER FREQUENCIES
    english_frequencies = {
        'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
        's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
        'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
        'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
        'q': 0.10, 'z': 0.07
    }
    
    total_letters = sum(1 for char in message.lower() if char in alphabet)
    if total_letters == 0:
        return 0, 0, message, "", ""

    max_possible_score = total_letters * max(english_frequencies.values())
    
    best_key = 0
    best_score = 0
    best_message = ""
    
    for key in range(len(alphabet)):
        attempt = cesar_encoder(message.lower(), key)
        raw_score = sum(english_frequencies.get(char, 0) for char in attempt)
        normalized_score = (raw_score / max_possible_score) * 100

        if normalized_score > best_score:
            best_score = normalized_score
            best_key = key
            best_message = attempt

    message_freq = calculate_frequencies(message.lower(), total_letters)
    found_freq = calculate_frequencies(best_message, total_letters)
    
    return round(best_score, 2), best_key, best_message, message_freq, found_freq

def dynamic_cracker(message):
    guessed_length = guess_key_length(message)
    clean_message = "".join([c for c in message.lower() if c in alphabet])
    discovered_keys = []
    
    for i in range(guessed_length):
        column_text = clean_message[i::guessed_length]
        _, best_key, _, _, _ = frequency_cracker(column_text)
        discovered_keys.append(best_key)
        
    final_message = dynamic_encoder(message, discovered_keys)
    
    print(f"Discovered Key Sequence: {discovered_keys}")
    print(f"\n==========================================================")
    print(f"FINAL DECODED MESSAGE")
    print(f"==========================================================\n")
    print(final_message.upper())
    print(f"\n==========================================================")
    
    return final_message

# ==========================================================
# 5. PLAYGROUND
# ==========================================================
if __name__ == '__main__':
    print("\nRUNNING FULLY AUTOMATIC CRACKER...")
    
    encrypted_text = "KJWTKZUGZQJXOEAIQFRITVOSSSGGAQKGXFRZITKGGDWXZVGFZZTSSNGXIOLH SQFITOLUGZQKGSSTREOUQKTZZTIQFUOFUGXZIOLDGXZIITOLQEGVWGNAORNT QIITYGXFRQLONLIGGZTKUXFOFIOLRQRESGLTZQFRVOZIQWGZGYYXFZIOFULOR GFZTCTFAFGVVIQZWXZITOLEGDOFUYGKNGXNTQIITOLEGDOFUYGKNGXQSSZIT GZITKAORLVOZIZITHXDHTRXHAOEANGXWTZZTKKXFWTZZTKKXFGXZKXFDNU XFQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANGXWTZZTKKXFWTZZTKKXFYQ LZTKZIQFDNWXSSTZQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANGXWTZZTKK XFWTZZTKKXFGXZKXFDNUXFQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANGX WTZZTKKXFWTZZTKKXFYQLZTKZIQFDNWXSSTZRQRRNVGKALQSGFURQNIT'RW TEGDOFUIGDTSQZTNTQIITOLEGDOFUIGDTSQZTQFRITOLWKOFUOFUDTQLXKHK OLTEQXLROFFTKOLOFZITAOZEITFQFROZOLHQEATROFOETOIQCTVQOZTRYGKQ SGFUZODTNTQIZITLSTOUIZGYDNIQFROLFGVQJXOEAHXSSZKOUUKOKTQLGFVO ZIDNEOUQKTZZTZITFLQNNGXKIQOKOLGFYOKTNGXDXLZIQCTSGLZNGXKVOZL NTQIQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANGXWTZZTKKXFWTZZTKKXFG XZKXFDNUXFQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANGXWTZZTKKXFWTZ ZTKKXFYQLZTKZIQFDNWXSSTZQSSZITGZITKAORLVOZIZITHXDHTRXHAOEANG XWTZZTKKXFWTZZTKKXFGXZKXFDNUXFQSSZITGZITKAORLVOZIZITHXDHTRX HAOEANGXWTZZTKKXFWTZZTKKXFYQLZTKZIQFDNWXSSTZ"
    
    cracked_text = dynamic_cracker(encrypted_text)