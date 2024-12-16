document.addEventListener('DOMContentLoaded', function() {
    const grupoSelect = document.getElementById('grupo');
    const categoriaSelect = document.getElementById('categoria');
    const subcategoriaSelect = document.getElementById('subcategoria');
    const tamañoSelect = document.getElementById('tamaño');

    // Función para cargar grupos
    function loadGroups() {
        fetch('/api/groups')
            .then(response => response.json())
            .then(groups => {
                grupoSelect.innerHTML = '<option selected DISABLED>Seleccionar</option>';
                groups.forEach(group => {
                    grupoSelect.innerHTML += `<option value="${group.id}">${group.name}</option>`;
                });
            });
    }
    
    // Función para cargar categorías
    function loadCategories(groupId) {
        fetch(`/api/categories/${groupId}`)
            .then(response => response.json())
            .then(categories => {
                categoriaSelect.innerHTML = '<option selected DISABLED>Seleccionar</option>';
                categories.forEach(category => {
                    categoriaSelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
                });
                subcategoriaSelect.innerHTML = '<option selected DISABLED>Seleccionar</option>';
                tamañoSelect.innerHTML = '<option selected DISABLED>Seleccione un tamaño</option>';
            });
    }

    // Función para cargar subcategorías
    function loadSubcategories(categoryId) {
        fetch(`/api/subcategories/${categoryId}`)
            .then(response => response.json())
            .then(subcategories => {
                subcategoriaSelect.innerHTML = '<option selected DISABLED>Seleccionar</option>';
                subcategories.forEach(subcategory => {
                    subcategoriaSelect.innerHTML += `<option value="${subcategory.id}">${subcategory.name}</option>`;
                });
                tamañoSelect.innerHTML = '<option selected DISABLED>Seleccione un tamaño</option>';
            });
    }

    // Función para cargar tamaños
    function loadSizes(subCategoryId) {
        fetch(`/api/sizes/${subCategoryId}`)
            .then(response => response.json())
            .then(sizes => {
                tamañoSelect.innerHTML = '<option selected DISABLED>Seleccione un tamaño</option>';
                sizes.forEach(size => {
                    tamañoSelect.innerHTML += `<option value="${size.id}">${size.size}</option>`;
                });
            });
    }

    // Cargar grupos al cargar la página
    loadGroups();

    // Manejar cambio en el select de grupos
    grupoSelect.addEventListener('change', function() {
        const groupId = this.value;
        loadCategories(groupId);
    });

    // Manejar cambio en el select de categorías
    categoriaSelect.addEventListener('change', function() {
        const categoryId = this.value;
        loadSubcategories(categoryId);
    });

    // Manejar cambio en el select de subcategorías
    subcategoriaSelect.addEventListener('change', function() {
        const subCategoryId = this.value;
        loadSizes(subCategoryId);
    });
});