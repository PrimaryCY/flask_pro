function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击推出按钮时执行的函数
function logout() {
    $.ajax({
        url: "/api/v1.0/session",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if ("0" == resp.errno) {
                location.href = "/index.html";
            }
        }
    });
}

$(function(){
    $.get('/api/v1.0/user',function (resp) {
        if (resp.errno=='0'){
            $('.menu-text #user-name').html(resp.data.name);
            $('.menu-text #user-mobile').html(resp.data.mobile);
            $('.menu-content #user-avatar').attr('src',resp.data.avatar)
        }
        else if (resp.errno=='4101'){
            location.href = '/login.html'
        }
        else {
            alert(resp.msg)
        }
    })

})