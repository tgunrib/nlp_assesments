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

def exec_regex_toc( file_book = None ) :

	# CHANGE BELOW CODE TO USE REGEX TO BUILD A TABLE OF CONTENTS FOR A BOOK (task 1)

	# Input >> www.gutenberg.org sourced plain text file for a whole book
	# Output >> toc.json = { <chapter_number_text> : <chapter_title_text> }

	# hardcoded output to show exactly what is expected to be serialized
	text = ''
	for line in codecs.open(file_book, "r", encoding="utf-8"):
		text += line

	find_individual_paragraph = re.split(r'\r\n\r\n[\r\n]*', text)

	dictTOC = {}
	text = ''
	for line in codecs.open(file_book, "r", encoding="utf-8"):
		text += line

	pattern = r'\s*((?i)chapter)?\s*(\d+|(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3}))\.?:?\s*(.*)'

	chapter_pattern = re.compile(pattern)

	paragraphs = re.split(r'\r\n\r\n[\r\n]+', text)
	dict = {}
	current_bk = None
	current_vol = None
	current_part = None
	for i in range(0, len(paragraphs)):
		if re.match('\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*',paragraphs[i]):
			break
		if re.match(r'(\s*(The?)\s*\S{4,7}BOOK\s.*)|(Book.*)', paragraphs[i], flags=re.IGNORECASE):
			current_bk = re.match('\s*(.*)\.?\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
			continue
		if re.match(r'(\s*(The?)\s*\S{4,7}Part\s.*)|(Part.*)', paragraphs[i], flags=re.IGNORECASE):
			current_part = re.match('\s*(.*)\.?\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
			continue
		if re.match(r'(\s*(The?)\s*\S{4,7}Volume\s.*)|(Volume.*)', paragraphs[i], flags=re.IGNORECASE):
			current_vol = re.match('\s*(.*)\.?\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
			continue
		index = ''
		if current_vol is not None:
			index += '(' + current_vol + ') '
		if current_bk is not None:
			index += '(' + current_bk + ') '
		if current_part is not None:
			index += '(' + current_part + ') '
		result = chapter_pattern.search(paragraphs[i])
		if result is not None:
			if result.groups()[0] is not None:
				if (re.match('I|L|M|X|V|C',result.groups()[1]) and re.match('[^A-Z].', result.groups()[2])):
					continue
				if result.groups()[1] is not None:
					dict[index + str(result.groups()[1])] = str(result.groups()[2]).strip()
			elif result.groups()[1] is not None:
				if re.fullmatch(r'\d+|(?=.)(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})',result.groups()[1]) is not None:
					if(re.match('I|L|M|X|V|C',result.groups()[1]) and re.match('[^A-Z].', result.groups()[2])):
						continue
					dict[index + str(result.groups()[1])] = str(result.groups()[2])

	dictTOC = dict

	# DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

	writeHandle = codecs.open( 'toc.json', 'w', 'utf-8', errors = 'replace' )
	strJSON = json.dumps( dictTOC, indent=2 )
	writeHandle.write( strJSON + '\n' )
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

	exec_regex_toc( book_file )
