# -*- coding: utf-8 -*-
"""Module to receive and process data from a user"""

import re

from unidecode import unidecode

from P7_02_site.grandpy.grandpyconfig import Scrap


class UserFetching:
    """Class to encapsulate getting data from a user"""

    @staticmethod
    def ask_grandpy():
        """Receive user question"""
        user_question = input()
        return user_question


class QuestionParsing:
    """Class to analyse given question from a user"""

    @staticmethod
    def extract_relevant_sentence_from(question):
        """Get relavant sentence from user query"""
        # convert on lower case
        lowered_question = question.lower()
        # get rid of accents
        accent_free_question = unidecode(lowered_question)
        # extract sentence containing key word with regular expression
        # use of a positive lookbehind assertion regex
        pattern = re.compile(r"("
                             "((?<=trouv)(.|\n)+)|"
                             "((?<=localis)(.|\n)+)|"
                             "((?<=situ)(.|\n)+)|"
                             "((?<=plac)(.|\n)+)|"
                             "((?<=reper)(.|\n)+)|"
                             "((?<=resid)(.|\n)+)|"
                             "((?<=log)(.|\n)+)|"
                             "((?<=position)(.|\n)+)|"
                             "((?<=nich)(.|\n)+)|"
                             "((?<=instal)(.|\n)+)|"
                             "((?<=dissimul)(.|\n)+)|"
                             "((?<=cach)(.|\n)+)|"
                             "((?<=montr)(.|\n)+)|"
                             "((?<=ou est)(.|\n)+)|"
                             "((?<=adresse d)(.|\n)+)"
                             ")")
        match = pattern.search(accent_free_question)

        if match:
            # get the matching result as a string
            return match.group()
        return "Oups, la question n'est claire !"

    @staticmethod
    def extract_irrelevant_words_from(sentence):
        """Get rid of predefined irrelevant words on a given sentence"""
        # split the sentence on any non word separator
        sentence_word_list = re.split(r'\W+', sentence)
        # get out irrelevant words from the list formed by the split
        sentence_word_list_cleaned = [
            word for word in sentence_word_list if word not in Scrap.UNACCENTED_STOP_WORDS]
        # recreate the string with join
        cleaned_sentence = (' ').join(sentence_word_list_cleaned)

        return cleaned_sentence


def main():

    question = QuestionParsing.extract_relevant_sentence_from("Bonsoir Grandpy, montre Tunis?")
    if question:
        key_word = QuestionParsing.extract_irrelevant_words_from(question)
        return key_word
    else:
        return None

if __name__ == "__main__":
    main()
