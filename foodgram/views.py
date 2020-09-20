from django.shortcuts import render


def author(request):
    """Страница об исполнителе проекта"""

    headline = 'Об авторе'
    text = 'Моя муза и главный любитель пожрать'
    jam = True

    return render(request, 'about.html', {
        'text': text,
        'headline': headline,
        'jam': jam})


def tech(request):
    """Страница о технологиях, используемых в проекте"""

    headline = 'Технологии'
    text = ''
    tech = True

    return render(request, 'about.html', {
        'text': text,
        'headline': headline,
        'tech': tech})


def page_not_found(request, exception):
    """Ошибка 404"""
    return render(request, '404.html', {'path': request.path}, status=404)


def server_error(request):
    """Ошибка 500"""
    return render(request, '500.html', {'path': request.path}, status=500)
