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

warnings.simplefilter(action='ignore', category=FutureWarning)

import nltk, numpy, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger.info('logging started')


def exec_regex_toc(file_book=None):
    # CHANGE BELOW CODE TO USE REGEX TO BUILD A TABLE OF CONTENTS FOR A BOOK (task 1)

    # Input >> www.gutenberg.org sourced plain text file for a whole book
    # Output >> toc.json = { <chapter_number_text> : <chapter_title_text> }

    # hardcoded output to show exactly what is expected to be serialized
    text = ''
    for line in codecs.open(file_book, "r", encoding="utf-8"):
        text += line

    find_individual_paragraph = re.split(r'\r\n\r\n[\r\n]*', text)

    book = r'\s*((BOOK\s.*)|(Book\s.*)|(Bk\.\s.*))'
    volume = r'\s*(Volume.*|VOLUME.*|Vol\..*|VOL\..*)'
    part = r'\s*(Part.*|PART.*|Pt\..*)'
    current_book = None
    current_part = None
    current_vol = None
    chapter_dict = {}


    for i in range(0, len(find_individual_paragraph)):
        cur_index = ''
        if re.match(book, find_individual_paragraph[i]):
            current_part = find_individual_paragraph[i].strip()
            continue
        if re.match(volume, find_individual_paragraph[i]):
            current_vol = find_individual_paragraph[i].strip()
            continue
        if re.match(part, find_individual_paragraph[i]):
            current_part = find_individual_paragraph[i].strip()
            continue
        if current_vol is not None:
            cur_index += '(' + re.sub(r'[^\w\s]', '', current_vol) + ')'
        if current_book is not None:
            cur_index += '(' + re.sub(r'[^\w\s]', '', current_book)+ ')'
        if current_part is not None:
            index += '(' + current_part + ') '

        current_paragraph = re.split(' |\r|\n', find_individual_paragraph[i].strip())
        current_paragraph = list(filter(None, current_paragraph))
        if re.match(r'\s*(Chapter|CHAPTER|CH|ch)?(\s*\d+.*?)', find_individual_paragraph[i]):
            if len(current_paragraph) > 1 and re.fullmatch(r'\d+\.?\:?\s*', current_paragraph[1]) and re.fullmatch(r'\s*(Chapter|CHAPTER|CH|ch)',current_paragraph[0]):
                index = re.findall('\d+', current_paragraph[1])
                c_index = re.sub(r'[^\w\s]', '', index[0])
                if len(current_paragraph) > 2:
                    title = ' '.join(current_paragraph[2:])
                    chapter_dict[cur_index + c_index] = title
                if len(current_paragraph) == 2:
                    chapter_dict[cur_index + c_index] = None
            if re.fullmatch(r'\d+\.?\:?\s*', current_paragraph[0]):
                index = re.findall('\d+', current_paragraph[0])
                if len(current_paragraph) > 1:
                    c_index = re.sub(r'[^\w\s]', '', index[0])
                    title = ' '.join(current_paragraph[1:])
                    chapter_dict[cur_index + c_index] = title


        elif len(current_paragraph) >= 1 and re.fullmatch(
               r'\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W?', current_paragraph[0]) and \
                current_paragraph[0] != "":
            if current_paragraph[0] == 'I' and len(current_paragraph) > 1:
                continue
            if len(re.findall(r'\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W?',
                              ' '.join(current_paragraph))) > 1:
                continue
            index = re.findall('\d+', current_paragraph[0])
            title = ' '.join(current_paragraph[1:])
            chapter_dict[cur_index + index[0]] = title
        elif len(current_paragraph) > 1 and re.fullmatch(r'\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W?',
                                                         current_paragraph[1]) and re.fullmatch(
                                                         r'\s*(Chapter|CHAPTER|CH|ch)?', current_paragraph[0]):
            index = re.sub(r'[^\w\s]', '', current_paragraph[1])
            title = ' '.join(current_paragraph[2:])
            c_index = re.sub(r'[^\w\s]', '', index[0])
            chapter_dict[cur_index + c_index] = title

    dictTOC = chapter_dict

    # DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

    writeHandle = codecs.open('toc.json', 'w', 'utf-8', errors='replace')
    strJSON = json.dumps(dictTOC, indent=2)
    writeHandle.write(strJSON + '\n')
    writeHandle.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise Exception('missing command line args : ' + repr(sys.argv))
    ontonotes_file = sys.argv[1]
    book_file = sys.argv[2]
    chapter_file = sys.argv[3]

    logger.info('ontonotes = ' + repr(ontonotes_file))
    logger.info('book = ' + repr(book_file))
    logger.info('chapter = ' + repr(chapter_file))

    # DO NOT CHANGE THE CODE IN THIS FUNCTION

    exec_regex_toc(book_file)
