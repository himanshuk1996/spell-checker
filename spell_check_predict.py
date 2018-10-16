import pickle
import numpy as np

from typing import Tuple


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True

def find_count(root, prefix: str):
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return node.counter

def spell_checker(root,word:str,desperateness_index=2):
    node=root
    probable_replacements=[]
    found=False
    i=0
    if isthere(root,word):
        return word
    if not root.children:
        return False
    node = root
    
    for char in word:
        if i>3 and len(node.children)==1:
            return spell_predictor(root,word[:i])
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            # print('error at '+char)
            lister=[]
            for a in node.children:
                lister.append(a.counter)
#             for a in node.children:
#                 print(a.char) 
            if len(lister)>0:
                probable_replace=lister.index(max(lister))
                new_word_2=word[:i]+node.children[probable_replace].char+word[i+1:]
                new_word_1=word[:i]+node.children[probable_replace].char+word[i:]
                new_word_3=word[:i]+word[i+1:]
                if isthere(root,new_word_1) and not found:
                    found=True
                    probable_replacements.append(new_word_1)
                if isthere(root,new_word_2) and not found:
                    found=True
                    probable_replacements.append(new_word_2)
                if isthere(root,new_word_3)and not found:
                    found=True
                    probable_replacements.append(new_word_3)
                break
        i=i+1
    if not node.word_finished:
        predicted_word=spell_predictor(root,word)
        if predicted_word:
            probable_replacements.append(predicted_word)
            found=True
    if not found:
        i=0
        node = root
        for char in word:
            for index in range(len(node.children)):
                new_word_2=word[:i]+node.children[index].char+word[i+1:]
                new_word_1=word[:i]+node.children[index].char+word[i:]
                new_word_3=word[:i]+word[i+1:]
                if isthere(root,new_word_1) and not found:
                    found=True
                    probable_replacements.append(new_word_1)
                if isthere(root,new_word_2) and not found:
                    found=True
                    probable_replacements.append(new_word_2)
                if isthere(root,new_word_3) and not found:
                    found=True
                    probable_replacements.append(new_word_3)
            for child in node.children:
                if child.char == char:
                    node = child
                    i=i+1
                    
    if not found and desperateness_index>1:
        i=0
        node = root
        for char in word:
            for index in range(len(node.children)):
                new_word_1=word[:i]+node.children[index].char+word[i:]
                new_word = spell_checker(root,new_word_1,desperateness_index-1)
                if new_word:
                    return new_word
                    found =True
            for child in node.children:
                if child.char == char:
                    node = child
                    i=i+1
        i=0
        node = root
        for char in word:
            for index in range(len(node.children)):
                new_word_2=word[:i]+node.children[index].char+word[i+1:]
                new_word = spell_checker(root,new_word_2,desperateness_index-1)
                if new_word and not found:
                    return new_word
                    found =True
            for child in node.children:
                if child.char == char:
                    node = child
                    i=i+1
                    
        i=0
        node = root
        for char in word:
            for index in range(len(node.children)):
                new_word_3=word[:i]+word[i+1:]
                new_word = spell_checker(root,new_word_3,desperateness_index-1)
                if new_word:
                    return new_word
                    found =True
            for child in node.children:
                if child.char == char:
                    node = child
                    i=i+1
    if found:
        new_word=probable_replacements[0]
        return new_word

def spell_predictor(root,prefix:str):
    node = root
    word=prefix
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
    
    while not node.word_finished:
        lister=[]
        for child in node.children:
            lister.append(child.counter)
        next_index=lister.index(max(lister))
        word=word+node.children[next_index].char
        node=node.children[next_index]
        
    if(isthere(root,word)):
        return word

def isthere(root,word):
    node = root
    is_there=True
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        if not found_in_child:
            is_there=False
    if not node.word_finished:
        is_there=False
    return is_there
            
    

# root=TrieNode('*')
# from nltk.corpus import words
# for each_word in words.words():
#     add(root,each_word)

# with open('myvoc.pickle','wb') as h:
#     pickle.dump(root,h,protocol=pickle.HIGHEST_PROTOCOL)
with open('myvoc.pickle','rb') as h:
    root = pickle.load(h)

spell_checker(root,'printe')

spell_predictor(root,'printe')