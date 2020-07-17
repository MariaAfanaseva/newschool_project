class Basket {
    constructor() {
        this.changeItem = '.cart';
        this.cart_quantity = '.fa-shopping-cart'
    }

    deleteItem() {
        $(document).on('click', '.cart-delete a', (event) => {
            // console.log('ajax');
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
                    if (data.quantity > 0) {
                        $(this.cart_quantity).text(data.quantity);
                    } else {
                         $(this.cart_quantity).text('');
                    }
                }
            });
        });
    }
}

const cart = new Basket();

$(document).ready(() => {
    cart.deleteItem();
});

$(document).ajaxStop(() => {
    cart.deleteItem();
});