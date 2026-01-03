import spacy
from nltk import Tree
nlp= spacy.load("en_core_web_sm")

# Not Needed in ISL
stop_words = set(["am","are","is","was","were","be","being","been","have","has","had", "does","did","could","should","would","can","shall","will","may","might","must","let"])

# print(nlp.pipe_names)

# sentences array
sent_list = [];
# sentences array
sent_list_detailed=[];
# word array
word_list=[];
# word array with details
word_list_detailed=[];


def convert_to_sentence_list(text):
	for sentence in text.sents:
		sent_list.append(sentence.text)
		sent_list_detailed.append(sentence)

def convert_to_sentence_list(text):
    for sentence in text.sents:
        sent_list.append(sentence.text)
        sent_list_detailed.append(sentence)

def convert_to_word_list(sentences):
	temp_list=[]
	temp_list_detailed=[]
	for sentence in sentences:
		for word in sentence:
			temp_list.append(word.text)
			temp_list_detailed.append(word)
		word_list.append(temp_list.copy())
		word_list_detailed.append(temp_list_detailed.copy())
		temp_list.clear();
		temp_list_detailed.clear()

# removes stop words
def filter_words(word_list):
	temp_list=[];
	final_words=[];
	# removing stop words from word_list
	for words in word_list:
		temp_list.clear();
		for word in words:
			if word not in stop_words:
				temp_list.append(word);
		final_words.append(temp_list.copy());
	# removes stop words from word_list_detailed 
	for words in word_list_detailed:
		for i,word in enumerate(words):
			if(words[i].text in stop_words):
				del words[i];
				break;
	
	return final_words;

def remove_punct(word_list):
    punct = [".", ",", "'", "-", "(", ")", "/", "!", "?", "\"", "[", "]", ":"]
    new_list = []

    for words in word_list:
        for word in words:
            if word not in punct:
                new_list.append(str(word))
    return new_list

# lemmatizes words
def lemmatize(final_word_list):
	for words,final in zip(word_list_detailed,final_word_list):
		for i,(word,fin) in enumerate(zip(words,final)):
			if fin in word.text:
				if(len(fin)==1):
					final[i]=fin;
				else:
					final[i]=word.lemma;

def label_parse_subtrees(parent_tree):
    tree_traversal_flag = {}

    for pos in parent_tree.treepositions():
        tree_traversal_flag[pos] = 0
    return tree_traversal_flag

# insert noun at first position
def handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    # if Noun it there and not traversed insert it first in a tree
    if tree_traversal_flag[sub_tree.treeposition()] == 0 and tree_traversal_flag[sub_tree.parent().treeposition()] == 0:
        tree_traversal_flag[sub_tree.treeposition()] = 1
        modified_parse_tree.insert(i, sub_tree)
        i = i + 1
    return i, modified_parse_tree


# handles if verb/proposition in tree after noum
def handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    # if it is Verb or Proportion recursively check for Noun clause
    for child_sub_tree in sub_tree.subtrees():
        if child_sub_tree.label() == "NP" or child_sub_tree.label() == 'PRP': # checks if it it noun or pronoun it indicate there is verb in it.
            if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                tree_traversal_flag[child_sub_tree.treeposition()] = 1
                modified_parse_tree.insert(i, child_sub_tree)
                i = i + 1
    return i, modified_parse_tree


# Function to convert spaCy token to nltk Tree
def to_nltk_tree(token):
    # Create an nltk Tree with the token as the root and its children as branches
    return Tree(token.text, [to_nltk_tree(child) for child in token.children])

# Modify tree according to POS
def modify_tree_structure(parent_tree):
    tree_traversal_flag = label_parse_subtrees(parent_tree)
    modified_parse_tree = Tree('ROOT', [])
    i = 0
    for sub_tree in parent_tree.subtrees():
        if sub_tree.label() == "NP":
            i, modified_parse_tree = handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)
        if sub_tree.label() == "VP" or sub_tree.label() == "PRP":
            i, modified_parse_tree = handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)

    # recursively check for omitted clauses to be inserted in tree
    for sub_tree in parent_tree.subtrees():
        for child_sub_tree in sub_tree.subtrees():
            if len(child_sub_tree.leaves()) == 1: # check is it has a leaf node
                if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                    tree_traversal_flag[child_sub_tree.treeposition()] = 1
                    modified_parse_tree.insert(i, child_sub_tree)
                    i = i + 1

    return modified_parse_tree

def reorder_eng_to_isl(input_string):
    doc = nlp(input_string)
    root_token = [token for token in doc if token.head == token][0]  # Find the root token
    parse_tree = Tree('ROOT', [to_nltk_tree(root_token)])
    # Modify the tree structure as needed
    modified_parse_tree = modify_tree_structure(parse_tree)
    # Get the parsed sentence
    parsed_sent = [token.text for token in doc]

    return parsed_sent

# final word list
final_words= [];
# final word list that is detailed(dict)
final_words_detailed=[];


# pre processing text
def pre_process(text):
	final_words.extend(filter_words(word_list));
	lemmatize(final_words)


# checks if sigml file exists of the word if not use letters for the words
def final_output(input):
	valid_words=open("words.txt",'r').read()
	valid_words=valid_words.split('\n')
	fin_words=[]
	for word in input:
		word=word.lower()
		if(word not in valid_words):
			for letter in word:
				# final_string+=" "+letter
				fin_words.append(letter)
		else:
			fin_words.append(word)
	return fin_words

final_output_in_sent=[];
final_response = []
# convert final list with letters sepearated
def convert_to_final():
	for words in final_words:
		final_output_in_sent.append(final_output(words))


def take_input(text):
    if(len(text) == 1):
        return [text]
        
    text = text.strip().replace("\n", "").replace("\t", "")
    if len(text) == 1:
        return nlp(text)
    processed_text = " ".join(word.capitalize() for word in text.split(".")) + "."
    doc = nlp(processed_text)
    return convert(doc)

def convert(some_text):
    convert_to_sentence_list(some_text)
    convert_to_word_list(sent_list_detailed)

    for i,words in enumerate(word_list):
        word_list[i]=reorder_eng_to_isl(str(words))
    pre_process(some_text)
    convert_to_final()
    final_response = remove_punct(final_output_in_sent)
    # print("Final List : ", final_response)
    
    return final_response

def print_lists():
	print("--------------------Word List------------------------");
	print(word_list)
	print("--------------------Final Words------------------------");
	print(final_words)
	print("---------------Final sentence with letters--------------")
	print(final_output_in_sent)

# clears all the list after completing the work
def clear_all():
	sent_list.clear();
	sent_list_detailed.clear();
	word_list.clear();
	word_list_detailed.clear();
	final_words.clear();
	final_words_detailed.clear();
	final_output_in_sent.clear();
	final_words_dict.clear();


# dict for sending data to front end in json
final_words_dict = {};

# while True:
#     text = input("Enter Text : ")
#     final_response = take_input(text)
#     print("Final Response : \n", final_response)
#     clear_all()
