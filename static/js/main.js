function add_class_icon(){
    const classes = {
        'id_name_icon':['zmdi-account', 'material-icons-name'],
        'id_username_icon':['zmdi-email'],
        'id_email_icon':['zmdi-email'],
        'id_password_icon':['zmdi-lock'],
        'id_password1_icon':['zmdi-lock'],
        'id_password2_icon': ['zmdi-lock-outline']
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

add_class_icon();
