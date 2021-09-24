from selenium import webdriver
import time
import keyboard

driver = webdriver.Chrome('./chromedriver')

driver.get('https://monkeytype.com')

time.sleep(5)
    
word_id = driver.find_elements_by_class_name("word")
last_sentence = []

def array_differentiation(sentence, prev_sentence=[]):
    if prev_sentence == []:
        return sentence
    
    for i in range(len(prev_sentence)):
        if sentence[0] == prev_sentence[i]:
            if sentence[1] == prev_sentence[i + 1]:
                if sentence[2] == prev_sentence[i + 2]:
                    if sentence[3] == prev_sentence[i + 3]:
                        overlap_length = len(prev_sentence) - i
                        return sentence[overlap_length:] 
    
    return sentence


while len(word_id) != 0:
    word_id = driver.find_elements_by_class_name("word")

    words = []
    for attr in word_id:
        word = attr.text
        if word != "":
            words.append(word)

    print(words) 
    prev_words = words
    words = array_differentiation(words, prev_sentence=last_sentence)
    print(words)
    if prev_words == words:
        print("EXCEPTION HERE")
        print(prev_words)
    print()
    
    if words == last_sentence:
        continue 
    
    for i in range(len(words)):
        temp_word = words[i]
        temp_word = temp_word.split()
        for character in temp_word:
            keyboard.write(character)
        # keyboard.write(words[i])
        keyboard.write(' ')
    
    last_sentence = words

    '''
    sentence = ' '.join(words)
    for prev_sentence in sentence_set:
        if sentence in prev_sentence:
            len_diff = len(prev_sentence) - len(sentence)

    try: 
        sentence = sentence[len_diff:]
    except:
        pass
    
    print(sentence)

    sentence_set.add(sentence)
    keyboard.write(sentence)
    print()
    '''