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
                        $(this.change_item).append( $(data).find(this.change_item).html());
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
