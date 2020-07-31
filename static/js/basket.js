function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changeTotal() {
    const total_quantity = $('#total_quantity').data("quantity");
    if (+total_quantity > 0) {
        $('.fa-shopping-cart').text(total_quantity);
        return true;
    } else {
        $('.fa-shopping-cart').text('');
        return false;
    }
}

function completeOrder(details) {
    const data = {
        'order_id': details.id,
        'payment_time': details.create_time,
        'status': details.status,
        'payer_email': details.payer.email_address,
        'payer_name': details.payer.name.given_name,
        'payer_surname': details.payer.name.surname,
    };

    const csrftoken = this.getCookie('csrftoken');
    const path = $('#paypal-button-container').data("success");
    $.ajax({
        url: path,
        type: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        data: JSON.stringify(data),
        success: (data) => {
            $('.fa-shopping-cart').text('');
            $('.cart').empty();
            $('.cart').html(data.result);
            $("#site-loader").css("display","none");
        }
    });
}

function renderPayPalButton() {
    if (changeTotal()) {
        payPal();
    }
}

class Basket {
    constructor() {
        this.changeItem = '.cart';
    }

    deleteItem() {
        $(document).off('click').on('click', '.cart-delete a', (event) => {
            event.preventDefault();
            const path = event.target.href;
            const csrftoken = $("[name=csrfmiddlewaretoken]").val();  // get csrf token

            $.ajaxSetup({  // add csrf token to header ajax request
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: path,
                type: 'DELETE',
                success: (data) => {
                    $(this.changeItem).empty();
                    $('#pay-pal').remove();
                    $(this.changeItem).html(data.result);
                    renderPayPalButton();
                }
            });
        });
    }
}

renderPayPalButton();

const cart = new Basket();

$(document).ready(() => {
    cart.deleteItem();
});

$(document).ajaxStop(() => {
    cart.deleteItem();
});
