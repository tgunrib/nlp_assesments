import codecs
import re

import sys


def get_file(filename):
    text = ''
    for line in codecs.open(filename, "r", encoding="utf-8"):
        text += line

    find_individual_paragraph = re.split(r'\r\n\r\n[\r\n]*', text)

    """rules to handle
    :param : current_book, current_volume
    find the books/volume:
      Book (number)
      Book (title) - should be a singular sentence with no punctuations
    :param : {}
    find the chapters:
      Chapter (number) 
      Chapter (title) should be a singular sentence with no punctuation
      number (title) should be singular sentence with no punctuations
      title should be a singular sentence with no punctuations
    """

    capital_sentences = '[^a-z\r\n]+'
    singular_titles = r'(([A-Z\d]\w+\s)|(\S{1,3}\s))+s*\n+'
    book = r'\s*((BOOK\s.*)|(Book\s.*)|(Bk\\s..*))'
    volume = r'\s*(Volume.*|VOLUME.*|Vol\..*|VOL\..*)'
    part = r'\s*(Part.*|PART.*|Pt\..*)'
    current_book = None
    current_vol = None
    current_part = None
    chapter_dict = {}
    current_index = None
    for paragraph in find_individual_paragraph:
        if re.match('\s*FOOTNOTES.*|\*\*\* END OF THE PROJECT GUTENBERG .*',paragraph):
            break
        if re.match(book, paragraph):
            current_book = paragraph.strip()
            continue
        if re.match(volume,paragraph):
            current_vol = paragraph.strip()
            continue
        if re.match(part,paragraph):
            current_part = paragraph.strip().replace('\n','').replace('\r','')
        cur_index = ''
        if current_vol is not None:
            cur_index += '(' + current_vol + ')'
        if current_part is not None:
            cur_index += '(' + current_part + ')'
        if current_book is not None:
            cur_index += '(' + current_book + ')'
        if current_index is not None:
            cur_index += current_index
        current = paragraph.split(' ')
        current = list(filter(None, current))
        if(len(current)==0):
            continue
        if re.match(r'\s*(Chapter|CHAPTER|CH|ch)?\s*\d+.+?)', paragraph) or re.fullmatch('\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.?\:?',current[0])\
                or re.match(r'\s*(Chapter|CHAPTER|CH|ch)', paragraph):
            if re.fullmatch('(Chapter|CHAPTER|ch|Ch)', current[0]):
                if len(current)<2:
                    break
                if len(current)<=2:
                    cur_index += re.sub('.', '', current[1])
                    continue
                else:
                    cur_index += re.sub('.', '', current[1])
                    chapter_dict[cur_index] = ' '.join(current[2:]).strip()
                    continue
            if re.match('(\s*\d+)', current[0]) or re.match(
                    '\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.?\:?', current[0]):
                if len(current) > 1 and re.fullmatch(singular_titles,current[1]):
                    cur_index += re.sub('.','',current[1])
                    chapter_dict[cur_index] = ' '.join(current[1:])

        elif re.match(capital_sentences, paragraph) or re.match(singular_titles, paragraph):
            if current_index is None:
                chapter_dict[cur_index + str(len(chapter_dict))] = paragraph.strip()
            else:
                chapter_dict[cur_index] = paragraph.strip()
    return chapter_dict




# print(chapter_dict)


if __name__ == '__main__':
    get_file(sys.argv[1])



    find_individual_paragraph = re.split(r'\r\n\r\n[\r\n]*', text)

    book = r'\s*((BOOK\s.*)|(Book\s.*)|(Bk\.\s.*))'
    volume = r'\s*(Volume.*|VOLUME.*|Vol\..*|VOL\..*)'
    part = r'\s*(Part.*|PART.*|Pt\..*)'
    current_book_part = None
    current_vol = None
    chapter_dict = {}
    current_index = None

    for i in range(0, len(find_individual_paragraph)):
        cur_index = ''
        if re.match(book, find_individual_paragraph[i]):
            current_book_part = find_individual_paragraph[i].strip()
            continue
        if re.match(volume, find_individual_paragraph[i]):
            current_vol = find_individual_paragraph[i].strip()
            continue
        if re.match(part, find_individual_paragraph[i]):
            current_book_part = find_individual_paragraph[i].strip()
            continue
        if current_vol is not None:
            cur_index += '(' + re.sub(r'[^\w\s]', '', current_vol) + ')'
        if current_book_part is not None:
            cur_index += '(' + re.sub(r'[^\w\s]', '', current_book_part)+ ')'

        current_paragraph = re.split(' |\r|\n', find_individual_paragraph[i].strip())
        current_paragraph = list(filter(None, current_paragraph))
        if re.match(r'\s*(Chapter|CHAPTER|CH|ch)?(\s*\d+.*?)', find_individual_paragraph[i]):
            if len(current_paragraph) > 1 and re.fullmatch(r'\d+\.?\:?\s*', current_paragraph[1]):
                index = re.findall('\d+', current_paragraph[1])
                title = ' '.join(current_paragraph[2:])
                chapter_dict[cur_index + index[0]] = title
            if re.fullmatch(r'\d+\.?\:?\s*', current_paragraph[0]):
                index = re.findall('\d+', current_paragraph[0])
                if len(current_paragraph) > 1:
                    title = ' '.join(current_paragraph[1:])
                    chapter_dict[cur_index + index[0]] = title

        elif len(current_paragraph) >= 1 and re.fullmatch(
               r'\s*M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\W?', current_paragraph[0]) and \
                current_paragraph[0] != "":
            if current_paragraph[0] == 'I' and len(current_paragraph) > 1 :
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
            index = current_paragraph[1]
            title = ' '.join(current_paragraph[2:])
            chapter_dict[cur_index + index] = title
