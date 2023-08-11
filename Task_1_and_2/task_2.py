capital_pattern = re.compile('\s*\W([A-Z][^“!?.]+\?)')
capitals = capital_pattern.findall(text)
c_text = capital_pattern.sub('', text)
pattern = re.compile('\W*\s*([^!?.]+\?)')
first_result = first_pattern.findall(c_text)
n_text = first_pattern.sub('', c_text)

second_result = pattern.findall(n_text)
answer = first_result + second_result + capitals
answer_2 = []
for result in answer:
    if result in first_result and result[0] is not None:
        answer_2.append(re.sub('(\r\n)+|\r|\n', ' ', result[1]).strip())
    elif result in first_result and result[1] is not None:
        answer_2.append(re.sub('(\r\n)+|\r|\n', ' ', result[2]).strip())
    elif result not in first_result:
        answer_2.append(re.sub('(\r\n)+|\r|\n', ' ', result).strip())