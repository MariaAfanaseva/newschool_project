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


class Paginator {
    constructor(pagination_link, change_item){
        this.pagination_link = pagination_link;
        this.change_item = change_item;
    }
    ajaxPagination(){
        $( document ).on('click', this.pagination_link, (event) => {
        if (event.target.hasAttribute('href')) {
            let page_url = event.target.href;
            $.ajax(
                {
                    url: page_url,
                    type: 'GET',
                    success: (data) => {
                        $(this.change_item).empty();
                        $(this.change_item).append( $(data).find(this.change_item).html() );
                    }
                }
            );
        event.preventDefault();
        }
    })
    }
}

const coursesPagination = new Paginator('#courses-pagination a', '#courses-row');
const currentCoursePagination = new Paginator('#single-course-pagination a', '#current-courses');
const teacherCoursesPagination = new Paginator('#single-teacher-pagination a', '#teacher_courses');
const teachersPagination = new Paginator('#teachers-pagination a', '#teachers-row');

$(document).ready(() => {
    coursesPagination.ajaxPagination();
    currentCoursePagination.ajaxPagination();
    teacherCoursesPagination.ajaxPagination();
    teachersPagination.ajaxPagination();
});

$(document).ajaxStop(() => {
    coursesPagination.ajaxPagination();
    currentCoursePagination.ajaxPagination();
    teacherCoursesPagination.ajaxPagination();
    teachersPagination.ajaxPagination();
});
