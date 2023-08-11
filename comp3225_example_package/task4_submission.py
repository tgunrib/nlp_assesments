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


def create_dataset(dataset_file, max_files=50):
    # load parsed ontonotes dataset
    readHandle = codecs.open(dataset_file, 'r', 'utf-8', errors='replace')
    str_json = readHandle.read()
    readHandle.close()
    dict_ontonotes = json.loads(str_json)

    # make a training and test split
    list_files = list(dict_ontonotes.keys())
    if len(list_files) > max_files:
        list_files = list_files[:max_files]
    nSplit = math.floor(len(list_files) * 0.99)
    list_train_files = list_files[: nSplit]
    list_test_files = list_files[nSplit:]

    # sent = (tokens, pos, IOB_label)
    list_train = []
    for str_file in list_train_files:
        for str_sent_index in dict_ontonotes[str_file]:
            # ignore sents with non-PENN POS tags
            if 'XX' in dict_ontonotes[str_file][str_sent_index]['pos']:
                continue
            if 'VERB' in dict_ontonotes[str_file][str_sent_index]['pos']:
                continue

            list_entry = []

            # compute IOB tags for named entities (if any)
            ne_type_last = None
            for nTokenIndex in range(len(dict_ontonotes[str_file][str_sent_index]['tokens'])):
                strToken = dict_ontonotes[str_file][str_sent_index]['tokens'][nTokenIndex]
                strPOS = dict_ontonotes[str_file][str_sent_index]['pos'][nTokenIndex]
                ne_type = None
                if 'ne' in dict_ontonotes[str_file][str_sent_index]:
                    dict_ne = dict_ontonotes[str_file][str_sent_index]['ne']
                    if not 'parse_error' in dict_ne:
                        for str_NEIndex in dict_ne:
                            if nTokenIndex in dict_ne[str_NEIndex]['tokens']:
                                ne_type = dict_ne[str_NEIndex]['type']
                                break
                if ne_type != None:
                    if ne_type == ne_type_last:
                        strIOB = 'I-' + ne_type
                    else:
                        strIOB = 'B-' + ne_type
                else:
                    strIOB = 'O'
                ne_type_last = ne_type

                list_entry.append((strToken, strPOS, strIOB))

            list_train.append(list_entry)

    list_test = []
    for str_file in list_test_files:
        for str_sent_index in dict_ontonotes[str_file]:
            # ignore sents with non-PENN POS tags
            if 'XX' in dict_ontonotes[str_file][str_sent_index]['pos']:
                continue
            if 'VERB' in dict_ontonotes[str_file][str_sent_index]['pos']:
                continue

            list_entry = []

            # compute IOB tags for named entities (if any)
            ne_type_last = None
            for nTokenIndex in range(len(dict_ontonotes[str_file][str_sent_index]['tokens'])):
                strToken = dict_ontonotes[str_file][str_sent_index]['tokens'][nTokenIndex]
                strPOS = dict_ontonotes[str_file][str_sent_index]['pos'][nTokenIndex]
                ne_type = None
                if 'ne' in dict_ontonotes[str_file][str_sent_index]:
                    dict_ne = dict_ontonotes[str_file][str_sent_index]['ne']
                    if not 'parse_error' in dict_ne:
                        for str_NEIndex in dict_ne:
                            if nTokenIndex in dict_ne[str_NEIndex]['tokens']:
                                ne_type = dict_ne[str_NEIndex]['type']
                                break
                if ne_type != None:
                    if ne_type == ne_type_last:
                        strIOB = 'I-' + ne_type
                    else:
                        strIOB = 'B-' + ne_type
                else:
                    strIOB = 'O'
                ne_type_last = ne_type

                list_entry.append((strToken, strPOS, strIOB))
            list_test.append(list_entry)
        return list_train, list_test


def names(check):
    names_possibility = "((?:Dr|Mr|Mrs|Miss|Sir|Lord|Lady|King|Professor|Doctor|Madam|Gentleman|Dame)\.?\s*(?:[A-Z]\.?\s?)*(?:[A-Z][a-z0-9\-\.]+\s?)+|(?:[A-Z]\.\s?)+(?:[A-Z][a-z0-9\-\.]+\s?)+)"
    result = re.findall(names_possibility, check)
    result = [re.sub(r'\r|\n|\'|"|“|’', '', word.strip().strip('.').lower(), re.IGNORECASE) for word in result]
    return result


def names_match(text):
    names_possibility = "((?:Dr|Mr|Mrs|Miss|Sir|Lord|Lady|King|Professor|Doctor|Madam|Gentleman|Dame)\.?\s*(?:[A-Z]\.?\s?)*(?:[A-Z][a-z0-9\-\.]+\s?)+|(?:[A-Z]\.\s?)+(?:[A-Z][a-z0-9\-\.]+\s?)+)"
    return re.findall(names_possibility, text)


def preprocess_textfile(filename):
    text = ''
    for line in codecs.open(filename, "r", encoding="utf-8"):
        text += line
    sentences = nltk.sent_tokenize(text)
    word_pos_tags = [nltk.pos_tag(nltk.word_tokenize(word)) for word in sentences]
    lemmatizer = nltk.stem.WordNetLemmatizer()
    # stemmer = nltk.stem.porter.PorterStemmer()
    word_lemmas = []
    sents = names(text)
    for sent in word_pos_tags:
        # word_lemmas.append([(stemmer.stem(word[0]), word[1]) for word in sent])
        word_lemmas.append([(lemmatizer.lemmatize(word[0]), word[1]) for word in sent])
    return word_pos_tags, sents


def task2_word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'word': word,
        'postag': postag,

        # token shape
        'word.lower()': word.lower(),
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.regex()': names_match(word),
        # token suffix
        'word.suffix': word.lower()[-3:],

        # POS prefix
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word_prev = sent[i - 1][0]
        postag_prev = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word_prev.lower(),
            '-1:postag': postag_prev,
            '-1:word.isupper()': word_prev.isupper(),
            '-1:word.istitle()': word_prev.istitle(),
            '-1:word.isdigit()': word_prev.isdigit(),
            '-1:word.suffix': word_prev.lower()[-3:],
            '-1:postag[:2]': postag_prev[:2],
            '-1:word.regex()': names_match(word_prev),
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word_next = sent[i + 1][0]
        postag_next = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word_next.lower(),
            '+1:postag': postag_next,
            '+1:word.isupper()': word_next.isupper(),
            '+1:word.istitle()': word_next.istitle(),
            '+1:word.isdigit()': word_next.isdigit(),
            '+1:word.suffix': word_next.lower()[-3:],
            '+1:postag[:2]': postag_next[:2],
            '+1:word.regex()': names_match(word_next),
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent, word2features_func=None):
    return [word2features_func(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def exec_task(filebook, dataset_file, word2features_func, max_files=10, train_crf_model_func=None, max_iter=100):
    # make a dataset from english NE labelled ontonotes sents
    train_sents, test_sents = create_dataset(dataset_file, max_files=max_files)
    txt_sents, sentences = preprocess_textfile(filebook)
    # tagged_words = [(word, tag) for word, tag in train_sents]

    """fd = nltk.FreqDist(tagged_words)
    smoothing_factor = 1  # Add-one smoothing
    lpd = LidstoneProbDist(fd, smoothing_factor)
    for word_pos_tuple in tagged_words:
        word, pos_tag = word_pos_tuple
        smoothed_prob = lpd.prob(word_pos_tuple)
        word_pos_tuple = (word,pos_tag,smoothed_prob)"""

    # create feature vectors for every sent
    X_train = [sent2features(s, word2features_func=word2features_func) for s in train_sents]
    Y_train = [sent2labels(s) for s in train_sents]
    unsup_text = [sent2features(s, word2features_func=word2features_func) for s in txt_sents]

    X_test = [sent2features(s, word2features_func=word2features_func) for s in test_sents]
    Y_test = [sent2labels(s) for s in test_sents]

    # get the label set
    set_labels = set([])
    for data in [Y_train, Y_test]:
        for n_sent in range(len(data)):
            for str_label in data[n_sent]:
                set_labels.add(str_label)
    labels = list(set_labels)

    # remove 'O' label as we are not usually interested in how well 'O' is predicted
    # labels = list( crf.classes_ )
    labels.remove('O')

    crf = train_crf_model_func(X_train, Y_train, max_iter, labels)
    Y_pred = crf.predict(X_test)
    result_pred = crf.predict(unsup_text)
    # print(len(Y_pred[1]), len(X_test[1]))
    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )

    # macro_scores = sklearn_crfsuite.metrics.flat_classification_report( Y_test, Y_pred, labels=sorted_labels)
    # print( macro_scores )
    result = []
    # print(len(X_test[1]), len(Y_pred[1]))
    for i in range(0, len(result_pred)):
        conlltags = [(word['word'], word['postag'], tg) for tg, word in zip(result_pred[i], unsup_text[i])]
        ne_tree = nltk.chunk.conlltags2tree(conlltags)
        for subtree in ne_tree:
            if type(subtree) == nltk.tree.Tree:
                original_label = subtree.label()
                original_string = " ".join([token for token, pos in subtree.leaves()]).lower().strip()
                result.append((original_string, original_label))
    d = {}
    for value, key in result:
        value = re.sub(r'[\r|\n|\'|"|“|’|\t]+', '', value.strip(), re.IGNORECASE)
        if key in d and value not in d[key] or key not in d:
            d.setdefault(key, []).append(value)

    for value in sentences:
        value = re.sub(r'[\r|\n|\'|"|“|’|\t]+', '', value.strip(), re.IGNORECASE)
        if 'PERSON' in d and value not in d['PERSON'] or 'PERSON' not in d:
            d.setdefault('PERSON', []).append(value)
    return d


def task3_train_crf_model(X_train, Y_train, max_iter, labels):
    # train the basic CRF model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=max_iter,
        all_possible_transitions=False,
    )
    crf.fit(X_train, Y_train)
    return crf


def exec_ner(file_chapter=None, ontonotes_file=None):
    # CHANGE CODE BELOW TO TRAIN A NER MODEL AND/OR USE REGEX GENERATE A SET OF BOOK CHARACTERS AND FILTERED SET OF
    # NE TAGS (task 4)

    # Input >> www.gutenberg.org sourced plain text file for a chapter of a book
    # Output >> characters.txt = plain text set of extracted character names. one line per character name.

    # hardcoded output to show exactly what is expected to be serialized (you should change this)
    # only the allowed types for task 4 PERSON will be serialized
    dictNE = exec_task(file_chapter, ontonotes_file, word2features_func=task2_word2features,
                       train_crf_model_func=task3_train_crf_model)
    # DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

    # write out all PERSON entries for character list for subtask 4
    writeHandle = codecs.open('characters.txt', 'w', 'utf-8', errors='replace')
    if 'PERSON' in dictNE:
        for strNE in dictNE['PERSON']:
            writeHandle.write(strNE.strip().lower() + '\n')
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

    exec_ner(chapter_file, ontonotes_file)
