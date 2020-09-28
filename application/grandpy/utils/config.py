#! /usr/bin/env python3
# coding: utf-8

"""Module containing needed cofiguration for GranPy project"""

import re

import string

import os

from unidecode import unidecode


class Scrap:
    """Class to encapsulate selected stop words"""

    OC_STOP_WORD_LIST = ["a", "abord", "absolument", "afin", "ah", "ai",
                         "ailleurs", "ainsi", "ait", "allaient", "allo",
                         "allons", "aie", "anterieures", "aucun",
                         "allô", "alors", "anterieur", "anterieure",
                         "apres", "après", "as", "assez", "attendu", "au",
                         "aucune", "aujourd", "aujourd'hui", "aupres",
                         "aura", "auraient", "aurait", "auront", "aussi",
                         "autre", "auquel", "auxquelles", "bah", "bas",
                         "autrefois", "autrement", "autres", "autrui", "aux",
                         "auxquels", "avaient", "avais", "avait",
                         "avant", "avec", "avoir", "avons", "ayant", "b",
                         "basee", "bat", "beau", "beaucoup", "bien", "bigre",
                         "boum", "celle", "celles-là", "certain",
                         "bravo", "brrr", "c", "car", "ce", "ceci", "cela",
                         "celle-ci", "celle-là", "celles", "celles-ci",
                         "celui", "celui-ci", "celui-là", "cent", "cependant",
                         "certaine", "certaines", "certains", "certes", "ces",
                         "cet", "chacune", "chère",
                         "cette", "ceux", "ceux-ci", "ceux-là", "chacun",
                         "chaque", "cher", "chers", "chez", "chiche", "chut",
                         "chères", "ci", "cinq", "cinquantaine", "cinquante",
                         "cinquantième", "cinquième", "clac", "clic",
                         "combien", "compris", "dans", "depuis",
                         "comme", "comment", "comparable", "comparables",
                         "concernant", "contre", "couic", "crac", "d", "da",
                         "de", "debout", "dedans", "dehors", "deja", "delà",
                         "dernier", "derniere", "derriere", "derrière", "des",
                         "desormais", "deux", "deuxième",
                         "desquelles", "desquels", "dessous", "dessus",
                         "deuxièmement", "devant", "devers", "devra",
                         "different", "différente",
                         "differentes", "differents", "différent",
                         "différentes", "différents", "dire", "directe",
                         "directement", "diverses", "dix", "doit",
                         "dit", "dite", "dits", "divers", "diverse",
                         "dix-huit", "dix-neuf", "dix-sept", "dixième",
                         "doivent", "duquel", "durant", "egalement", "egales",
                         "donc", "dont", "douze", "douzième", "dring", "du",
                         "dès", "désormais", "e", "effet", "egale",
                         "eh", "elle", "elle-même", "elles", "elles-mêmes",
                         "en", "encore", "et", "etant", "exactement",
                         "enfin", "entre", "envers", "environ", "es", "est",
                         "etc", "etre", "eu", "euh", "eux", "eux-mêmes",
                         "excepté", "extenso", "exterieur", "f", "fais",
                         "faisaient", "floc", "hi", "ho", "hue", "hui",
                         "faisant", "fait", "façon", "feront", "fi", "flac",
                         "font", "g", "gens", "h", "ha", "hein", "hem", "hep",
                         "holà", "hop", "hormis", "hors", "hou", "houp",
                         "huit", "huitième", "hum", "hurrah", "hé", "hélas",
                         "i", "il", "juste", "k", "lequel", "les",
                         "ils", "importe", "j", "je", "jusqu", "jusque",
                         "l", "la", "laisser", "laquelle", "las", "le",
                         "lesquelles", "lesquels", "leur", "leurs",
                         "longtemps", "lors", "lès", "m", "ma",
                         "lorsque", "lui", "lui-meme", "lui-même", "là",
                         "maint", "maintenant", "mais", "malgre", "malgré",
                         "maximale", "me", "miennes", "miens",
                         "meme", "memes", "merci", "mes", "mien", "mienne",
                         "mille", "mince", "minimale", "moi", "moi-meme",
                         "moi-même", "moindres", "même", "mêmes",
                         "moins", "mon", "moyennant", "multiple", "multiples",
                         "n", "na", "naturel", "naturelle", "naturelles",
                         "ne", "neanmoins", "ni", "nombreuses",
                         "necessaire", "necessairement", "neuf", "neuvième",
                         "nombreux", "non", "nos", "notamment", "notre",
                         "nous", "nous-mêmes", "o", "oh", "ohé",
                         "nouveau", "nul", "néanmoins", "nôtre", "nôtres",
                         "ollé", "olé", "on", "ont", "onze", "onzième",
                         "ore", "ou", "ouf", "ouias", "ouverts", "o|",
                         "oust", "ouste", "outre", "ouvert", "ouverte",
                         "où", "p", "parlent", "parler",
                         "paf", "pan", "par", "parce", "parfois", "parle",
                         "parmi", "parseme", "partant", "particulier",
                         "particulière", "pense", "permet",
                         "particulièrement", "pas", "passé", "pendant",
                         "personne", "peu", "peut", "peuvent", "peux", "pff",
                         "pfft", "pfut", "plutôt",
                         "pif", "pire", "plein", "plouf", "plus", "plusieurs",
                         "possessif", "possessifs", "possible", "possibles",
                         "pouah", "pour", "prealable", "precisement",
                         "pourquoi", "pourrais", "pourrait", "pouvait",
                         "premier", "première", "premièrement", "pres",
                         "probable", "probante", "puisque", "pur",
                         "procedant", "proche", "près", "psitt", "pu", "puis",
                         "pure", "q", "qu", "quand", "quant", "quant-à-soi",
                         "quanta", "quarante", "quatrièmement", "que",
                         "quatorze", "quatre", "quatre-vingt", "quatrième",
                         "quel", "quelconque", "quelle", "quelles",
                         "quelqu'un", "quelque", "quoi", "quoique",
                         "quelques", "quels", "qui", "quiconque", "quinze",
                         "r", "rare", "rarement", "rares", "relative",
                         "relativement", "restent", "s", "sa",
                         "remarquable", "rend", "rendre", "restant", "reste",
                         "restrictif", "retour", "revoici", "revoilà", "rien",
                         "sacrebleu", "sait", "sans", "sapristi", "sauf",
                         "seize", "selon", "semblable", "semblaient",
                         "semble", "semblent", "se", "sein",
                         "sent", "sept", "septième", "sera", "seraient",
                         "serait", "seront", "sienne", "siennes",
                         "ses", "seul", "seule", "seulement", "si", "sien",
                         "siens", "sinon", "six", "sixième", "soi",
                         "soi-même", "soit", "soixante", "specifiques",
                         "son", "sont", "sous", "souvent", "specifique",
                         "speculatif", "stop", "strictement", "subtiles",
                         "suffisant", "suivante", "sur", "surtout",
                         "suffisante", "suffit", "suis", "suit", "suivant",
                         "suivantes", "suivants", "suivre", "superpose",
                         "t", "ta", "tac", "tant", "tardive", "te", "tel",
                         "telle", "tellement", "tente", "tes", "tic",
                         "telles", "tels", "tenant", "tend", "tenir",
                         "tien", "tienne", "tiennes", "tiens", "toc", "toi",
                         "toi-même", "ton", "toutefois", "toutes",
                         "touchant", "toujours", "tous", "tout", "toute",
                         "treize", "trente", "tres", "trois", "troisième",
                         "troisièmement", "un", "une", "unes",
                         "trop", "très", "tsoin", "tsouin", "tu", "té", "u",
                         "uniformement", "unique", "uniques", "uns", "v",
                         "va", "vais", "vas", "vive", "vives", "vlan",
                         "vers", "via", "vif", "vifs", "vingt", "vivat",
                         "voici", "voilà", "vont", "vos", "votre", "vous",
                         "vous-mêmes", "vu", "étant", "été", "être",
                         "vé", "vôtre", "vôtres", "w", "x", "y", "z", "zut",
                         "à", "â", "ça", "ès", "étaient", "étais", "était",
                         "ô"]

    # add some irrelevant words as well as all punctuation signs and digits
    ADDITIONAL_WORD_LIST = ["ville",
                            "capitale",
                            "adresse",
                            "svp",
                            "stp",
                            "plait"] + list(string.digits + string.punctuation)
    # concatenate the hole list after removing duplicates
    MODIFIED_LIST = list(set(OC_STOP_WORD_LIST + ADDITIONAL_WORD_LIST))
    # get rid of accents
    UNACCENTED_STOP_WORDS = [unidecode(word) for word in MODIFIED_LIST]


class GmgeoParams:
    """Class to encapsulate parameters for Google geocoding Api"""

    GMGEO_KEY = os.environ.get('Gmgeo_key')
    GMAPS_KEY = os.environ.get('Gmaps_key')
    ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json?"


class WikiParams:
    """Class to encapsulate parameters for Media wiki Api"""

    ENDPOINT = "https://fr.wikipedia.org/w/api.php?"

    @staticmethod
    def define_geosearch_params(latitude, longitude):
        """Define params for searching a page id on Wikimedia API"""
        params = {
            "format": "json",  # response format
            "action": "query",  # action to be realised
            "list": "geosearch",  # query method
            "gsradius": 1000,  # search radius
            "gscoord": f"{latitude}|{longitude}"  # GPS coordinates
        }
        return params

    @staticmethod
    def define_extraction_params(page_id):
        """Define params for extracting data from Wikimedia API"""
        params = {
            "format": "json",  # response format
            "action": "query",  # action to be realised
            "prop": "extracts|info",  # properties for required pages
            "inprop": "url",  # supply url
            "exchars": 1200,  # number of characters
            "explaintext": 1,  # return raw text (without markup)
            "pageids": page_id
        }
        return params


class GmapsParams:
    """Class to encapsulate parameters for Google maps Api"""

    GMAPS_KEY = os.environ.get('Gmaps_key')
