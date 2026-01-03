import spacy
# !python -m spacy download en_core_web_sm

nlp = spacy.load('en_core_web_sm')

sent_list = []
word_list = []

# Not Needed in ISL
stop_words = set(["am","are","is","was","were","be","being","been","have","has","had", "does","did","could","should","would","can","shall","will","may","might","must","let"])

# WH words
wh_words = set(["who", "whom", "what", "which", "when", "where", "why", "how"])

# Punctuation
punct = [".", ",", "'", "-", "(", ")", "/", "!", "?", "\"", "[", "]", ":", ";"]

ISL_Rule = {
  "intj": [],
  "nsubj": [],
  "poss": [],
  "amod": [],
  "dobj": [],
  "amod": [],
  "pobj": [],
  "amod": [],
  "iobj": [],
  "prep": [],
  "nummod": [],
  "attr": [],
  "dative": [],
  "advmod": [],
  "ROOT": [],
  "neg": [],
  "wh": []
}

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

# def clear_all():
#   final_response.clear()



def get_isl_text(text):
  final_response = []
  doc = nlp(text)

  for sent in doc.sents:
    for token in sent:
      if(token.text in stop_words or token.text in punct):
        continue
      tag = token.dep_
      if(tag == "intj"):
        ISL_Rule["intj"].append(token.lemma_)
      elif(tag == "poss"):
        ISL_Rule["poss"].append(token.lemma_)
      elif(token.text in wh_words):
        ISL_Rule["wh"].append(token.lemma_)
      elif(tag == "amod"):
        ISL_Rule["amod"].append(token.lemma_)
      elif(tag == "nsubj"):
        ISL_Rule["nsubj"].append(token.lemma_)
      elif(tag == "dobj"):
        ISL_Rule["dobj"].append(token.lemma_)
      elif(tag == "advmod"):
        ISL_Rule["advmod"].append(token.lemma_)
      elif(tag == "pobj"):
        ISL_Rule["pobj"].append(token.lemma_)
      elif(tag == "iobj"):
        ISL_Rule["iobj"].append(token.lemma_)
      # elif(tag == "prep"):
      #   ISL_Rule["prep"].append(token.lemma_)
      elif(tag == "nummod"):
        ISL_Rule["nummod"].append(token.lemma_)
      elif(tag == "attr"):
        ISL_Rule["attr"].append(token.lemma_)
      elif(tag == "dative"):
        ISL_Rule["dative"].append(token.lemma_)
      elif(tag == "ROOT"):
        ISL_Rule["ROOT"].append(token.lemma_)
      elif(tag == "neg"):
        ISL_Rule["neg"].append(token.lemma_)
      else:
        pass

    # print(ISL_Rule)
    isl_list = []
    # print(ISL_Rule.keys())
    for dep in ISL_Rule.keys():
      if(len(ISL_Rule[dep]) >= 1):
        isl_list.extend(ISL_Rule[dep])
    # print(isl_list)
    for val in ISL_Rule.values():
      val.clear()
    
    final_response.extend(final_output(isl_list))

  return final_response
