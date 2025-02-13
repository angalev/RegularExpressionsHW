import csv
import re


def correct_names(lastname, firstname, surname, organization, position, phone, email):
    namelist = []
    result = {}
    if lastname.split(' '):
        namelist.extend(lastname.split())
    if firstname.split(' '):
        namelist.extend(firstname.split())
    if surname.split(' '):
        namelist.extend(surname.split(' '))
    names = list(filter(None, map(str.strip, namelist)))
    if len(names) == 3:
        result = {"lastname" : names[0],
                  "firstname" : names[1],
                  "surname" : names[2],
                  "organization" : organization,
                  "position" : position,
                  "phone" : phone,
                  "email" : email}
    if len(names) == 2:
        result = {"lastname" : names[0],
                  "firstname" : names[1],
                  "surname" : '',
                  "organization" : organization,
                  "position" : position,
                  "phone" : phone,
                  "email" : email}
    return result

def merge_dics(dic1, dic2):
    merged_dic = {}
    for key in dic1.keys():
        if dic1[key] != dic2[key]:
            merged_dic[key] = dic1[key]+ dic2[key]
        else:
            merged_dic[key] = dic1[key]
    return merged_dic

def del_duplicate(list):
    merged_data = []
    while list:
        elem = list.pop(0)
        lastname_double = [item for item in list if item['lastname'] == elem['lastname']]
        firstname_double = [item for item in list if item['firstname'] == elem['firstname']]
        if lastname_double != [] and firstname_double != []:
            merged_data.append(merge_dics(elem, *lastname_double))
            for row in list:
                if row['lastname'] == elem['lastname']:
                    ind = list.index(row)
            del list[ind]
        else:
            merged_data.append(elem)
    return merged_data


if __name__=="__main__":
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        data = list(csv.reader(f))
        dics = []
        for i in range(1, len(data)):
            dics.append(dict(zip(data[0], data[i])))
# 1 Исправление положения имён
    new_data = []
    for dic in dics:
        new_data.append(correct_names(**dic))
    print(*new_data, sep='\n', end='\n\n')

# 2 Исправление дубликатов
    data = del_duplicate(new_data)
    print(*data, sep='\n')

# 3 Исправление телефонных номеров
    pattern = r"(\+7|8)\s*\(?(\d{3})\)?[-\s]?(\d{3})?[-\s]?(\d{2})?[-\s]?(\d{2})\s?\(?(доб.)?\s?(\d*)\)?"
    pattern_subs = r"+7(\2)\3-\4-\5 \6\7"
    for elem in data:
        elem["phone"] = re.sub(pattern, pattern_subs, elem["phone"]).rstrip()
    print()
    print(*data, sep='\n')

# Запись в файл
    with open('phonebook.csv','w+', encoding='UTF-8') as f:
        fieldnames = list(data[0].keys())
        datawriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames, lineterminator='\n')
        datawriter.writeheader()
        datawriter.writerows(data)

