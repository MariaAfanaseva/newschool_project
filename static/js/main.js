function addClassIcon(){
    const classes = {
        'id_name_icon':['zmdi-account', 'material-icons-name'],
        'id_username_icon':['zmdi-email'],
        'id_surname_icon': ['zmdi-account-o', 'material-icons-name'],
        'id_email_icon':['zmdi-email'],
        'id_password_icon':['zmdi-lock'],
        'id_password1_icon':['zmdi-lock'],
        'id_password2_icon': ['zmdi-lock-outline'],
        'id_city_icon': ['zmdi-home'],
        'id_country_icon': ['zmdi-city'],
        'id_old_password_icon': ['zmdi-lock'],
        'id_new_password1_icon': ['zmdi-lock-outline'],
        'id_new_password2_icon': ['zmdi-lock-outline']
    };
    for (let element_id in classes){
        let element = document.getElementById(element_id);
        if (element){
            for (let cl of classes[element_id]){
                element.classList.add(cl);
            }
        }
    }
}

addClassIcon();

function ajaxPagination() {
    $( document ).on('click', '.ow-pagination a', (event) => {
        if (event.target.hasAttribute('href')) {
            let page_url = event.target.href;
            $.ajax(
                {
                    url: page_url,
                    type: 'GET',
                    success: (data) => {
                        $('#courses_row').empty();
                        $('#courses_row').append( $(data).find('#courses_row').html() );
                    }
                }
            );
        event.preventDefault();
        }
    })
}

$(document).ready(() => {
    ajaxPagination();
});

$(document).ajaxStop(() => {
    ajaxPagination();
});
