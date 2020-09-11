""" Module for testing parser module"""

import sys
print(sys.path)

from ..grandpy.utils.config import Scrap

from ..grandpy.utils.parser import QuestionParsing

def test_extract_relevant_sentence_from_lower_the_sentence():
	result = QuestionParsing.extract_relevant_sentence_from("Bonjour grandpy, où est Paris stp ?")
	assert result.islower()

def test_extract_relevant_sentence_from_gets_rid_of_accent():
	result = QuestionParsing.extract_relevant_sentence_from("Bonjour grandpy, où est Paris stp ?")
	accent_list = ["é", "è", "â", "î", "ô", "ñ", "ü", "ï", "ç"]
	for character in result:
		assert character not in accent_list

def test_extract_relevant_sentence_from_parses_the_sentence():
	result = QuestionParsing.extract_relevant_sentence_from("Bonjour grandpy, où est Paris stp ?")
	guideline_word_list = ["trouv", "localis", "situ", "plac", "reper", "resid", "log", "position", "nich", "instal", "dissimul", "cach", "ou est", "adresse d"]
	for word in guideline_word_list:
		assert word not in result

def test_extract_relevant_sentence_from_could_return_No_result():
	result = QuestionParsing.extract_relevant_sentence_from("Bonjour grandpy, Paris stp ?")
	assert result == "Oups, la question n'est claire !"

def test_extract_irrelevant_words_from_eliminate_irrelevant_words():
	result = QuestionParsing.extract_irrelevant_words_from("la ville de Paris,capitale, stp")
	irrelevant_word_list = Scrap.UNACCENTED_STOP_WORDS
	for word in irrelevant_word_list:
		assert (" " + word + " ") not in result

