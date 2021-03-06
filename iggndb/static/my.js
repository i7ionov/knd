function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addTab(control, title, url, add_existing = false) {

    if (!add_existing && $(control).tabs('exists', title)) {
        $(control).tabs('select', title);
    } else {
        $.get(url, function (data) {
            $(control).tabs('add', {
                title: title,
                content: data,
                closable: true
            });
        });
    }
}


function openFileDialog(uid, parent_id, model) {
    $.post('/file_select/', {'uid': uid, 'parent_id': parent_id, 'model': model},
        function (data) {
            $('#files' + uid).append(data);
            $('#file_dialog' + uid).dialog('open');
        });
}



function save(form, url, id_input) {
    $(form).form('submit', {
        url: url,
        traditional: true,
        onSubmit: function () {
            return $(this).form('validate');
        },
        success: function (data) {
            let result = JSON.parse(data)[0];
            if (result.errorMsg) {
                $.messager.alert('Ошибка', result.errorMsg);
              } else if (result.count) {
                $.messager.show({
                    title: 'Результат',
                    msg: 'Количество записей, удовлетворяющих заданным условиям: ' + result.count,
                    timeout: 2000,
                    showType: 'show',
                    style: {
                        right: '',
                        top: document.body.scrollTop + document.documentElement.scrollTop,
                        bottom: ''
                    }
                });
            } else {
                $.messager.show({
                    title: 'Сохранение',
                    msg: 'Форма успешно сохранена',
                    timeout: 1000,
                    showType: 'show',
                    style: {
                        right: '',
                        top: document.body.scrollTop + document.documentElement.scrollTop,
                        bottom: ''
                    }
                });
            }
        }
    });
}

// control - id контрола, в который добавляется панель
// url - адрес, из которого загружается контент панели
// uid - уникальный код формы контрола(передается post-запросом)
// id - первичный ключ объекта, данные которого будут загружены (передается post-запросом)
// idx - порядковый номер панели (передается post-запросом)
// title - заголовок панели
function addAccordionPanel(control, url, uid, id, idx, title) {
    $.post(url, {'uid': uid, 'id': id, 'idx': idx}, function (data) {
        $(control).accordion('add', {
            title: title,
            content: data
        });
    });
}

function removeAccordionPanel(control, url) {
    var pp = $(control).accordion('getSelected');
    if (pp) {
        var index = $(control).accordion('getPanelIndex', pp);
        $(control).accordion('remove', index);
    }
}


// добавляет повторную проверку
// control - кнопка, которая должна стать неактивной
// createurl - адрес бэкэнда для создания повторной проверки, get-запрос, должен возвратить JSON
/*
function addRepeated(control, createurl) {
    $.messager.confirm('Подтверждение', 'Добавить повторную проверку?', function (r) {
        if (r) {
            $(control).linkbutton('disable');
            $.getJSON(createurl, function (result) {
                var result = result[0];
                if (result.errorMsg) {
                    $.messager.show({
                        title: 'Ошибка',
                        msg: result.errorMsg,
                        timeout: 1000,
                        showType: 'show',
                        style: {
                            right: '',
                            top: document.body.scrollTop + document.documentElement.scrollTop,
                            bottom: ''
                        }
                    });
                } else {
                    addTab('#tt', 'Повторная проверка ' + result.id, '/insp/new_inspection_form/' + result.id + '/')
                }
            });
        }
    });
}
*/

function working_day_send_changes(url, day, month, year) {
    var status = contains($('#d' + year + '_' + month + '_' + day).attr('class'), 'active');
    var status = !status;
    //alert('day: '+ day + 'month: ' + month + 'status: ' + status );
    $.post(url, {'day': day, 'month': month, 'status': status, 'year': year}, function (data) {
    });
}

// наличие вхождений в строке
// r - исходная строка
// s - искомая строка
function contains(r, s) {
    return r.indexOf(s) > -1;
}


function calculate_date(src, dest, days_count, url) {
    var src_date = $(src).datebox('getValue');
    $.post(url, {'src_date': src_date, 'days_count': days_count}, function (data) {
        var result = data[0];
        $(dest).datebox('setValue', result.msg);
    });
}


function refresh_accordion(control, title, url) {

    var pp = $(control).accordion('getPanel', title);    // get the selected panel
    if (pp) {
        pp.panel('refresh', url)
    }

}

function update_violations_in_precept(uid) {
    let tg = $('#violations_tree' + uid);
    let roots = tg.treegrid('getRoots');
    printnode(roots);

    function printnode(node) {
        node.forEach(function (item, i, node) {
            tg.treegrid('endEdit', item.id);
            let childrens = tg.treegrid('getChildren', item.id);
            let parrent = tg.treegrid('getParent', item.id);
            if (parrent !== null) {
                if (parrent.count_to_remove !== "undefined") {
                    if (item.count_to_remove) {
                        tg.treegrid('update', {
                            id: parrent.id,
                            row: {
                                count_to_remove: parseInt(parrent.count_to_remove) + parseInt(item.count_to_remove)
                            }
                        });
                    }
                }
                if (parrent.count_of_removed !== "undefined") {
                    if (item.count_of_removed) {
                        tg.treegrid('update', {
                            id: parrent.id,
                            row: {
                                count_of_removed: parseInt(parrent.count_of_removed) + parseInt(item.count_of_removed)
                            }
                        });
                    }
                }
            }

            if (childrens.length > 0) {
                tg.treegrid('update', {
                    id: item.id,
                    row: {
                        count_to_remove: 0,
                        count_of_removed: 0
                    }
                });
                printnode(childrens);
            }
            $('#violations' + uid).append('<input type="hidden" name="violations" value="' + item.id + ';' + item.count_to_remove + ';' + item.count_of_removed + '"/>');

        });
    }
}

function update_violations_in_inspection(uid) {
    let tg = $('#violations_tree' + uid);
    let roots = tg.treegrid('getRoots');
    printnode(roots);

    function printnode(node) {
        node.forEach(function (item, i, node) {
            tg.treegrid('endEdit', item.id);
            let childrens = tg.treegrid('getChildren', item.id);
            let parrent = tg.treegrid('getParent', item.id);
            if (parrent !== null) {
                if (parrent.count !== "undefined") {
                    if (item.count) {
                        tg.treegrid('update', {
                            id: parrent.id,
                            row: {
                                count: parseInt(parrent.count) + parseInt(item.count)
                            }
                        });
                    }
                }
            }
            if (childrens.length > 0) {
                tg.treegrid('update', {
                    id: item.id,
                    row: {
                        count: 0
                    }
                });
                printnode(childrens);
            }
            $('#violations' + uid).append('<input type="hidden" name="violations" value="' + item.id + ';' + item.count + '"/>')
        });
    }
}