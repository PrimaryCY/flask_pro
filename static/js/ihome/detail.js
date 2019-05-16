function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    var querydata = decodeQuery();
    var house_id = querydata['id'];
    $.get('/api/v1.0/houses/' + house_id, function (resp) {
        if (resp.errno == 0) {
            var house = resp.data.house;
            var user = resp.data.user;
            var img_urls = house.img_urls;
            if (house.max_days == 0) {
                house.max_days = '无限制';
            }
            console.log(house);
            $(".swiper-container").html(template("house-image-tmpl", {img_urls: img_urls, price: house.price}));
            $('.detail-con').html(template('house_detail_tmpl', {'house': house}));

            console.log(house.user_id)
            console.log(user.user_id)
            if (house.user_id == user.user_id) {
                console.log(house.user_id)
                console.log(user.user_id)
                $('.book-house').hide()
            }
            else {
                $('.book-house').show()
            }

        }


    });


    var mySwiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();
})