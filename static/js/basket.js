class Basket {
    constructor() {
        this.changeItem = '.cart';
    }

    deleteItem() {
        $(document).on('click', '.cart-delete a', (event) => {
            console.log('ajax');
            event.preventDefault();
            const path = event.target.href;
            $.ajax({
                url: path,
                success: (data) => {
                    console.log(data);
                    $(this.changeItem).empty();
                    $(this.changeItem).html(data.result);
                    if (data.cart_quantity > 0) {
                        $('.fa-shopping-cart').text(data.cart_quantity);
                    } else {
                         $('.fa-shopping-cart').text('');
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