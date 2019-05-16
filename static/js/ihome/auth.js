function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(function () {
    $.get('/api/v1.0/user/auth', function (resp) {
        if (resp.errno == 0) {
            if (resp.data.real_name && resp.data.id_card) {
                $('#real-name').val(resp.data.real_name).prop('disabled', true);
                $('#id-card').val(resp.data.id_card).prop('disabled', true);
                $('#form-auth input[type=submit]').hide()
            }

        } else if (resp.errno == '4101') {
            location.href = '/login.html'
        } else {
            alert(resp.msg)
        }
    })
    $('#form-auth').submit(function (e) {
        e.preventDefault()
        var data_dict = {
            'real_name': $('#real-name').val(),
            'id_card': $('#id-card').val()
        };


        data_json = JSON.stringify(data_dict)
        console.log(data_json)
        $.ajax({
            url: '/api/v1.0/user/auth',
            type: 'post',
            contentType: 'application/json',
            data: data_json,
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == 0) {
                    if (resp.data.real_name && resp.data.id_card) {
                        $('#real-name').val(resp.data.real_name).prop('disabled', true);
                        $('#id-card').val(resp.data.id_card).prop('disabled', true);
                        $('#form-auth input[type=submit]').hide()
                    }
                } else {
                    console.log(resp.msg)
                }
            }
        })


    })


})
