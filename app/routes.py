from flask import Blueprint, request, jsonify
from .models import db, Restaurante, Mesa, Cliente, Reserva, Comentario, Foto
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.security import check_password_hash

crud_bp = Blueprint('crud', __name__)

#Endpoint crud restaurante
@crud_bp.route('/restaurantes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_restaurantes():
    if request.method == 'GET':
        restaurantes = Restaurante.query.filter_by(estado='activo').all()
        return jsonify([{
            'id': r.id,
            'nombre': r.nombre,
            'direccion': r.direccion,
            'descripcion': r.descripcion,
            'calificacion': r.calificacion,
            'telefono': r.telefono,
            'horario_apertura': r.horario_apertura,
            'horario_cierre': r.horario_cierre,
            'estado': r.estado,
            'comentarios': [{
                'id': c.id,
                'cliente_id': c.cliente_id,
                'comentario': c.comentario,
                'calificacion': c.calificacion,
                'fecha': c.fecha.isoformat() if c.fecha else None,
                'estado': c.estado
            } for c in r.comentarios if c.estado == 'visible'],
            'fotos': [{
                'id': f.id,
                'url': f.url,
                'tipo': f.tipo,
                'descripcion': f.descripcion
            } for f in r.fotos]
        } for r in restaurantes])

    elif request.method == 'POST':
        data = request.get_json()
        restaurante = Restaurante(**data)
        db.session.add(restaurante)
        db.session.commit()
        return jsonify({'mensaje': 'Restaurante creado', 'id': restaurante.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400
        restaurante = Restaurante.query.get_or_404(id)
        for key, value in data.items():
            setattr(restaurante, key, value)
        db.session.commit()
        return jsonify({'mensaje': 'Restaurante actualizado'})

    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        restaurante = Restaurante.query.get_or_404(id)
        restaurante.estado = 'inactivo'
        db.session.commit()
        return jsonify({'mensaje': 'Restaurante eliminado (soft delete)'})
    
#Endpoint crud mesas
@crud_bp.route('/mesas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_mesas():
    if request.method == 'GET':
        mesas = Mesa.query.filter(Mesa.estado != 'eliminada').all()
        return jsonify([{
            'id': m.id,
            'restaurante_id': m.restaurante_id,
            'numero': m.numero,
            'capacidad': m.capacidad,
            'ubicacion': m.ubicacion,
            'estado': m.estado
        } for m in mesas])

    elif request.method == 'POST':
        data = request.get_json()

        restaurante_id = data.get('restaurante_id')
        if not restaurante_id:
            return jsonify({'error': 'restaurante_id es requerido'}), 400

        cantidad_mesas = Mesa.query.filter_by(restaurante_id=restaurante_id).count()
        if cantidad_mesas >= 15:
            return jsonify({'error': 'El restaurante ya tiene 15 mesas registradas'}), 400

        mesa = Mesa(**data)
        db.session.add(mesa)
        db.session.commit()
        return jsonify({'mensaje': 'Mesa creada', 'id': mesa.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400
        mesa = Mesa.query.get_or_404(id)
        for key, value in data.items():
            setattr(mesa, key, value)
        db.session.commit()
        return jsonify({'mensaje': 'Mesa actualizada'})

    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        mesa = Mesa.query.get_or_404(id)
        db.session.delete(mesa)
        db.session.commit()
        return jsonify({'mensaje': 'Mesa eliminada'})

#Endpoint crud cliente
@crud_bp.route('/clientes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_clientes():
    if request.method == 'GET':
        clientes = Cliente.query.filter_by(estado='activo').all()
        return jsonify([{
            'id': c.id,
            'nombre': c.nombre,
            'email': c.email,
            'telefono': c.telefono,
            'estado': c.estado
        } for c in clientes])

    elif request.method == 'POST':
        data = request.get_json()
        if 'contrasena' in data:
            data['contrasena'] = generate_password_hash(data['contrasena'])
        cliente = Cliente(**data)
        db.session.add(cliente)
        db.session.commit()
        return jsonify({'mensaje': 'Cliente creado', 'id': cliente.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400
        cliente = Cliente.query.get_or_404(id)
        for key, value in data.items():
            if key == 'contrasena':
                setattr(cliente, key, generate_password_hash(value))
            else:
                setattr(cliente, key, value)
        db.session.commit()
        return jsonify({'mensaje': 'Cliente actualizado'})

    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        cliente = Cliente.query.get_or_404(id)
        cliente.estado = 'inactivo'
        db.session.commit()
        return jsonify({'mensaje': 'Cliente eliminado'})
    
#Endpoint crud reservas
@crud_bp.route('/reservas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_reservas():
    if request.method == 'GET':
        reservas = Reserva.query.filter(Reserva.estado != 'cancelada').all()
        return jsonify([{
            'id': r.id,
            'cliente_id': r.cliente_id,
            'restaurante_id': r.restaurante_id,
            'mesa_id': r.mesa_id,
            'fecha': r.fecha.isoformat() if r.fecha else None,
            'comentarios': r.comentarios,
            'estado': r.estado
        } for r in reservas])

    elif request.method == 'POST':
        data = request.get_json()

        cliente_id = data.get('cliente_id')
        restaurante_id = data.get('restaurante_id')
        mesa_id = data.get('mesa_id')
        fecha_str = data.get('fecha')

        if not all([cliente_id, restaurante_id, mesa_id, fecha_str]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        try:
            fecha = datetime.fromisoformat(fecha_str).date()
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD'}), 400
        if fecha < datetime.now().date():
            return jsonify({'error': 'No puedes hacer reservas en fechas pasadas'}), 400
        
        # Validación 1: la mesa ya está reservada ese día
        reserva_existente = Reserva.query.filter_by(
            mesa_id=mesa_id,
            fecha=fecha
        ).filter(Reserva.estado != 'cancelada').first()

        if reserva_existente:
            return jsonify({'error': 'Esa mesa ya está reservada para ese día'}), 400

        # Validación 2: el restaurante tiene 15 reservas ese día
        reservas_restaurante = Reserva.query.filter_by(
            restaurante_id=restaurante_id,
            fecha=fecha
        ).filter(Reserva.estado != 'cancelada').count()

        if reservas_restaurante >= 15:
            return jsonify({'error': 'Este restaurante ya tiene 15 reservas para ese día'}), 400

        # Validación 3: no se permiten más de 20 reservas globales ese día
        reservas_totales = Reserva.query.filter_by(
            fecha=fecha
        ).filter(Reserva.estado != 'cancelada').count()

        if reservas_totales >= 20:
            return jsonify({'error': 'Ya se alcanzó el máximo de 20 reservas globales para ese día'}), 400

        # Validación 4: el cliente ya tiene una reserva ese día en el restaurante
        reserva_cliente = Reserva.query.filter_by(
            cliente_id=cliente_id,
            restaurante_id=restaurante_id,
            fecha=fecha
        ).filter(Reserva.estado != 'cancelada').first()

        if reserva_cliente:
            return jsonify({'error': 'Ya tienes una reserva en este restaurante para ese día'}), 400

        if reserva_cliente:
            return jsonify({'error': 'Ya tienes una reserva registrada para ese día'}), 400
        
        # Crear reserva si pasó todas las validaciones
        reserva = Reserva(
            cliente_id=cliente_id,
            restaurante_id=restaurante_id,
            mesa_id=mesa_id,
            fecha=fecha,
            comentarios=data.get('comentarios'),
            estado=data.get('estado', 'confirmada')
        )
        mesa = Mesa.query.get(mesa_id)
        if mesa:
            mesa.estado = 'ocupada'
        db.session.add(reserva)
        db.session.commit()
        return jsonify({'mensaje': 'Reserva creada', 'id': reserva.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400
        reserva = Reserva.query.get_or_404(id)
        for key, value in data.items():
            setattr(reserva, key, value)
        db.session.commit()
        return jsonify({'mensaje': 'Reserva actualizada'})

    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        reserva = Reserva.query.get_or_404(id)
        reserva.estado = 'cancelada'
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({'mensaje': 'Reserva cancelada '})
    
#Endpoint crud comentarios    
@crud_bp.route('/comentarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_comentarios():
    if request.method == 'GET':
        comentarios = Comentario.query.filter(Comentario.estado != 'oculto').all()
        return jsonify([{
            'id': c.id,
            'restaurante_id': c.restaurante_id,
            'cliente_id': c.cliente_id,
            'comentario': c.comentario,
            'calificacion': c.calificacion,
            'fecha': c.fecha.isoformat() if c.fecha else None,
            'estado': c.estado
        } for c in comentarios])

    elif request.method == 'POST':
        data = request.get_json()

        # Parsear fecha si viene
        fecha_str = data.get('fecha')
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.fromisoformat(fecha_str)
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD o ISO 8601'}), 400

        comentario = Comentario(
            restaurante_id=data['restaurante_id'],
            cliente_id=data.get('cliente_id'),
            comentario=data.get('comentario'),
            calificacion=data.get('calificacion'),
            fecha=fecha,
            estado=data.get('estado', 'visible')
        )
        db.session.add(comentario)
        db.session.commit()
        return jsonify({'mensaje': 'Comentario creado', 'id': comentario.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400

        comentario = Comentario.query.get_or_404(id)

        for key, value in data.items():
            if key == 'fecha' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD o ISO 8601'}), 400
            setattr(comentario, key, value)

        db.session.commit()
        return jsonify({'mensaje': 'Comentario actualizado'})
    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        comentario = Comentario.query.get_or_404(id)
        db.session.delete(comentario)
        db.session.commit()
        return jsonify({'mensaje': 'Comentario ocultado (soft delete)'})


@crud_bp.route('/fotos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_fotos():
    if request.method == 'GET':
        fotos = Foto.query.all()
        return jsonify([{
            'id': f.id,
            'restaurante_id': f.restaurante_id,
            'url': f.url,
            'tipo': f.tipo,
            'descripcion': f.descripcion
        } for f in fotos])

    elif request.method == 'POST':
        data = request.get_json()
        foto = Foto(
            restaurante_id=data['restaurante_id'],
            url=data['url'],
            tipo=data['tipo'],
            descripcion=data.get('descripcion')
        )
        db.session.add(foto)
        db.session.commit()
        return jsonify({'mensaje': 'Foto creada', 'id': foto.id}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para actualizar'}), 400
        foto = Foto.query.get_or_404(id)
        for key, value in data.items():
            setattr(foto, key, value)
        db.session.commit()
        return jsonify({'mensaje': 'Foto actualizada'})

    elif request.method == 'DELETE':
        data = request.get_json()
        id = data.get('id')
        if not id:
            return jsonify({'error': 'ID requerido para eliminar'}), 400
        foto = Foto.query.get_or_404(id)
        db.session.delete(foto)
        db.session.commit()
        return jsonify({'mensaje': 'Foto eliminada'})


# Lista de restaurantes con información completa
@crud_bp.route('/restaurante/<int:id>', methods=['GET'])
def obtener_restaurante(id):
    restaurante = Restaurante.query.get_or_404(id)

    if restaurante.estado != 'activo':
        return jsonify({'error': 'Restaurante inactivo'}), 404

    return jsonify({
        'id': restaurante.id,
        'nombre': restaurante.nombre,
        'direccion': restaurante.direccion,
        'descripcion': restaurante.descripcion,
        'calificacion': restaurante.calificacion,
        'telefono': restaurante.telefono,
        'horario_apertura': restaurante.horario_apertura,
        'horario_cierre': restaurante.horario_cierre,
        'estado': restaurante.estado,
        'comentarios': [{
            'id': c.id,
            'cliente_id': c.cliente_id,
            'comentario': c.comentario,
            'calificacion': c.calificacion,
            'fecha': c.fecha.isoformat() if c.fecha else None,
            'estado': c.estado
        } for c in restaurante.comentarios if c.estado == 'visible'],
        'fotos': [{
            'id': f.id,
            'url': f.url,
            'tipo': f.tipo,
            'descripcion': f.descripcion
        } for f in restaurante.fotos],
        'mesas_disponibles': [{
            'id': m.id,
            'numero': m.numero,
            'capacidad': m.capacidad,
            'ubicacion': m.ubicacion,
            'estado': m.estado
        } for m in restaurante.mesas if m.estado == 'libre']
    })

@crud_bp.route('/login', methods=['POST'])
def login_cliente():
    data = request.get_json()
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not email or not contrasena:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400

    cliente = Cliente.query.filter_by(email=email, estado='activo').first()

    if not cliente or not check_password_hash(cliente.contrasena, contrasena):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    return jsonify({'mensaje': 'Login exitoso', 'cliente_id': cliente.id})
