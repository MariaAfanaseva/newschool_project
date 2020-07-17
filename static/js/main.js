class Paginator {
    constructor(paginationLink, changeItem){
        this.paginationLink = paginationLink;
        this.changeItem = changeItem;
    }

    filterAjax(pageUrl) {
        let filterData = $(".filter-form").serialize();
        $.ajax(
            {
                url: pageUrl,
                type: 'GET',
                data: filterData,
                success: (data) => {
                    $(this.changeItem).empty();
                    $(this.changeItem).html(data.result);
                }
            }
        );
    }

    ajaxPagination(){
        $( document ).on('click', this.paginationLink, (event) => {
        event.preventDefault();
        if (event.target.hasAttribute('href')) {
            let pageUrl = event.target.href;
            if (/filter/i.test(pageUrl)) {
                this.filterAjax(pageUrl);
            }
            else {
                $.ajax(
                    {
                        url: pageUrl,
                        type: 'GET',
                        success: (data) => {
                            $(this.changeItem).empty();
                            $(this.changeItem).append($(data).find(this.changeItem).html());
                        }
                    }
                );
            }
        }
    })
    }
}

class Filter {
    constructor(changeBlock, filterBtn) {
        this.changeBlock = changeBlock;
        this.filterBtn = filterBtn
    }

    updateData() {
        $(this.filterBtn).off("click").on("click", (event) => {
            event.preventDefault();
            if (event.target.hasAttribute('href')) {
                const path = event.target.href;
                let filterData = $(".filter-form").serialize();
                $.ajax({
                    type: 'GET',
                    url: path,
                    data: filterData,
                    success: (data) => {
                        $(this.changeBlock).empty();
                        $(this.changeBlock).html(data.result);
                    }
                })
            }

        })
    }
}

const coursesPagination = new Paginator('#courses-pagination a', '#courses-row');
const currentCoursePagination = new Paginator('#single-course-pagination a', '#current-courses');
const teacherCoursesPagination = new Paginator('#single-teacher-pagination a', '#teacher_courses');
const teachersPagination = new Paginator('#teachers-pagination a', '#teachers-row');
const filterCourses = new Filter('#courses-row', '#filter-courses-btn');
const filterTeachers = new Filter('#teachers-row', "#filter-teachers-btn");

$(document).ready(() => {
    coursesPagination.ajaxPagination();
    currentCoursePagination.ajaxPagination();
    teacherCoursesPagination.ajaxPagination();
    teachersPagination.ajaxPagination();
    filterCourses.updateData();
    filterTeachers.updateData();
});

$(document).ajaxStop(() => {
    coursesPagination.ajaxPagination();
    currentCoursePagination.ajaxPagination();
    teacherCoursesPagination.ajaxPagination();
    teachersPagination.ajaxPagination();
    filterCourses.updateData();
    filterTeachers.updateData();
});
