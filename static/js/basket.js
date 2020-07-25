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
    const path = $('#paypal-button-container').data("path");
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

function payPal() {

    // Render the PayPal button into #paypal-button-container
    paypal.Buttons({

        style: {
            size: 'large',
            color: 'gold',
            shape: 'rect',
            label: 'pay'
        },


        // Set up the transaction
        createOrder: function(data, actions) {
            let totalPrice = $( '#total_price' ).attr( "data-price");
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: "0.1"
                    }
                }]
            });
        },

        // Finalize the transaction
        onApprove: function(data, actions) {
            $("#site-loader").css("display","block");
            return actions.order.capture().then(function(details) {
                if (details.status === 'COMPLETED') {
                    completeOrder(details);
                }
                else {
                    alert("Your order wasn't paid! Something was wrong!");
                }
            });
        }
    }).render('#paypal-button-container');
}

class Basket {
    constructor() {
        this.changeItem = '.cart';
    }

    deleteItem() {
        $(document).on('click', '.cart-delete a', (event) => {
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
                    $(this.changeItem).html(data.result);
                    if (changeTotal()) {
                        payPal();
                    }
                }
            });
        });
    }
}

if (changeTotal()) {
    payPal();
}

const cart = new Basket();

$(document).ready(() => {
    cart.deleteItem();
});

$(document).ajaxStop(() => {
    cart.deleteItem();
});