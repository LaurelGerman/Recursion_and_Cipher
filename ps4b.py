# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        assert isinstance(text, str), "Text is not a string"
        
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_dict_piece(self, shift, alphabet, shift_dict):
        '''
        Helper function for build_shift_dict
        
        Parameters
        ----------
        shift (integer): the amount by which to shift every letter of the 
        alphabet. -26 < shift < 26
        
        alphabet : alphabet string literal upon which to build the dictionary; 
        will be string.ascii_lowercase or string.ascii_uppercase
        
        shift_dict : the dictionary into which to enter the values
        
        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        -------
        None.

        '''
        assert isinstance(shift, int), "Shift is not an int"
        assert -26 < shift < 26, "Shift must be between -26 and 26"
        assert isinstance(alphabet, str), "Alphabet is not a string"
        assert isinstance(shift_dict, dict), "shift_dict is not a dictionary"
        
        for c in range(len(alphabet)): #for every letter
            if(shift >=0): #shift down in alphabet
                if(c+shift<26): #if doesn't cause wraparound
                    shift_dict[alphabet[c]] = alphabet[c+shift]
                else: #if does cause wraparound
                    shift_dict[alphabet[c]] = alphabet[c+shift-26]
            else: #shift up in alphabet
                if(c+shift >=0): #if doesn't cause wraparound
                    shift_dict[alphabet[c]] = alphabet[c+shift]
                else: #if does cause wraparound
                    shift_dict[alphabet[c]] = alphabet[c+shift+26]
        
        return shift_dict        

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. -26 < shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        assert isinstance(shift, int), "Shift is not an int"
        assert -26 < shift < 26, "Shift must be between -26 and 26"
        
        shift_dict = {}
        
        shift_dict = self.build_dict_piece(shift, string.ascii_lowercase, shift_dict)
        shift_dict = self.build_dict_piece(shift, string.ascii_uppercase, shift_dict)
                
        return shift_dict
    
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        
        assert isinstance(shift, int), "Shift is not an int"
        assert -26 < shift < 26, "Shift must be between 0 and 26"
        
        shift_dict = self.build_shift_dict(shift)
        ciphertext = ''
        
        for l in self.get_message_text():
            if l in string.ascii_letters:
                ciphertext += shift_dict[l]
            else:
                ciphertext += l
        
        return ciphertext
                

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        assert isinstance(shift, int), "Shift is not an int"
        assert 0 <= shift < 26, "Shift must be between 0 and 26"
        assert isinstance(text, str), "Text is not a string"
        
        Message.__init__(self,text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift
    
    def set_shift(self, shift):
        assert isinstance(shift, int), "Shift is not an int"
        assert 0 <= shift < 26, "Shift must be between 0 and 26"
        self.shift = shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()
    
    def set_encryption_dict(self, shift):
        assert isinstance(shift, int), "Shift is not an int"
        assert 0 <= shift < 26, "Shift must be between 0 and 26"
        self.encryption_dict = self.build_shift_dict(shift)
        
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def set_message_text_encrypted(self, shift):
        assert isinstance(shift, int), "Shift is not an int"
        assert 0 <= shift < 26, "Shift must be between 0 and 26"
        self.message_text_encrypted = self.apply_shift(shift)

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        assert isinstance(shift, int), "Shift is not an int"
        assert 0 <= shift < 26, "Shift must be between 0 and 26"
        
        self.set_shift(shift)
        self.set_encryption_dict(shift)
        self.set_message_text_encrypted(shift)
        


class CiphertextMessage(Message):

# =============================================================================
#     def __init__(self, text):
#         '''
#         Initializes a CiphertextMessage object
#                 
#         text (string): the message's text
# 
#         a CiphertextMessage object has two attributes:
#             self.message_text (string, determined by input text)
#             self.valid_words (list, determined using helper function load_words)
#         '''
#         pass
# =============================================================================
        


    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        valid_list = self.get_valid_words()
        best_try = ''
        best_score = 0
        best_shift = 0
        ties = []
        
        for s in range(0,-26,-1):
            this_try = self.apply_shift(s)            
            list_of_words = this_try.split(" ")
            num_words = 0
            
            for word in list_of_words:
                if(is_word(valid_list,word)):
                    num_words +=1
            
            if(num_words > best_score):
                best_shift = s
                best_score = num_words
                best_try = this_try
                ties = []
                
            elif(num_words == best_score):
                ties.append(s)
        
        if(len(ties) > 0):
            print("Other options:",ties)
            
        return (best_shift,best_try)
            

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #WRITE YOUR TEST CASES HERE
# =============================================================================
#     orig = PlaintextMessage('Hello World!',2)
#     print(orig.get_message_text_encrypted())
#     orig.change_shift(7)
#     print(orig.get_message_text_encrypted())
#     
#     cyph = CiphertextMessage('Olssv, Dvysk!')
#     print(cyph.decrypt_message())
#     
# =============================================================================
    story_cyph = CiphertextMessage(get_story_string())
    print(story_cyph.decrypt_message())
    
    

    #TODO: best shift value and unencrypted story 
    

