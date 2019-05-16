function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 向后端获取城区信息
    $.get("/api/v1.0/areas", function (resp) {

        if (resp.errno == 0) {

            var areas = resp.data;
            // for (i=0; i<areas.length; i++) {
            //     console.log('1');
            //     $("#area-id").append('<option value="'+ area.id +'">'+ area.name +'</option>');
            // }
            // $.each(areas,function (i,area) {
            //     $("#area-id").append('<option value="'+ area.id +'">'+ area.name +'</option>');
            // })

            // 使用js模板
            var html = template('areas-tmpl', {areas: areas});
            $('#area-id').html(html)


        } else {
            alert(resp.msg);
        }

    }, "json");

    var data = {};
    var facility = [];
    $('#form-house-info').submit(function (e) {
        e.preventDefault();
        $(this).serializeArray().map(function (x) {
            data[x.name] = x.value
        });
        $(':checked[name="facility"]').each(function (index, x) {
            facility[index] = $(x).val()
        });
        data.facility = facility;

        $.ajax({
            url: "/api/v1.0/houses/info",
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(data),
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '4101') {
                    location.href = '/login.html'
                } else if (resp.errno == 0) {
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    console.log()
                    $('#house-id').val(resp.data.house_id);
                    console.log($('#house-id').val())
                } else {
                    alert(resp.msg)
                }
            }
        })


    })
    $('#form-house-image').submit(function (e) {
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxsubmit对表单进行异步提交

        $(this).ajaxSubmit({
            url: '/api/v1.0/houses/image',
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
                    var img_url = resp.data.img_url;
                    $('.house-image-cons').append('<img src="'+ img_url +'">')
                } else {
                    alert(resp.msg)
                }
            }
        })
    })


});