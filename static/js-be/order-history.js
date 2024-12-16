document.addEventListener('DOMContentLoaded', function() {
    function cargarPedidos(page = 1) {
        $.ajax({
            url: '/order_history',
            type: 'GET',
            data: { page: page },
            success: function(response) {
                const itemsTabla = document.getElementById('itemsTabla');
                const pagination = document.getElementById('pagination');

                itemsTabla.innerHTML = '';
                pagination.innerHTML = '';

                response.pedidos.forEach(pedido => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${pedido.id}</td>
                        <td>${new Date(pedido.fecha).toLocaleDateString()}</td>
                        <td>${pedido.total}</td>
                        <td>${pedido.status}</td>
                        <td><a href="/order_detail/${pedido.id}" class="btn btn-primary">Detalles</a></td>
                    `;
                    itemsTabla.appendChild(row);
                });

                for (let i = 1; i <= response.total_pages; i++) {
                    const pageItem = document.createElement('li');
                    pageItem.className = `page-item ${i === response.current_page ? 'active' : ''}`;
                    pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                    pageItem.addEventListener('click', function(e) {
                        e.preventDefault();
                        cargarPedidos(i);
                    });
                    pagination.appendChild(pageItem);
                }
            }
        });
    }

    cargarPedidos();
});
