# TODO: IMPLEMENTAR SHOW ITEMS GROUP, SHOW ITEMS CATEGORY

from datetime import datetime, timedelta
import os
from passlib.context import CryptContext
import pytz
import stripe
from flask import Config, Flask, render_template, request, redirect, url_for, jsonify, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from psycopg2 import IntegrityError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from wtforms.validators import ValidationError, EqualTo
from werkzeug.utils import secure_filename
from PIL import Image
from flask import session, redirect, url_for
from flask_mail import Mail, Message
import random
import string
import hashlib
from flask_socketio import SocketIO, emit


# Configura tu clave secreta de prueba de Stripe
stripe.api_key = 'sk_test_51PfA1pCAViqZ6hFUgLhvlNNuTDufw8x5eDaFdxkChz9PL2ZviqGaMPEuMFQ2tKqg9Tu7QU1zScevtk4kZ5gNjKY500lLRQicb4'

# Configuracion de la aplicacion
app = Flask(__name__)
app.secret_key = '1234'

# Configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:stevenjse@localhost/WEB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuracion de SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'soporte.revibe.ec@gmail.com'
app.config['MAIL_CONTACT'] = 'revibe.ec@gmail.com'
app.config['MAIL_PASSWORD'] = 'vikeuruzggtdqmrz'
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Configuracion de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuracion de archivos subidos
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Definir los requisitos de la contraseña
# Configuración de passlib
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

# Validación Contraseña
def validate_password(password):
    errors = []

    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    if not any(char.isdigit() for char in password):
        errors.append("La contraseña debe contener al menos un número.")
    if not any(char.isupper() for char in password):
        errors.append("La contraseña debe contener al menos una letra mayúscula.")
    if not any(char.islower() for char in password):
        errors.append("La contraseña debe contener al menos una letra minúscula.")
    if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>/?\\" for char in password):
        errors.append("La contraseña debe contener al menos un carácter especial.")

    return errors
#####################################################################################
# Modelos

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    #prefijo = db.Column(db.String(5), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contraseña = db.Column(db.String(500), nullable=False)
    is_subscribed = db.Column(db.Boolean, default=False)
    acerca = db.Column(db.String(255), nullable=True)
    foto_perfil = db.Column(db.Text, nullable=True)

    # Relación para reseñas que un usuario ha dejado
    reviews_given = db.relationship('Resena', foreign_keys='Resena.id_usuario', back_populates='reviewer', lazy=True)

    # Relación para reseñas que un usuario ha recibido
    reviews_received = db.relationship('Resena', foreign_keys='Resena.id_usuario2', back_populates='reviewed_user', lazy=True)

    # Relaciones para mensajes
    mensajes_enviados = db.relationship('Mensaje', foreign_keys='Mensaje.id_remitente', back_populates='remitente', lazy=True)
    mensajes_recibidos = db.relationship('Mensaje', foreign_keys='Mensaje.id_receptor', back_populates='receptor', lazy=True)

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        # Puedes ajustar la lógica si hay más reglas para considerar si el usuario está activo
        return True

    @property
    def is_authenticated(self):
        # Flask-Login ya maneja esto, pero lo agregamos aquí por claridad
        return True

    @property
    def is_anonymous(self):
        # No hay anonimato en este contexto, puedes ajustar si es necesario
        return False

# Modelo de Producto
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Guayaquil')), nullable=False)
    fotos = db.Column(db.String(255), nullable=True)  # Campo para almacenar rutas de imágenes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='product', lazy=True)
    brand = db.relationship('Brand', backref='product', lazy=True)
    size = db.relationship('Size', backref='product', lazy=True)
    color = db.relationship('Color', backref='product', lazy=True)
    condition = db.relationship('Condition', backref='product', lazy=True)
    material = db.relationship('Material', backref='product', lazy=True)
    group = db.relationship('Group', backref='product', lazy=True)
    category = db.relationship('Category', backref='product', lazy=True)
    subcategory = db.relationship('SubCategory', backref='product', lazy=True)

# Modelo de Marca
class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

# Modelo de Color
class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    rgb = db.Column(db.String(7), nullable=False)

# Modelo de Estado
class Condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

# Modelo de Tipo Material
class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

# Modelo Grupo
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    categories = db.relationship('Category', backref='group', lazy=True)
    sizes = db.relationship('Size', backref='group', lazy=True)

# Modelo Categoria
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)
    sizes = db.relationship('Size', backref='category', lazy=True)

# Modelo SubCategoria
class SubCategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    sizes = db.relationship('Size', backref='sub_category', lazy=True)

# Modelo Talla
class Size(db.Model):
    __tablename__ = 'size'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

# Modelo de Direcciones de Facturación
class DireccionesFacturacion(db.Model):
    __tablename__ = 'direcciones_facturacion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref='direcciones_facturacion', lazy=True)

# Modelo de Direcciones de Envío
class DireccionesEnvio(db.Model):
    __tablename__ = 'direcciones_envio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    lugar = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #prefijo = db.Column(db.String(5), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref='direcciones_envio', lazy=True)

# Modelo de Factura
class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Guayaquil')))
    envio = db.Column(db.Float, nullable=False)
    tasa_proteccion = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    direccion_envio_id = db.Column(db.Integer, db.ForeignKey('direcciones_envio.id'), nullable=False)

    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='compras', lazy=True)
    seller = db.relationship('User', foreign_keys=[seller_id], backref='ventas', lazy=True)
    direccion_envio = db.relationship('DireccionesEnvio', backref='factura', lazy=True)

# Modelo de Detalle de Factura
class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto = db.relationship('Product', backref='detalles', lazy=True)

# Modelo de Pedido
class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    status = db.Column(db.Text, nullable=False)

    factura = db.relationship('Factura', backref='pedido', lazy=True)

# Modelo de Wishlist
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    usuario = db.relationship('User', backref='wishlist', lazy=True)
    producto = db.relationship('Product', backref='wishlist', lazy=True)

class Resena(db.Model):
    __tablename__ = 'resena'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Usuario que deja la reseña
    id_usuario2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Usuario que recibe la reseña
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Guayaquil')), nullable=False)

    # Relaciones para evitar ambigüedad en los nombres
    reviewer = db.relationship('User', foreign_keys=[id_usuario], back_populates='reviews_given')
    reviewed_user = db.relationship('User', foreign_keys=[id_usuario2], back_populates='reviews_received')

# Modelo de Tokens de Usuario
class UserToken(db.Model):
    __tablename__ = 'user_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('tokens', lazy=True))

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_remitente = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_receptor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Guayaquil')))

    # Relaciones
    remitente = db.relationship('User', foreign_keys=[id_remitente], back_populates='mensajes_enviados')
    receptor = db.relationship('User', foreign_keys=[id_receptor], back_populates='mensajes_recibidos')

#####################################################################################

# EndPoints

# Principal
@app.route('/')
def index():
    # Buscar los productas mas nuevos
    products = Product.query.filter_by(status=True).order_by(Product.created_at.desc()).limit(8).all()

    groups = Group.query.all()
    return render_template('home.html', groups=groups, productos=products)

# About
@app.route('/about', methods=['GET'])
def about():
    groups = Group.query.all()
    return render_template('main/about.html', groups=groups)

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(id_usuario=current_user.id).all()
    product_ids = [item.id_producto for item in wishlist_items]
    productos = Product.query.filter(Product.id.in_(product_ids)).all()
    groups = Group.query.all()

    return render_template('main/wishlist.html', user=current_user, groups=groups, productos=productos)

# Items Sub Categoria
@app.route('/<int:subcategory_id>/<string:subcategory_name>')
def show_items_subcategory(subcategory_id, subcategory_name):
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Filtra los productos con status=True y por subcategory_id, y luego aplica la paginación
    productos_paginados = Product.query.filter_by(subcategory_id=subcategory_id, status=True).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    productos = productos_paginados.items
    total_pages = productos_paginados.pages
    current_page = productos_paginados.page

    groups = Group.query.all()

    # Consulta para obtener las tallas únicas basadas en el subcategory.id
    sizes = db.session.query(Size).filter_by(sub_category_id=subcategory_id).distinct(Size.size).all()
    #sizes = Size.query.all()
    colors = Color.query.all()
    brands = Brand.query.all()
    conditions = Condition.query.all()
    materials = Material.query.all()

    if not productos:
        return render_template('main/shop.html', productos=productos, subcategory_id=subcategory_id,
                               subcategory_name=subcategory_name, groups=groups, mensaje=1, total_pages=total_pages,
                               current_page=current_page, sizes=sizes, colors=colors, brands=brands, conditions=conditions, materials=materials)
    else:
        return render_template('main/shop.html', productos=productos, subcategory_id=subcategory_id,
                               subcategory_name=subcategory_name, groups=groups, mensaje=None, total_pages=total_pages,
                               current_page=current_page, sizes=sizes, colors=colors, brands=brands, conditions=conditions, materials=materials)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    productos_paginados = Product.query.filter(Product.title.ilike(f'%{query}%'), Product.status == True).paginate(page=page, per_page=12,
                                                                                           error_out=False)
    productos = productos_paginados.items
    total_pages = productos_paginados.pages
    current_page = productos_paginados.page
    groups = Group.query.all()

    unique_sizes = db.session.query(Product.size_id).filter(Product.title.ilike(f'%{query}%')).distinct()
    sizes = Size.query.filter(Size.id.in_(unique_sizes)).all()
    #sizes = Size.query.all()
    colors = Color.query.all()
    brands = Brand.query.all()
    conditions = Condition.query.all()
    materials = Material.query.all()

    if not productos:
        return render_template('main/shop.html', productos=productos, search_query=query, groups=groups, mensaje=1,
                               total_pages=total_pages, current_page=current_page, sizes=sizes, colors=colors, brands=brands, conditions=conditions, materials=materials)
    else:
        return render_template('main/shop.html', productos=productos, search_query=query, groups=groups, mensaje=None,
                               total_pages=total_pages, current_page=current_page, sizes=sizes, colors=colors, brands=brands, conditions=conditions, materials=materials)


@app.route('/filter_products', methods=['POST'])
def filter_products():
    data = request.json
    subcategory_id = data.get('subcategory_id')
    search_query = data.get('search_query', '')
    sort = data.get('sort', 'newest')

    # Iniciar la consulta base
    query = Product.query.filter_by(status=True)

    # Filtrar por subcategoría si se proporciona
    if subcategory_id:
        query = query.filter_by(subcategory_id=subcategory_id, status=True)

    # Filtrar por término de búsqueda si se proporciona
    if search_query:
        query = query.filter(db.or_(
            Product.title.ilike(f'%{search_query}%'),
            Product.description.ilike(f'%{search_query}%'),
            Product.status == True
        ))

    if data.get('prices'):
        price_filters = []
        for price_range in data['prices']:
            min_price, max_price = get_price_limits(price_range)
            price_filters.append((Product.price >= min_price) & (Product.price <= max_price))
        query = query.filter(db.or_(*price_filters))

    if data.get('sizes'):
        size_names = data['sizes']
        size_ids = [size.id for size in Size.query.filter(Size.size.in_(size_names)).all()]
        query = query.filter(Product.size_id.in_(size_ids))

    if data.get('colors'):
        color_names = data['colors']
        color_ids = [color.id for color in Color.query.filter(Color.name.in_(color_names)).all()]
        query = query.filter(Product.color_id.in_(color_ids))

    if data.get('brands'):
        brand_names = data['brands']
        brand_ids = [brand.id for brand in Brand.query.filter(Brand.name.in_(brand_names)).all()]
        query = query.filter(Product.brand_id.in_(brand_ids))

    if data.get('states'):
        states_names = data['states']
        states_ids = [state.id for state in Condition.query.filter(Condition.name.in_(states_names)).all()]
        query = query.filter(Product.state_id.in_(states_ids))

    if data.get('materials'):
        materials_names = data['materials']
        materials_ids = [material.id for material in Material.query.filter(Material.name.in_(materials_names)).all()]
        query = query.filter(Product.material_id.in_(materials_ids))

    # Añadir el criterio de ordenación a la consulta
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'oldest':
        query = query.order_by(Product.created_at.asc())
    else:  # Default sort (newest)
        query = query.order_by(Product.created_at.desc())

    # Configurar la paginación
    per_page = 12
    page = int(data.get('page', 1))
    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)

    filtered_products = paginated_query.items
    current_page = paginated_query.page
    total_pages = paginated_query.pages

    if not filtered_products:
        return jsonify({
            'html': render_template('main/filtered_products_not_found.html'),
            'pagination': render_template('main/filtered_products_pagination.html', current_page=current_page,
                                          total_pages=total_pages)
        })
    else:
        return jsonify({
            'html': render_template('main/filtered_products.html', productos=filtered_products),
            'pagination': render_template('main/filtered_products_pagination.html', current_page=current_page,
                                          total_pages=total_pages)
        })

def get_price_limits(price_range):
    if price_range == '0-25':
        return 0, 25
    elif price_range == '25-50':
        return 25, 50
    elif price_range == '50-100':
        return 50, 100
    elif price_range == '100-150':
        return 100, 150
    else:
        return 150, float('inf')

@app.route('/upload-product', methods=['GET', 'POST'])
@login_required 
def upload_product():
    if request.method == 'GET':
        groups = Group.query.all()
        marcas = Brand.query.all()
        materiales = Material.query.all()
        colores = Color.query.all()
        estados = Condition.query.all()
        return render_template('main/loadProduct.html', groups=groups, marcas=marcas, materiales=materiales, colores=colores, estados=estados)
    elif request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        grupo = request.form['grupo']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        marca = request.form['marca']
        tamaño = request.form['tamaño']
        material = request.form['material']
        color = request.form['color']
        estado = request.form['estado']
        ubicacion = request.form['ubicacion']
        precio = float(request.form['precio'])
        fotos = request.files.getlist('fotos')

        nuevo_producto = Product(
            title=titulo,
            description=descripcion,
            group_id=grupo,
            category_id=categoria,
            subcategory_id=subcategoria,
            brand_id=marca,
            size_id=tamaño,
            material_id=material,
            color_id=color,
            condition_id=estado,
            location=ubicacion,
            price=precio,
            created_at=datetime.now(pytz.timezone('America/Guayaquil')),
            user_id=current_user.id
            # fotos=fotos_binario[0] if fotos_binario else None  # Manejar adecuadamente si hay múltiples fotos
        )

        # if not fotos or not any(fotos):
        #     flash('Debe seleccionar al menos una foto', 'error')
        #     return redirect(url_for('loadProduct'))

        # # Convertir imágenes a binario
        # fotos_binario = [foto.read() for foto in fotos if foto]

        if 'images' not in request.files:
            return redirect(request.url)
    
        files = request.files.getlist('images')
        if not files:
            return redirect(request.url)

        

        db.session.add(nuevo_producto)
        db.session.commit()

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Guardar las imágenes
        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                # Leer el contenido de la foto
                contenido_foto = file.read()
                # Generar el hash del contenido
                hash_foto = hashlib.sha256(contenido_foto).hexdigest()
                # Crear el nombre del archivo usando el hash y la extensión original
                extension_archivo = file.filename.rsplit('.', 1)[1].lower()
                nombre_archivo_hash = f"{hash_foto}.{extension_archivo}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_hash)
                # Es necesario volver a leer el archivo, ya que fue leído anteriormente
                file.stream.seek(0)
                file.save(filepath)
                file_paths.append(nombre_archivo_hash)

        # Asociar las imágenes con el producto
        nuevo_producto.fotos = ','.join(file_paths)
        db.session.commit()
        flash('Producto subido con éxito')
        return redirect(url_for('mostrar_productos'))

# Función para verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/productos', methods=['GET'])
@login_required
def mostrar_productos():
    #productos = Product.query.all()
    productos = Product.query.filter_by(user_id=current_user.id).all()
    groups = Group.query.all()

    return render_template('main/productos.html', productos=productos, groups=groups)

@app.route('/producto/<int:producto_id>')
@login_required
def ver_producto(producto_id):
    # Verificación de que el usuario actual es el propietario del producto
    producto = Product.query.get_or_404(producto_id)
    if producto.user_id != current_user.id:
        return redirect(url_for('index'))
    
    producto = Product.query.filter_by(id=producto_id, user_id=current_user.id).first_or_404()
    groups = Group.query.all()

    # Buscar el detalle de la factura que contiene el producto
    detalle_factura = DetalleFactura.query.filter_by(producto_id=producto_id).first()
    if detalle_factura:
        pedido = Pedido.query.filter_by(factura_id=detalle_factura.factura_id).first()
        return render_template('main/producto_detalle.html', producto=producto, groups=groups, pedido=pedido)

    return render_template('main/producto_detalle.html', producto=producto, groups=groups, pedido=None)

@app.route('/producto/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    # Verificación de que el usuario actual es el propietario del producto
    producto = Product.query.get_or_404(producto_id)
    if producto.user_id != current_user.id:
        return redirect(url_for('index'))

    grupos = Group.query.all()
    categorias = Category.query.all()
    subcategorias = SubCategory.query.all()
    marcas = Brand.query.all()
    tamanos = Size.query.all()
    materiales = Material.query.all()
    colores = Color.query.all()
    estados = Condition.query.all()

    if request.method == 'POST':
        try:
            # Validar datos del formulario
            group_id = request.form.get('grupo')
            category_id = request.form.get('categoria')
            subcategory_id = request.form.get('subcategoria')
            brand_id = request.form.get('marca')
            size_id = request.form.get('tamaño')
            material_id = request.form.get('material')
            color_id = request.form.get('color')
            state_id = request.form.get('estado')

            if not all([group_id, category_id, subcategory_id, brand_id, size_id, material_id, color_id, state_id]):
                raise ValueError("Faltan campos obligatorios")

            # Actualizar atributos del producto
            producto.title = request.form['titulo']
            producto.description = request.form['descripcion']
            producto.group = Group.query.get(group_id)
            producto.category = Category.query.get(category_id)
            producto.subcategory = SubCategory.query.get(subcategory_id)
            producto.brand = Brand.query.get(brand_id)
            producto.size = Size.query.get(size_id)
            producto.material = Material.query.get(material_id)
            producto.color = Color.query.get(color_id)
            producto.condition = Condition.query.get(state_id)
            producto.location = request.form['ubicacion']
            producto.price = float(request.form['precio'])

            # Manejar eliminación de imágenes
            remove_images = request.form.get('remove_images', '')
            if remove_images:
                old_images = producto.fotos.split(',')
                remove_images_list = remove_images.split(',')
                for image in remove_images_list:
                    if image in old_images:
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        old_images.remove(image)
                producto.fotos = ','.join(old_images)

            # Guardar nuevas imágenes
            fotos = request.files.getlist('images')
            new_file_paths = []
            for file in fotos:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    new_file_paths.append(filename)

            # Obtener imágenes existentes
            existing_images = producto.fotos.split(',') if producto.fotos else []

            # Validar total de imágenes
            total_images = len(existing_images) + len(new_file_paths)
            if total_images < 1:
                raise ValueError("Debe haber al menos una imagen")
            if total_images > 4:
                raise ValueError("No puede haber más de 4 imágenes en total")

            # Actualizar lista de imágenes
            producto.fotos = ','.join(existing_images + new_file_paths)

            db.session.commit()
            flash('Producto actualizado correctamente')
            return redirect(url_for('mostrar_productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error actualizando el producto: {str(e)}', 'danger')


    # Extraer las categorias del grupo
    categorias_producto = Category.query.filter_by(group_id=producto.group_id).all()
    # Extraer las subcategorias de la categoria
    subcategorias_producto = SubCategory.query.filter_by(category_id=producto.category_id).all()

    return render_template('main/editar-producto.html', producto=producto, grupos=grupos, groups=grupos,categorias=categorias, subcategorias=subcategorias, marcas=marcas, tamanos=tamanos, materiales=materiales, colores=colores, estados=estados, categorias_producto=categorias_producto, subcategorias_producto=subcategorias_producto)

@app.route('/producto/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    producto = Product.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('mostrar_productos'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Filtra las facturas del usuario actual como comprador
    facturas = Factura.query.filter_by(buyer_id=current_user.id).all()

    # Obtén los IDs de las facturas del usuario
    factura_ids = [factura.id for factura in facturas]

    # Filtra los pedidos que están asociados con estas facturas
    pedidos = Pedido.query.filter(Pedido.factura_id.in_(factura_ids)).limit(5)

    groups = Group.query.all()
    return render_template('/main/user-dashboard.html', user=current_user, groups=groups, pedidos=pedidos)

@app.route('/account-settings')
@login_required
def account_settings():
    groups = Group.query.all()
    return render_template('/main/account-setting.html', user=current_user, groups=groups)

@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    if request.method == 'POST':
        try:
            foto = request.files.get('fotoPerfil')
            if foto:
                # Leer el contenido de la foto
                contenido_foto = foto.read()
                # Generar el hash del contenido
                hash_foto = hashlib.sha256(contenido_foto).hexdigest()
                # Crear el nombre del archivo usando el hash y la extensión original
                extension_archivo = foto.filename.rsplit('.', 1)[1].lower()
                nombre_archivo_hash = f"{hash_foto}.{extension_archivo}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_hash)
                # Es necesario volver a leer el archivo, ya que fue leído anteriormente
                foto.stream.seek(0)
                foto.save(filepath)
                # Actualizar la ruta de la foto en la base de datos
                current_user.foto_perfil = nombre_archivo_hash

            # Actualizar otros campos si no están vacíos
            nombre = request.form.get('nombre')
            if nombre not in [None, '']:
                current_user.nombre = nombre

            apellido = request.form.get('apellido')
            if apellido not in [None, '']:
                current_user.apellido = apellido

            # correo = request.form.get('correo')
            # if correo not in [None, '']:
            #     current_user.correo = correo

            telefono = request.form.get('telefono')
            if telefono not in [None, '']:
                current_user.telefono = telefono

            acerca = request.form.get('acercaDe')
            if acerca not in [None, '']:
                current_user.acerca = acerca

            db.session.commit()

            # Construir la respuesta con los datos actualizados
            response_data = {
                'message': 'Datos actualizados con éxito',
                'userData': {
                    'nombre': current_user.nombre,
                    'apellido': current_user.apellido,
                    'correo': current_user.correo,
                    'telefono': current_user.telefono,
                    'acercaDe': current_user.acerca,
                    'fotoPerfil': current_user.foto_perfil
                }
            }

            return jsonify(response_data), 200

        except Exception:
            return jsonify({'error': 'Se produjo un error al actualizar los datos. Intenta de nuevo'}), 500

@app.route('/direcciones-facturacion', methods=['POST', 'GET'])
@login_required
def direcciones_facturacion():
    if request.method == 'POST':
        direccion_id = request.form.get('direccionSeleccionada')
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        empresa = request.form.get('empresa')
        direccion = request.form['direccion']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
        codigo_postal = request.form['codigo_postal']
        email = request.form['email']
        telefono = request.form['telefono']

        if direccion_id:  # Si hay un ID de dirección, se trata de una edición
            direccion_existente = DireccionesFacturacion.query.get(direccion_id)
            if direccion_existente:
                direccion_existente.nombre = nombre
                direccion_existente.apellido = apellido
                direccion_existente.empresa = empresa
                direccion_existente.direccion = direccion
                direccion_existente.pais = pais
                direccion_existente.ciudad = ciudad
                direccion_existente.codigo_postal = codigo_postal
                direccion_existente.email = email
                direccion_existente.telefono = telefono
                db.session.commit()
                flash('Dirección de facturación actualizada con éxito')
        else:  # Si no hay ID de dirección, es una nueva dirección
            nueva_direccion = DireccionesFacturacion(
                id_usuario=current_user.id,  # Este es solo un ejemplo, aquí deberías obtener el id del usuario actual
                nombre=nombre,
                apellido=apellido,
                empresa=empresa,
                direccion=direccion,
                pais=pais,
                ciudad=ciudad,
                codigo_postal=codigo_postal,
                email=email,
                telefono=telefono
            )
            db.session.add(nueva_direccion)
            db.session.commit()
            flash('Dirección de facturación agregada con éxito')
        
        return redirect(url_for('direcciones_facturacion'))

    direcciones = DireccionesFacturacion.query.filter_by(id_usuario=current_user.id).all()
    return render_template('main/account-setting.html', direcciones=direcciones, user=current_user)

@app.route('/direcciones-facturacion/<int:id>', methods=['DELETE'])
@login_required
def eliminar_direccion(id):
    direccion = DireccionesFacturacion.query.get(id)
    if direccion:
        db.session.delete(direccion)
        db.session.commit()
        return jsonify({'message': 'Dirección eliminada con éxito'}), 200
    return jsonify({'message': 'Dirección no encontrada'}), 404

@app.route('/direcciones-envio', methods=['POST', 'GET'])
@login_required
def direcciones_envio():
    if request.method == 'POST':
        direccion_id = request.form.get('direccionSeleccionadaEnvio')
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        lugar = request.form.get('lugar')
        direccion = request.form['direccion']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
        zip = request.form['zip']
        email = request.form['email']
        celular = request.form['telefono']
        # prefijo = request.form['prefijo']

        if direccion_id:  # Si hay un ID de dirección, se trata de una edición
            direccion_existente = DireccionesEnvio.query.get(direccion_id)

            if direccion_existente:
                direccion_existente.nombre = nombre
                direccion_existente.apellido = apellido
                direccion_existente.lugar = lugar
                direccion_existente.direccion = direccion
                direccion_existente.pais = pais
                direccion_existente.ciudad = ciudad
                direccion_existente.codigo_postal = zip
                direccion_existente.email = email
                direccion_existente.telefono = celular
                #direccion_existente.prefijo = prefijo
                db.session.commit()
                flash('Dirección de envío actualizada con éxito')
        else:  # Si no hay ID de dirección, es una nueva dirección
            nueva_direccion = DireccionesEnvio(
                id_usuario=current_user.id,  # Este es solo un ejemplo, aquí deberías obtener el id del usuario actual
                nombre=nombre,
                apellido=apellido,
                lugar=lugar,
                direccion=direccion,
                pais=pais,
                ciudad=ciudad,
                codigo_postal=zip,
                email=email,
                telefono=celular,
                #prefijo=prefijo
            )
            db.session.add(nueva_direccion)
            db.session.commit()
            flash('Dirección de envío agregada con éxito')

        return redirect(url_for('direcciones_envio'))

    direccionesE = DireccionesEnvio.query.filter_by(id_usuario=current_user.id).all()
    return render_template('main/account-setting.html', direccionesE=direccionesE, user=current_user)

@app.route('/direcciones-envio/<int:id>', methods=['DELETE'])
@login_required
def eliminar_direccionEnvio(id):
    direccion = DireccionesEnvio.query.get(id)
    if direccion:
        db.session.delete(direccion)
        db.session.commit()
        return '', 204
    return '', 404


@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    groups = Group.query.all()

    return render_template('/main/product-detail.html', product=product, groups=groups, user=current_user)


def format_date(value, format='%d/%m/%Y'):
    if value is None:
        return ''
    return value.strftime(format)


app.jinja_env.filters['format_date'] = format_date


@app.route('/checkout')
@login_required
def checkout():
    product = Product.query.get_or_404(request.args.get('product_id'))
    subtotal = round(float(product.price), 2)
    envio = 0.00
    tasa_proteccion = round(subtotal * 0.2, 2)
    total = round(subtotal + envio + tasa_proteccion, 2)
    groups = Group.query.all()
    direccionesE = DireccionesEnvio.query.filter_by(id_usuario=current_user.id).all()

    return render_template('/main/checkout.html', user=current_user, groups=groups, product=product, subtotal=subtotal, envio=envio, tasa_proteccion=tasa_proteccion, total=total, direccionesE=direccionesE)


@app.route('/pay', methods=['POST'])
@login_required
def pay():
    if request.method == 'POST':
        # Obtener los datos JSON de la solicitud
        data = request.json
        product_id = data.get('product_id')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        address = data.get('address')
        country = data.get('country')
        city = data.get('city')
        zip = data.get('zip')
        token = data.get('token')
        amount = round(data.get('total') * 100)  # Convertir a centavos
        envio = data.get('envio')
        description = "Compra de producto"

        # Buscar el producto por ID
        product = Product.query.get_or_404(product_id)

        # Obtener el comprador
        buyer = current_user

        # Buscar la dirección de envío
        direccion_envio = DireccionesEnvio.query.filter_by(id_usuario=buyer.id, nombre=firstName, apellido=lastName, direccion=address, pais=country, ciudad=city, codigo_postal=zip).first()

        # Obtener al vendedor
        seller = product.user

        # Procesar el pago
        try:
            # Crear el cargo
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=description,
                source=token,
            )

            # Generar una factura
            factura = Factura(
                buyer_id=buyer.id,
                seller_id=seller.id,
                fecha=datetime.now(pytz.timezone('America/Guayaquil')),
                envio=envio,
                tasa_proteccion=round(round(float(product.price), 2) * 0.2, 2),
                total=data.get('total'),
                direccion_envio_id=direccion_envio.id
            )

            # Guardar en la base de datos
            db.session.add(factura)
            db.session.commit()

            # Generar detalle
            detalle = DetalleFactura(
                factura_id=factura.id,
                producto_id=product.id,
                subtotal=product.price
            )

            # Guardar en la base de datos
            db.session.add(detalle)
            db.session.commit()

            # Generar Pedido
            pedido = Pedido(
                factura_id=factura.id,
                status='Pagado'
            )

            # Guardar en la base de datos
            db.session.add(pedido)
            db.session.commit()

            # Cambiar el estado del producto
            product.status = False

            # Guardar en la base de datos
            db.session.commit()

            # Enviar el correo electrónico de notificacion de venta
            msg = Message('Venta Realizada',
                          sender=('Equipo de Re-Vibe', app.config['MAIL_USERNAME']),
                          recipients=[seller.correo])
            msg.html = f'''
            <html>
                <body>
                    <p>Hola {seller.nombre},</p>
                    <p>¡El producto {product.title} ha sido vendido!</p>
                    <p>Revisa tus productos para notificar cuando lo envies.</p>
                    <p>Gracias por usar Re-Vibe.</p>                                                    
                </body>
            </html>
            '''
            mail.send(msg)

            return jsonify({'status': 'success', 'message': 'Pago procesado exitosamente.'})

        except stripe.error.CardError as e:
            return jsonify({'status': 'error', 'message': str(e)})
        except stripe.error.RateLimitError as e:
            return jsonify({'status': 'error', 'message': 'Demasiadas solicitudes al API de Stripe. Por favor intenta nuevamente.'})
        except stripe.error.InvalidRequestError as e:
            return jsonify({'status': 'error', 'message': 'Parámetros inválidos enviados a Stripe.'})
        except stripe.error.AuthenticationError as e:
            return jsonify({'status': 'error', 'message': 'Error de autenticación con Stripe.'})
        except stripe.error.APIConnectionError as e:
            return jsonify({'status': 'error', 'message': 'Error de conexión con Stripe. Por favor intenta nuevamente.'})
        except stripe.error.StripeError as e:
            return jsonify({'status': 'error', 'message': 'Ocurrió un error con Stripe. Por favor intenta nuevamente.'})
        except Exception as e:
            print(e)
            return jsonify({'status': 'error', 'message': 'Error al procesar el pago.'})


@app.route('/order_history')
@login_required
def order_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Filtra las facturas del usuario actual como comprador
    facturas = Factura.query.filter_by(buyer_id=current_user.id).all()

    # Obtén los IDs de las facturas del usuario
    factura_ids = [factura.id for factura in facturas]

    # Filtra los pedidos que están asociados con estas facturas
    pedidos_paginados = Pedido.query.filter(Pedido.factura_id.in_(factura_ids)).paginate(page=page, per_page=per_page, error_out=False)

    groups = Group.query.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        pedidos = [{
            'id': pedido.id,
            'factura_id': pedido.factura_id,
            'fecha': pedido.factura.fecha,
            'total': pedido.factura.total,
            'status': pedido.status
        } for pedido in pedidos_paginados.items]
        return jsonify({
            'pedidos': pedidos,
            'total_pages': pedidos_paginados.pages,
            'current_page': pedidos_paginados.page
        })
    else:
        pedidos = pedidos_paginados.items
        return render_template('main/order-history.html', pedidos=pedidos, total_pages=pedidos_paginados.pages, current_page=pedidos_paginados.page, groups=groups)


@app.route('/order_detail/<int:order_id>')
@login_required
def order_detail(order_id):
    pedido = Pedido.query.get_or_404(order_id)
    producto = pedido.factura.detalles[0].producto
    groups = Group.query.all()

    return render_template('/main/order-details.html', pedido=pedido, product=producto, groups=groups)


@app.route('/toggle_wishlist', methods=['POST'])
# @login_required
def toggle_wishlist():
    product_id = request.json.get('product_id')
    user_id = current_user.id

    wishlist_item = Wishlist.query.filter_by(id_usuario=user_id, id_producto=product_id).first()

    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_wishlist_item = Wishlist(id_usuario=user_id, id_producto=product_id)
        db.session.add(new_wishlist_item)
        db.session.commit()
        return jsonify({'status': 'added'})

@app.route('/productos')
def productos():
    productos = Product.query.all()  # Obtén todos los productos
    wishlist_product_ids = [item.id_producto for item in Wishlist.query.filter_by(id_usuario=current_user.id).all()]

    return render_template('main/wishlist.html', productos=productos, wishlist_product_ids=wishlist_product_ids)


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    productos = Product.query.filter_by(user_id=user_id).all()
    reseñas = Resena.query.filter_by(id_usuario2=user_id).all()
    # Calcular la calificación general
    if reseñas:
        calificacion_general = sum(reseña.calificacion for reseña in reseñas) / len(reseñas)
    else:
        calificacion_general = 0
    return render_template('/main/user-details.html', user=user, productos=productos, reseñas=reseñas, calificacion_general=calificacion_general)


@app.route('/agregar-resena', methods=['POST'])
@login_required
def agregar_resena():
    calificacion = request.form.get('calificacion')
    comentario = request.form.get('comentario')
    print(calificacion)
    print(comentario)
    id_usuario2 = request.form.get('id_usuario2')  # El ID del usuario que recibirá la reseña

    # if not calificacion or not comentario or not id_usuario2:
    if not calificacion or not comentario:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('user_details'))  # Cambia 'index' por la ruta adecuada

    nueva_resena = Resena(
        id_usuario=current_user.id,
        id_usuario2=id_usuario2,
        calificacion=calificacion,
        comentario=comentario,
        fecha=datetime.now(pytz.timezone('America/Guayaquil'))
    )

    db.session.add(nueva_resena)
    db.session.commit()
    flash('Reseña agregada exitosamente.', 'success')
    print('Reseña agregada exitosamente.')
    return redirect(url_for('user_profile', user_id=id_usuario2))


@app.route('/enviar_producto', methods=['POST'])
@login_required
def enviar_producto():
    data = request.get_json()
    pedido_id = data.get('pedido_id')
    pedido = Pedido.query.get(pedido_id)

    if pedido:
        # Cambiar el estado del pedido
        pedido.status = 'Enviado'
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Pedido marcado como Enviado'})

    return jsonify({'status': 'error', 'message': 'Pedido no encontrado o no se pudo actualizar'}), 404

@app.route('/pedido_recibido', methods=['POST'])
@login_required
def pedido_recibido():
    data = request.get_json()
    pedido_id = data.get('pedido_id')
    pedido = Pedido.query.get(pedido_id)

    if pedido:
        pedido.status = 'Recibido'
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Pedido marcado como Recibido'})

    return jsonify({'status': 'error', 'message': 'Pedido no encontrado o no se pudo actualizar'}), 404

@app.route('/pedido_devuelto', methods=['POST'])
@login_required
def pedido_devuelto():
    data = request.get_json()
    pedido_id = data.get('pedido_id')
    pedido = Pedido.query.get(pedido_id)

    factura = Factura.query.get(pedido.factura_id)
    seller = factura.seller
    producto = factura.detalles[0].producto
    if pedido:
        pedido.status = 'Devuelto'
        db.session.commit()

        # Enviar el correo electrónico de notificacion de venta
        msg = Message('Producto Devuelto',
                      sender=('Equipo de Re-Vibe', app.config['MAIL_USERNAME']),
                      recipients=[seller.correo])
        msg.html = f'''
            <html>
                <body>
                    <p>Hola {seller.nombre},</p>
                    <p>El producto {producto.title} ha sido devuelto :(</p>
                    <p>El comprador se pondrá en contacto contigo, revisa tus mensajes.</p>
                    <p>Gracias por usar Re-Vibe.</p>                                                    
                </body>
            </html>
            '''
        mail.send(msg)


        return jsonify({'status': 'success', 'message': 'Pedido marcado como Devuelto'})

    return jsonify({'status': 'error', 'message': 'Pedido no encontrado o no se pudo actualizar'}), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('main/error404.html'), 404

@app.route('/chat/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def chat(receiver_id):
    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        sender_id = request.form.get('sender_id')
        receiver_id = request.form.get('receiver_id')

        nuevo_mensaje = Mensaje(id_remitente=sender_id, id_receptor=receiver_id, contenido=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return jsonify({'status': 'success'}), 200

    mensajes = Mensaje.query.filter(
        ((Mensaje.id_remitente == current_user.id) & (Mensaje.id_receptor == receiver_id)) |
        ((Mensaje.id_remitente == receiver_id) & (Mensaje.id_receptor == current_user.id))
    ).order_by(Mensaje.fecha).all()

    receptor = User.query.get_or_404(receiver_id)
    return render_template('main/chat.html', receptor=receptor, mensajes=mensajes)

@app.route('/chats')
@login_required
def chats():
    current_user_id = current_user.id
    # Obtener IDs de los usuarios con los que el usuario actual ha chateado
    sent_ids = db.session.query(Mensaje.id_receptor).filter_by(id_remitente=current_user_id).distinct()
    received_ids = db.session.query(Mensaje.id_remitente).filter_by(id_receptor=current_user_id).distinct()

    # Convertir resultados a una lista de IDs
    chat_user_ids = [row[0] for row in sent_ids.union(received_ids).all()]

    # Obtener los detalles de los usuarios
    chat_users = User.query.filter(User.id.in_(chat_user_ids)).all()

    return render_template('main/chats.html', chat_users=chat_users)


############# LOGIN Y REGISTRO DE USUARIOS ################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        groups=Group.query.all()
        return render_template('main/sign-in.html', groups=groups)
    elif request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        correo = data.get('correo')
        #prefijo = data.get('prefijo')
        telefono = data.get('telefono')
        contraseña = data.get('password')
        contraseña_confirm = data.get('passwordConfirmation')
        is_subscribed = data.get('is_subscribed', False)

        if User.query.filter_by(correo=correo).first():
            return jsonify({'error': 'El correo electrónico ya está en uso'}), 400

        if contraseña != contraseña_confirm:
            return jsonify({'error': 'Las contraseñas no coinciden'}), 400

        # Validar la contraseña
        validation_errors = validate_password(contraseña)

        if validation_errors:
            error_message = 'La contraseña no cumple con los requisitos:<ul>'
            for error in validation_errors:
                error_message += f'<li>{error}</li>'
            error_message += '</ul>'
            return jsonify({'error': error_message}), 400

        new_user = User(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            #prefijo=prefijo,
            telefono=telefono,
            foto_perfil='default.png'
        )

        new_user.set_password(contraseña)
        new_user.is_subscribed = is_subscribed
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registro exitoso'}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        groups=Group.query.all()
        return render_template('main/log-in.html', groups=groups)
    elif request.method == 'POST':
        data = request.get_json()
        correo = data.get('correo')
        contraseña = data.get('password')
        user = User.query.filter_by(correo=correo).first()

        next_page = data.get('next')

        if user and user.check_password(contraseña):
            login_user(user)
            if next_page:
                return jsonify({'message': 'Inicio de sesión exitoso', 'next': next_page}), 200
            else:
                return jsonify({'message': 'Inicio de sesión exitoso', 'next': url_for('index')}), 200
        else:
            return jsonify({'error': 'Correo electrónico o contraseña incorrectos'}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

############# RESTABLECIMIENTO DE CONTRASEÑA ##############

def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/password-reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    correo = data.get('correo')
    user = User.query.filter_by(correo=correo).first()

    if user:
        # Generar un token único y establecer una expiración
        token = generate_temp_password(length=32)
        expiration = datetime.now(pytz.timezone('America/Guayaquil')) + timedelta(minutes=15)  # Token expira en 1 hora

        # Eliminar tokens antiguos si los hay
        UserToken.query.filter_by(user_id=user.id).delete()

        # Crear y guardar el nuevo token
        new_token = UserToken(user_id=user.id, token=token, expires_at=expiration)
        db.session.add(new_token)
        db.session.commit()

        # Enviar el correo electrónico con el token
        msg = Message('Restablecimiento de contraseña',
                      sender=('Equipo de Soporte', app.config['MAIL_USERNAME']),
                      recipients=[correo])
        msg.html = f'''
        <html>
            <body>
                <p>Hola {user.nombre},</p>
                <p>Hemos recibido una solicitud para restablecer tu contraseña. Por favor, utiliza el siguiente enlace para restablecer tu contraseña:</p>
                <p><a href="{url_for('reset_password', token=token, _external=True)}">Restablecer contraseña</a></p>
                <p>Este enlace expira en 15 minutos. Si no solicitaste este cambio, por favor ignora este correo.</p>
            </body>
        </html>
        '''
        mail.send(msg)

        return jsonify({'message': 'Se ha enviado un enlace para restablecer tu contraseña a tu correo electrónico.'}), 200
    else:
        return jsonify({'error': 'No se encontró una cuenta con ese correo electrónico.'}), 400

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    token_entry = UserToken.query.filter_by(token=token).first()

    if not token_entry:
        return render_template('main/invalid_or_expired_token.html')

    if token_entry.expires_at < datetime.now(pytz.timezone('America/Guayaquil')):
        db.session.delete(token_entry)
        db.session.commit()
        return render_template('main/invalid_or_expired_token.html')

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            return jsonify({'success': False, 'message': 'Las contraseñas no coinciden'}), 200

        # Validar la contraseña
        validation_errors = validate_password(new_password)

        if validation_errors:
            error_message = 'La contraseña no cumple con los requisitos:<ul>'
            for error in validation_errors:
                error_message += f'<li>{error}</li>'
            error_message += '</ul>'
            return jsonify({'success':False, 'message': error_message}), 200

        user = User.query.get(token_entry.user_id)
        user.set_password(new_password)
        db.session.delete(token_entry)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Contraseña restablecida exitosamente'})

    return render_template('main/reset_password.html', token=token)

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get('currentpassword')
    new_password = data.get('newpassword')
    confirm_password = data.get('confirmpassword')

    user = current_user

    print(user.id, user.nombre, current_password, new_password, confirm_password)

    if not user.check_password(current_password):
        return jsonify({'error': 'La contraseña actual es incorrecta.'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'Las nuevas contraseñas no coinciden.'}), 400

    # Validar la contraseña
    validation_errors = validate_password(new_password)

    if validation_errors:
        error_message = 'La contraseña no cumple con los requisitos:<ul>'
        for error in validation_errors:
            error_message += f'<li>{error}</li>'
        error_message += '</ul>'
        return jsonify({'error': error_message}), 400

    # Establecer la nueva contraseña
    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Contraseña actualizada exitosamente.'}), 200


######################## SOPORTE ##########################
# Renderizar la página de contacto
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        groups=Group.query.all()
        return render_template('main/contact.html', groups=Group.query.all()) 
    elif request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        telefono = data.get('telefono')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')

        # Enviar el correo electrónico con formato HTML
        msg = Message('Nueva Solicitud Contacto',
                        sender=('Equipo de Soporte Re-Vibe Ecuador', app.config['MAIL_USERNAME']),
                        recipients=[app.config['MAIL_CONTACT']])
        msg.html = f'''
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="margin: 20px;">
                    <h2 style="color: #2C3E50;">Nueva Solicitud de Contacto</h2>
                    <p>Hola,</p>
                    <p>Hemos recibido una nueva solicitud de contacto. A continuación, se detallan los datos proporcionados:</p>
                    <hr>
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Correo:</strong> {correo}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                    <p><strong>Asunto:</strong> {asunto}</p>
                    <p><strong>Mensaje:</strong></p>
                    <p>{mensaje}</p>
                    <hr>
                    <p>Saludos cordiales,</p>
                    <p>El equipo de soporte</p>
                    <hr>
                    <p style="font-size: 0.9em;">Este es un mensaje automático, por favor no respondas a este correo electrónico.</p>
                </div>
            </body>
        </html>
        '''

        mail.send(msg)
        
        msg_user = Message(
            'Confirmación de Recepción de Solicitud',
            sender=('Equipo de Soporte Re-Vibe Ecuador', app.config['MAIL_USERNAME']),
            recipients=[correo]  # Enviar al correo del usuario
        )

        msg_user.html = f'''
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="margin: 20px;">
                    <h2 style="color: #2C3E50;">Confirmación de Recepción de Solicitud</h2>
                    <p>Hola {nombre},</p>
                    <p>Gracias por ponerte en contacto con nosotros. Hemos recibido tu solicitud y la hemos registrado correctamente.</p>
                    <hr>
                    <p>Estos son los detalles de tu solicitud:</p>
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Correo:</strong> {correo}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                    <p><strong>Asunto:</strong> {asunto}</p>
                    <p><strong>Mensaje:</strong></p>
                    <p>{mensaje}</p>
                    <hr>
                    <p>Nuestro equipo revisará tu solicitud y se pondrá en contacto contigo a la brevedad.</p>
                    <p>Si tienes alguna pregunta adicional, no dudes en responder a este correo.</p>
                    <br>
                    <p>Saludos cordiales,</p>
                    <p>El equipo de soporte de Re-Vibe Ecuador</p>
                    <hr>
                    <p style="font-size: 0.9em;">Este es un mensaje automático, por favor no respondas a este correo electrónico.</p>
                </div>
            </body>
        </html>
        '''

        # Enviar el mensaje
        mail.send(msg_user)

        return jsonify({'message': 'Hemos Recibido tu Solicitud de Contacto!.'}), 200

#####################################################################################

##################### NUEVO PRODUCTO ######################

@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify([{'id': group.id, 'name': group.name} for group in groups])

@app.route('/api/categories/<int:group_id>', methods=['GET'])
def get_categories(group_id):
    categories = Category.query.filter_by(group_id=group_id).all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])

@app.route('/api/subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    subcategories = SubCategory.query.filter_by(category_id=category_id).all()
    return jsonify([{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories])

@app.route('/api/sizes/<int:sub_category_id>', methods=['GET'])
def get_sizes(sub_category_id):
    sizes = Size.query.filter_by(sub_category_id=sub_category_id).all()
    return jsonify([{'id': size.id, 'size': size.size} for size in sizes])

####################### CHATBOT ##########################
# Respuestas básicas del chatbot
responses = {
    '1': {
        'message': 'Para vender, primero necesitas registrarte en nuestra plataforma. Luego, puedes listar tus productos y empezar a vender.',
        'button': {'text': 'Registrarse', 'url': '/register'}
    },
    '2': 'Para comprar, explora nuestra sección de productos y añade los artículos que te interesen a tu carrito. Luego, realiza el pago para completar la compra.',
    '3': 'Para devoluciones, por favor contacta a nuestro soporte con tu número de pedido y el motivo de la devolución.',
    '4': 'Por favor, indícanos tu consulta específica para que podamos ayudarte.',
}

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '').strip()
    
    # Responder con base en el mensaje del usuario
    response = responses.get(user_message, 'Hola, ¿Cuáles opciones necesitas?\n1. Cómo vender\n2. Cómo comprar\n3. Devoluciones\n4. Otros')
    
    # Si la respuesta contiene un botón, incluirlo en la respuesta
    if isinstance(response, dict) and 'button' in response:
        response_message = {
            'message': response['message'],
            'button': response['button']
        }
    else:
        response_message = {'message': response}
    
    return jsonify({'response': response_message})


################## EJECUCION #####################
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
