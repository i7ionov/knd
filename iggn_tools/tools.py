# экранирование нежелательных символов
def screen(string):
    result = str(string)
    if result:
        # замена "абв" на «абв»
        while "\"" in result:
            i = result.index("\"")
            if (len(result) > i+1) and not (result[i+1].isspace()):
                result = result[:i] + "«" + result[i+1:]
            elif i > 0 and not result[i-1].isspace():
                result = result[:i] + "»" + result[i + 1:]
            else:
                result = result[:i] + "»" + result[i + 1:]
        result = result.replace("\\", "/")
        result = result.replace("'", "`")
    return result


# инкрементирует номер документа
# 7 преобразует в 7/1
# 7/1 преобразует в 7/2
def increment_doc_number(string):
    try:
        m_doc_num = string.split('/')
        if len(m_doc_num) > 1:
            return '/'.join(m_doc_num[0:-1]) + '/' + str(int(m_doc_num[-1]) + 1)
        else:
            return string + '/' + '1'
    except:
        return string
