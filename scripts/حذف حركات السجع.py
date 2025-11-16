import re

def extract_last_char_and_haraka(word):
    vowels = ['َ', 'ُ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ', 'ّ']
    if not word:
        return None, None
    char = word[-1]
    if char in vowels:
        return word[-2], char
    return char, None

pattern = r'^\w{3,4}[،"]\ .*\،\ .*$'
intro_sentence = "-------------------------تعرية أواخر هذه الكلمات للسجع---------------------"

with open('ملاحظات حركات السجع.txt', 'w', encoding='utf-8') as file:  
    file.write(intro_sentence + '\n\n')

with open('جذاذة.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('تاريخ آخر تحديث')

for record in data:
    lines = record.splitlines()
    for line in lines:
        if line.startswith('"') and line.endswith('"'):
            matched_sentences = re.findall(pattern, line, re.MULTILINE)
            
            words = re.split(r'[،"؟!.]\s*', line)
            words = [word.strip() for word in words if word.strip()]
            matching_words = []
    
            for i in range(len(words) - 1):
                char1, haraka1 = extract_last_char_and_haraka(words[i])
                char2, haraka2 = extract_last_char_and_haraka(words[i+1])
        
                if char1 and char2 and char1 == char2 and haraka1 == haraka2 and haraka1 is not None:
                    matching_words.append((words[i], words[i+1]))
    
            with open('ملاحظات حركات السجع.txt', 'a', encoding='utf-8') as file:
                if matching_words:
                    for sentence in matched_sentences:
                        file.write(sentence + '\n')
                    for pair in matching_words:
                        file.write(pair[0] + ' - ' + pair[1] + '\n')
                    file.write("\n")
