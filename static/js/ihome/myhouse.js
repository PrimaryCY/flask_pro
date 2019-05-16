function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/api/v1.0/user/auth', function (resp) {
        if (resp.errno == 0) {
            if (resp.data.real_name && resp.data.id_card) {
                $('#auth-warn').hide()
            }

        } else if (resp.errno == '4101') {
            location.href = '/login.html'
        } else {
            alert(resp.msg)
        }
    },'json');

    $.get('/api/v1.0/user/houses',function (resp) {
        if (resp.errno == 0) {
            var houses = resp.data.houses;
            // 使用js模板
            var html = template('myhouse-tmpl', {houses: houses});
            $('#houses-list').append(html)


        } else {
            alert(resp.msg);
        }

    },'json')






})