function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
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
    var amount = parseFloat($("#lead_offer").val()).toFixed(2);
    $.ajax({
		type: "POST",
		url: "/process_offer/",
		data: "hash=" + hash
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


change_amount = function (id) {
    var html = '<input type="number" id="new_value" placeholder="new offer"/><button onclick="save_new_value(' + id + ')">Save</button>';
    $("#amountfield" + id).html(html);
}

save_new_value = function(id) {
    var new_value = parseFloat($("#new_value").val());
    var html = '<div onclick="change_amount(' + id + ')">' + new_value.toFixed(2) + '</div>';
    $.ajax({
        type: "POST",
        url: "/change_amount/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: "id=" + id + "&amount=" + new_value.toFixed(2),
        success: function(msg) {
            $("#amountfield" + id).html(html);
        }
    });
}

save_settings = function(tip) {
    var values1 = ($("#1_value").val());
    var values2 = ($("#2_value").val());
    var values3 = ($("#3_value").val());
    var values4 = ($("#4_value").val());
    var values5 = ($("#5_value").val());
    var values6 = ($("#6_value").val());
    var values7 = ($("#7_value").val());
    var values8 = ($("#8_value").val());
    var values9 = ($("#9_value").val());
    var values10 = ($("#10_value").val());
    var values11 = ($("#11_value").val());
    var values12 = ($("#12_value").val());

    var data = 'tip=' + tip;
    data += '&1=' + values1;
    data += '&2=' + values2;
    data += '&3=' + values3;
    data += '&4=' + values4;
    data += '&5=' + values5;
    data += '&6=' + values6;
    data += '&7=' + values7;
    data += '&8=' + values8;
    data += '&9=' + values9;
    data += '&10=' + values10;
    data += '&11=' + values11;
    data += '&12=' + values12;

    $.ajax({
        type: "POST",
        url: "/save_settings/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: data,
        success: function(msg) {
            window.location.reload();
        }
    });

}
