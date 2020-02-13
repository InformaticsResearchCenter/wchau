import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

class KataIndo:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            '../auth/kata-indo.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.typo_sheet = self.client.open('kata-typo-indo').sheet1
        self.typo_words = self.typo_sheet.get_all_values()

    # Memperbagus kata
    def fixWord(self, word):
        status = False
        word = re.sub(r'[?|$|.|!|,|@|#|%|^|*|(|)|_|-|+|=|/|{|}|;|:|"|\'|\||[|\]|/|\||\\]',r'',word)
        chars1 = [char for char in word]
        for word_list in self.typo_words:
            words = word_list[1].split(",")+[word_list[0]]
            for wordx in words:                
                chars2 = [char for char in wordx]
                chars3 = [item for item in chars2 if item in chars1]                    
                if len(chars3) == len(chars2) and set(chars1).issubset(chars3):
                    status = True
                    break

            if status:
                word = ""
                return word.join(chars3)
                break
            
    # Menerjemahkan kata typo
    def setWord(self, search):
        searchs = self.fixWord(search)
        if searchs is not None:
            for word_list in self.typo_words:
                word = word_list[1].split(",")
                if searchs in word:
                    return word_list[0]
                    break
            return searchs
        else:
            return search

    # Menyambungkan kata-kata menjadi kalimat
    def listToString(self, list_word):
        sentence = " "
        return sentence.join(list_word)

    # Kalimat fix
    def sentenceFix(self, sentence):
        word_split = sentence.split()
        sentence_fix = []
        for word in word_split:
            sentence_fix.append(word.replace(word, self.setWord(word)))
        return self.listToString(sentence_fix)
