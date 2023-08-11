# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2021
#
# Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Stuart E. Middleton
# Created Date : 2021/01/29
# Project : Teaching
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, codecs, json, math, time, warnings, re, logging
warnings.simplefilter( action='ignore', category=FutureWarning )

import nltk, numpy, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )
logger.info('logging started')

def exec_regex_questions( file_chapter = None ) :

    # CHANGE BELOW CODE TO USE REGEX TO LIST ALL QUESTIONS IN THE CHAPTER OF TEXT (task 2)

    # Input >> www.gutenberg.org sourced plain text file for a chapter of a book
    # Output >> questions.txt = plain text set of extracted questions. one line per question.

    # hardcoded output to show exactly what is expected to be serialized

    text = ''
    for line in codecs.open(file_chapter, "r", encoding="utf-8"):
        text += line

    text = re.sub(r'[\r\n]+?',' ',text)
    answer_2 = re.findall(r'(?:[?.!;:\]})]\s|\s*[\'‘"“])'
                          r'([\w\s,\'’\-]+\?)',text)
    answer_2 = [txt.strip() for txt in answer_2]






    setQuestions = set(answer_2)

    # DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

    writeHandle = codecs.open( 'questions.txt', 'w', 'utf-8', errors = 'replace' )
    for strQuestion in setQuestions :
        writeHandle.write( strQuestion + '\n' )
    writeHandle.close()

if __name__ == '__main__':
    if len(sys.argv) < 4 :
        raise Exception( 'missing command line args : ' + repr(sys.argv) )
    ontonotes_file = sys.argv[1]
    book_file = sys.argv[2]
    chapter_file = sys.argv[3]

    logger.info( 'ontonotes = ' + repr(ontonotes_file) )
    logger.info( 'book = ' + repr(book_file) )
    logger.info( 'chapter = ' + repr(chapter_file) )

    # DO NOT CHANGE THE CODE IN THIS FUNCTION

    exec_regex_questions( chapter_file )

