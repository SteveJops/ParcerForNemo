import re


def extract_data_by_regex(test_input: str):
    print(test_input)
    inn_regex = re.compile(r' [0-9]{10}–')
    parent_type_regex = re.compile(r'[А-ЯҐЄІЇ][а-яґєії ]* [0-9]{10}')
    name_regex = re.compile(r'[0-9]{10}– [А-ЯҐЄІЇа-яґєії ]*\(')
    inn = re.findall(inn_regex, test_input)[0].replace('\t', '').replace('–', '')
    parent_type = re.findall(parent_type_regex, test_input)[0].split(' ')[0]
    name = re.findall(name_regex, test_input)[0].split('– ')[1].replace('(', '')
    return parent_type, inn, name
