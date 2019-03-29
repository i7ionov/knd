def convert_request(request):
    """
    Метод конвертирует request в словарь удобный для дальнейшей работы
    :param request: Пример:
    <QueryDict: {'field': ['houses'],
                'filter:inspection:doc_number:exact': ['1'],
                'filter:inspection:houses:contains': ['1;1'],
                'table': ['inspections.disposal']},
                'count:document:doc_type:exact': ['проверка'],
                'fields_to_count': ['document', 'house']>
    Уточнение по ключу disposal:houses:contains:
    здесь в ['1;1'] первая цифра означает pk объекта Address, вторая цифра - номер дома.
    в параметре fields_to_count передается список полей для подсчета
    :return: Пример:
    {'filter': {'inspection': {'houses': {'contains': ['1;1']}, 'doc_number': {'exact': ['1']}}},
    'count': {'document': {'doc_type': {'exact': ['проверка']}}},
    'fields_to_count': ['document', 'house']}
    """
    request_post = {}
    for param in request.POST:
        if ':' in param:
            param_split = param.split(':')
            if param_split[0] in request_post:
                if param_split[1] in request_post[param_split[0]]:
                    if param_split[2] in request_post[param_split[0]][param_split[1]]:
                        request_post[param_split[0]][param_split[1]][param_split[2]][param_split[3]] = request.POST.getlist(param)
                    else:
                        request_post[param_split[0]][param_split[1]][param_split[2]] = {param_split[3]: request.POST.getlist(param)}
                else:
                    request_post[param_split[0]][param_split[1]] = {param_split[2]: {param_split[3]: request.POST.getlist(param)}}
            else:
                request_post[param_split[0]] = {param_split[1]: {param_split[2]: {param_split[3]: request.POST.getlist(param)}}}
        elif param == 'address_list':
            request_post['houses'] = request.POST.getlist(param)
        elif param == 'fields_to_count':
            request_post['fields_to_count'] = request.POST.getlist(param)
    return request_post
