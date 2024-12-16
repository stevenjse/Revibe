$(document).ready(function() {
    var numItems = $('.card').length;
    var itemsPerPage = 9;
    var currentPage = 1;
    var totalPages = Math.ceil(numItems / itemsPerPage);

    $('.card').slice(itemsPerPage).hide();
    $('#page-info').text('Página ' + currentPage + ' de ' + totalPages);

    $('.page-link').click(function(e) {
        e.preventDefault();

        var pageNum = $(this).text();

        if (pageNum === "Previous") {
            if (currentPage > 1) {
                currentPage--;
            }
        } else if (pageNum === "Next") {
            if (currentPage < totalPages) {
                currentPage++;
            }
        } else {
            currentPage = parseInt(pageNum);
        }

        var start = (currentPage - 1) * itemsPerPage;
        var end = start + itemsPerPage;

        $('.card').hide().slice(start, end).show();
        $('#page-info').text('Página ' + currentPage + ' de ' + totalPages);
    });
});