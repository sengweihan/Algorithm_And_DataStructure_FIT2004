# FIT2004 S1/2021: Assignment 3 - Tries and Trees

# Firstly create a Trie Class and a node class.
class Node:

    def __init__(self):
        # character a-z = 26 and one more is for the character $ which adds up to 27 slots
        self.link = [None] * 27
        # To keep track of how many words have been inserted into the Trie.
        self.word_count = 0


class Trie:

    def __init__(self):
        # Each Trie will have one root node.
        self.root = Node()

    def insertion(self, words):
        # Begin insertion of characters starting from the root node.
        current_node = self.root

        for character in words:
            index = ord(character) - 96  # index 0 is for $ character.

            # Check whether the current character is a child of the current node.
            if current_node.link[index] is not None:
                # if the current_node.link[index] contains a link to another array, we will set the current node to that new linked array.
                current_node = current_node.link[index]
                current_node.word_count += 1

            else:
                # if the current character is not a child of the current node , then we will need to create a new node for that
                # character and set the current node to that new node created.
                new_node = Node()
                current_node.link[index] = new_node
                current_node = current_node.link[index]
                # Will keep track of the frequency of each characters when a new node is created. For eg: if 'a' is not in the array,
                # we will create a new node for 'a' and current will point to this new node and update the frequency of the total number
                # of character 'a' that have been added.
                current_node.word_count += 1

        # Lastly we will need to do the same check for the $ character to indicate the finalized word.
        if current_node.link[0] is not None:
            current_node = current_node.link[0]
            current_node.word_count += 1
        else:
            new_node = Node()
            current_node.link[0] = new_node
            current_node = current_node.link[0]
            current_node.word_count += 1

    def get_lex_pos(self, strings):

        # Initialized the current node to be the root node.
        current = self.root
        # To accumulate the amount of words which is greater than the word in strings.
        accumulator = 0

        if len(strings) == 0:
            # Since our for loops will only loop for 27 times hence, our time complexity is O(27) which is equaivalent
            #  to O(1) since 27 is constant
            for i in range(1, len(current.link)):
                if current.link[i] is not None:
                    accumulator += current.link[i].word_count
        else:
            for char in strings:
                index = ord(char) - 96  # index 0 is for $ character.

                # from the root node, find those character which is greater than the current char
                for i in range(index+1, len(current.link)):
                    if current.link[i] is not None:
                        # Accumulate the value.
                        accumulator += current.link[i].word_count

                # Now we will traverse through the char and update the current .
                if current.link[index] is not None:
                    current = current.link[index]
                else:
                    # handle the case where the character is not in node.
                    return accumulator
                    # for i in range(1, len(current.link)):
                    #     if current.link[i] is not None:
                    #         accumulator += current.link[i].word_count

            # Once we have finish traversing, we will use this for loops to check whether the current node have a link (its children node)
            # and if it do have a children node, we will accumulate the results to accumulator.

            for i in range(1, len(current.link)):
                if current.link[i] is not None:
                    accumulator += current.link[i].word_count

        return accumulator


def lex_pos(text, queries):
    """
    PURPOSE : THIS FUNCTION WILL FIRST CREATE A TRIE OBJECT TO ALLOW INSERTION OF TEXT INTO THE TRIE. IT WILL THEN LOOP THROUGH THE QUARIES 
    WHICH IN THIS CASE IS A LIST OF WORDS AND IT WILL FIND THE NUMBER OF WORDS IN THE TRIE WHICH ARE LEXICOGRAPHICALLY GREATER THAN THE 
    i^th ELEMENT OF THE QUARIES.

    ARGUMENTS : TEXT WHICH IN THIS CASE IS AN UNSORTED LISTS OF STRINGS . EACH STRINGS CONSIST OF ONLY LOWERCASE a-z LETTERS . TEXT 
    CAN CONTAIN DUPLICATES WHEREAS QUARIES IS A LIST OF STRINGS CONSISTING OF ONLY LOWERCASE a-z CHARACTERS . EACH STRING IN QUERIES 
    IS A PREFIX OF SOME STRING IN THE TEXT 

    OUTPUT : LEX_ POS WILL OUTPUT A LIST OF NUMBERS . THE i^th NUMBER IN THE LIST IS THE NUMBER OF WORDS IN TEXT
    WHICH ARE LEXICOGRAPHICALLY GREATER THAN THE i^th ELEMENT OF QUERIES.

    COMPLEXITY : THE FIRST FOR LOOP WHICH INSERT EACH STRING IN TEXT WILL TAKE O(T) WHERE T = SUM OF NUMBERS OF CHARACTERS IN ALL STRINGS IN TEXT
    WHEREAS THE SECOND FOR LOOPS WHICH SEARCH THROUGH THE TRIE TO FIND THOSE TEXT WHICH ARE LEXICOGRAPHICALLY GREATER THAN THE QUERIES STRINGS 
    USES O(Q) WHERE Q = THE TOTAL NUMBER OF CHARACTER IN THE QUERIES . HENCE OVERALL COMPLEXITY IS O(T+Q) WHICH DOES SATISFY THE REQUIREMENT.
    """
    # create a Trie object
    trie_obj = Trie()
    lst = []  # create a new list to stores the output.

    # Loop through the list of text and insert each word into the Trie
    for word in text:
        # This particular for loops will run together with calling insertion method will give us
        # a complexity of O(T) where T = sum of the number of characters in all strings in text
        trie_obj.insertion(word)

    # Once insertion completed, we can now find the number of words in text which is lexicographically
    # greater than the i^th element in the quaries. I created an additional function in the trie which helps to solve
    # the problem of finding those words which is lexicographically greater than the i^th element in the queries.
    for word in queries:
        lst.append(trie_obj.get_lex_pos(word))

    return lst
