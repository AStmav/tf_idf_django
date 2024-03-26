
from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Words
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

import math



def calc_tfidf(text: str) -> list:
    """
    Рассчитывает TF-IDF для текста.

    Параметры:
        text (str): Текст, для которого рассчитывается TF-IDF.

    Возвращает:
        list: Список слов с их TF и IDF.
    """
    # Создание объекта TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    # Применение TF-IDF к текстовым данным
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])

    # Получение списка ключевых слов и их значения TF-IDF для первого документа
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Добавим расчет IDF
    idf_scores = {}

    # Пока у нас только один документ
    num_documents = 1

    for word in feature_names:
        idf_scores[word] = calc_idf(text, word, num_documents)

    # Объединим TF и IDF в один список слов
    words = [{'word': word, 'tf': tf, 'idf': idf_scores[word]} for word, tf in zip(feature_names, tfidf_scores)]
    return words

def calc_idf(text: str, word: str, num_documents: int) -> float:
    """
    Рассчитывает IDF для указанного слова.

    Параметры:
        text (str): Текст, в котором происходит подсчет.
        word (str): Слово, для которого рассчитывается IDF.
        num_documents (int): Общее количество документов.

    Возвращает:
        float: Значение IDF для указанного слова.
    """
    # Количество вхождений слова в текст
    word_count = text.lower().split().count(word.lower())

    if word_count == 0:
        # Если слово не встречается в тексте, IDF будет 0
        return 0
    else:

        # Избегаем деления на ноль
        return math.log(num_documents / (word_count + 1))

def upload_file(request):
    """
    Обработчик загрузки файла.

    Параметры:
        request (HttpRequest): HTTP-запрос.

    Возвращает:
        HttpResponseRedirect | HttpResponse: Редирект или ответ на запрос.
    """
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Вычисление TF-IDF для текста файла
            words = calc_tfidf(text)
            for word in words:
                # Сохранение слова в базу данных вместе с TF и IDF
                Words.objects.create(word=word['word'], tf=word['tf'], idf=word['idf'])
            return redirect('result_view')
    else:
        form = UploadForm()
    return render(request, 'ti_idf/upload_form.html', {'form': form})


def result_view(request):
    """
    Представление для отображения результатов.

    Параметры:
        request (HttpRequest): HTTP-запрос.

    Возвращает:
        HttpResponse: Ответ на запрос с результатами.
    """

    # Получение 50 слов с наибольшим TF
    sorted_keywords = Words.objects.all().order_by('-idf')[:50]
    return render(request, 'ti_idf/result.html', {'keywords': sorted_keywords})

# Create your views here.
