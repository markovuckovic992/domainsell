function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

make_offer = function (base_id, hash, ip, name, contact, email) {
    var amount = $("#lead_offer").val()
    console.log(amount, name, contact, email)
    $.ajax({
		type: "POST",
		url: "/process_offer/",
		data: "base_id=" + base_id
        + "&amount=" + amount
        + "&name=" + name
        + "&contact=" + contact
        + "&email=" + email
        + "&ip=" + ip,
		headers: {
            'X-CSRFToken': csrftoken,
        },
	})
}

add_data = function (offer_id, hash) {
    email_offer = $("#email_offer").val()
    phone_offer = $("#phone_offer").val()
    $.ajax({
        type: "POST",
        url: "/contact/",
        data: "email_offer=" + email_offer + "&phone_offer=" + phone_offer + "&hash=" + hash,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg) {
            window.location=('/farewell/?id=' + hash)
        }
    })
}

revert_state = function(id, control) {
    var html = '';
    if (control == 0) {
        html += 'Offer:';
        html += '<button onclick="revert_state(' + id + ', 1)">';
        html += 'Revert';
        html += '</button>';
    } else {
        html += 'Sale:';
        html += '<button onclick="revert_state(' + id + ', 0)">';
        html += 'Revert';
        html += '</button>';
    }
    $.ajax({
        type: "POST",
        url: "/revert_state/",
        data: "id=" + id + "&control=" + control,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(msg) {
            $("#state_field" + id).html(html)
        }
    })
}

check_status = function(id) {
    $.ajax({
        type: "POST",
        url: "/check_status/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: "id=" + id,
        success: function(msg) {
            window.location.reload();
        }
    })
}

start_post_sale = function(id) {    
    var r = confirm("Are you sure?");
    if (r == true) {
        $.ajax({
            type: "POST",
            url: "/start_post_sale/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: "id=" + id,
            success: function(msg) {
                window.location.reload();
            }
        })
    }
}

start_post_release = function(id) {
    var r = confirm("Are you sure?");
    if (r == true) {
        $.ajax({
            type: "POST",
            url: "/start_post_release/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: "id=" + id,
            success: function(msg) {
                window.location.reload();
            }
        })
    }
}

Del = function (id) {
    var r = confirm("Are you sure?");
    if (r == true) {
        $.ajax({
            type: "POST",
            url: "/del_hash/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: "id=" + id,
            success: function(msg) {
                window.location.reload();
            }
        })
    }
}