$(document).ready(function () {
    let currentSort = 'newest';
    let searchQuery = $('input[type="search"]').val();

    if (!searchQuery) {
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');

        searchQuery = query
    }


    $('.filter-checkbox').change(function () {
        filterProducts(1,currentSort, searchQuery);
    });

    $(document).on('click', '.sort-option', function (e) {
        e.preventDefault();
        currentSort = $(this).data('sort');
        filterProducts(1, currentSort, searchQuery);
    });

    $(document).on('click', '#pagination .page-link', function (e) {
        e.preventDefault();
        var page = $(this).data('page');
        filterProducts(page, currentSort, searchQuery);
    });

    function filterProducts(page =1, sort = currentSort, searchQuery = '') {
        var subcategoryId = $('#products').data('subcategory-id');
        var selectedPrices = [];
        var selectedSizes = [];
        var selectedColors = [];
        var selectedBrands = [];
        var selectedStates = [];
        var selectedMaterials = [];

        $('#price-filter input:checked').each(function () {
            selectedPrices.push($(this).val());
        });
        $('#size-filter input:checked').each(function () {
            selectedSizes.push($(this).val());
        });
        $('#color-filter input:checked').each(function () {
            selectedColors.push($(this).val());
        });
        $('#brand-filter input:checked').each(function () {
            selectedBrands.push($(this).val());
        });
        $('#state-filter input:checked').each(function () {
            selectedStates.push($(this).val());
        });
        $('#material-filter input:checked').each(function () {
            selectedMaterials.push($(this).val());
        });

        // Construir el objeto de datos para enviar a la solicitud AJAX
        var requestData = {
            prices: selectedPrices,
            sizes: selectedSizes,
            colors: selectedColors,
            brands: selectedBrands,
            states: selectedStates,
            materials: selectedMaterials,
            page: page,
            sort: sort
        };

        if (searchQuery) {
            requestData.search_query = searchQuery;
        } else if (subcategoryId) {
            requestData.subcategory_id = subcategoryId;
        }

        // Enviar la solicitud AJAX
        $.ajax({
            url: '/filter_products',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function (response) {
                $('#products').html(response.html);
                $('#pagination').html(response.pagination);

                // Reinitialize wishlist buttons after updating the DOM
                initializeWishlistButtons();
            }
        });
    }
});