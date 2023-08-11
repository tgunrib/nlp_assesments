import codecs
import re
import sys


def task_1(file_book=None):
    text = ''
    for line in codecs.open(file_book, "r", encoding="utf-8"):
        text += line

    pattern = r'\s*((?i)chapter)?(?:\s*(\d+|\s*M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3}))\.?:?)?\s+(.+)'

    chapter_pattern = re.compile(pattern)

    paragraphs = re.split(r'\r\n\r\n[\r\n]*', text)
    dict = {}
    current_bk = None
    current_vol = None
    currentps = 0
    for i in range(0, len(paragraphs)):
        if re.match(r'\s*BOOK.*', paragraphs[i], flags=re.IGNORECASE):
            current_bk = re.match('\s*(BOOK.*)\.\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
            continue
        if re.match(r'\s*PART.*', paragraphs[i], flags=re.IGNORECASE):
            current_bk = re.match('\s*(PART.*)\.\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
            continue
        if re.match(r'\s*VOLUME.*', paragraphs[i], flags=re.IGNORECASE):
            current_vol = re.match('\s*(VOLUME.*)\.\s*', paragraphs[i], flags=re.IGNORECASE).groups()[0]
            continue
        index = ''
        if current_vol is not None:
            index += '(' + current_vol + ')'
        if current_bk is not None:
            index += '(' + current_bk + ')'
        result = chapter_pattern.search(paragraphs[i])
        if result is not None:
            if result.groups()[0] is not None:
                if result.groups()[1] is not None:
                    dict[index + str(result.groups()[1])] = str(result.groups()[2])
            elif result.groups()[1] is not None:
                if re.match(r'\d+|M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})',
                            result.groups()[1]) is not None:
                    dict[index + str(result.groups()[1])] = str(result.groups()[2])




if __name__ == '__main__':
    task_1(sys.argv[1])
