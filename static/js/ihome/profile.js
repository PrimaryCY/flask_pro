function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            $('#user-avatar').attr('src', resp.data.avatar);
            $('#form-name #user-name').val(resp.data.name)
        }
        else if (resp.errno=='4101'){
            location.href = '/login.html'
        }
        else {
            alert(resp.msg)
        }
    })

    $('#form-avatar').submit(function (e) {
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxsubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url: '/api/v1.0/user/avatar',
            type: 'post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '4101'){
                    location.href = '/login.html'
                }
                else if (resp.errno == 0) {
                    var avatar_url = resp.data.avatar_url;
                    $('#user-avatar').attr('src', avatar_url)
                } else {
                    alert(resp.msg)
                }
            }
        })
    })
    $('#form-name').submit(function (e) {
        e.preventDefault();
        data_dict = {
            'name': $('#form-name #user-name').val()
        };
        data_json = JSON.stringify(data_dict);

        $.ajax({
            url: '/api/v1.0/user',
            type: 'put',
            data: data_json,
            contentType: 'application/json',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == 0) {
                    alert('修改成功');
                    location.reload()
                } else if (resp.errno == 4001) {
                    $('.error-msg i').html(resp.msg).show()
                }else if (resp.errno == 4001){
                    location.href = '/login.html'
                }
            }

        })


    })


});