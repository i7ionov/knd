def convert_request(request):
    """
    Метод конвертирует request в словарь удобный для дальнейшей работы
    :param request: Пример:
    <QueryDict: {'field': ['houses'],
                'disposal:doc_number:exact': ['1'],
                'disposal:houses:contains': ['1;1'],
                'table': ['inspections.disposal']}>
    Уточнение по ключу disposal:houses:contains:
    здесь в ['1;1'] первая цифра означает pk объекта Address, вторая цифра - номер дома
    :return: Пример:
    {'disposal': {'houses': {'contains': ['1;1']}, 'doc_number': {'exact': ['1']}}}
    """
    request_post = {}
    for param in request.POST:
        if ':' in param:
            param_split = param.split(':')
            if param_split[0] in request_post:
                if param_split[1] in request_post[param_split[0]]:
                    request_post[param_split[0]][param_split[1]][param_split[2]] = request.POST.getlist(param)
                else:
                    request_post[param_split[0]][param_split[1]] = {param_split[2]: request.POST.getlist(param)}
            else:
                request_post[param_split[0]] = {param_split[1]: {param_split[2]: request.POST.getlist(param)}}
        elif param == 'address_list':
            request_post['houses'] = request.POST.getlist(param)
    return request_post
