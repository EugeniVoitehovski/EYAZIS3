import re

import pymorphy2

from printDocumets import printExpectation
from readFromFile import readFromFile
from saveInFile import SaveFile


def classicDocument():
    result = 'В разработке!'
    print(result)
    readFromFile()
    SaveFile(result, type)
    printExpectation()


def listDocument():
    # инициализируем словарь
    dict = {}
    # читаем файл и делим на слова
    words = readFromFile().split()
    # инициализируем счётчик
    counter = 0
    # создаём анализатор
    morph = pymorphy2.MorphAnalyzer()
    # подсчитываем количество вхождений именно лексемы в текст
    counted_lexemes = count_lexemes(words)
    # идём по каждому слову в тексте
    for word in words:
        # очищаем слово от сех символов, не относящихся к алфавиту
        word = re.sub('(\W|[0-9])', '', word)
        # если после очистки длина слова 2 и меньше символа, то идём дальше, т.к. скорее всего это был знак припинания,
        # или просто местоимение/предлог, сдвигаем счётчик и идём дальше
        if len(word) > 2:
            # парсим слово анализатором
            word_morph = morph.parse(word)[0]
            # достаём лексему
            lexeme = word_morph.normal_form
            # если эта лексема встречается в тексте больше 10 раз, начинаем извлечение словосочетания (пары слов)
            # если нет, сдвигаем счётчик и идём дальше
            if counted_lexemes.get(lexeme, 0) > 10:
                # если эта лексема  не в словаре, добавляем и инициализируем пустым списком
                if lexeme not in dict.keys():
                    dict[lexeme] = []
                try:
                    next_word = None
                    # переменная для отслеживания текущего положения за счётчиком counter
                    wrong_word_type_counter = 0
                    # проверяем последующие слова на знаки припинания и всё, что меньше 2-х символов. Всё, что меньше 2-х
                    # скипаем до следующего слова
                    while True:
                        wrong_word_type_counter = wrong_word_type_counter + 1
                        next_word = words[counter + wrong_word_type_counter]
                        next_word = re.sub('(\W|[0-9])', '', next_word)
                        if len(next_word) > 2:
                            break
                    # если следующее слово не копия текущего, добавляем это словосочетание в список лексемы
                    if next_word is not word:
                        dict[lexeme].append(word + ' ' + next_word)
                    # сдвигаем счётчик на следующее слово
                    counter = counter + 1
                # Если падает IndexError, значит мы вышли за границы текста и прошли его конец.
                except IndexError:
                    # text end
                    pass
            else:
                counter = counter + 1
        else:
            counter = counter + 1
    # выводим в консоль то, что получилось
    for key, value in dict.items():
        if len(value) > 0:
            print(key + ' -> ' + str(value))


def count_lexemes(words):
    counter = {}
    morph = pymorphy2.MorphAnalyzer()
    for word in words:
        temp = re.sub('(\W|[0-9])', '', word)
        if len(temp) > 2:
            lexeme = morph.parse(temp)[0].normal_form
            counter[lexeme] = counter.get(lexeme, 0) + 1
    return counter


def extract_word_Pair(dict, words, counter, word, lexeme):
    try:
        next_word = None
        wrong_word_type_counter = 0

        while True:
            wrong_word_type_counter = wrong_word_type_counter + 1
            next_word = words[counter + wrong_word_type_counter]
            next_word = re.sub('(\W|[0-9])', '', next_word)
            if len(next_word) > 2:
                break

        if next_word is not word:
            dict[lexeme].append(word + ' ' + next_word)
        counter = counter + 1

    except IndexError:
        # text end
        pass
