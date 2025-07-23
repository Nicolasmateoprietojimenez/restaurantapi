from . import db

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    calificacion = db.Column(db.Float)
    telefono = db.Column(db.String(20))
    horario_apertura = db.Column(db.String(10))
    horario_cierre = db.Column(db.String(10))
    estado = db.Column(db.String(20), default='activo')  #activo o inactivo

    mesas = db.relationship('Mesa', backref='restaurante', lazy=True)
    comentarios = db.relationship('Comentario', backref='restaurante', lazy=True)
    fotos = db.relationship('Foto', backref='restaurante', lazy=True)


class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    numero = db.Column(db.String(20))
    capacidad = db.Column(db.Integer)
    ubicacion = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='libre')  # (ocupada libre o mantenimiento)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    contrasena = db.Column(db.String(200), nullable=False) 
    estado = db.Column(db.String(20), default='activo')  # (activo o inactivo)


class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    comentarios = db.Column(db.Text)
    estado = db.Column(db.String(20), default='confirmada')  # (confirmada procesando o cancelada)

class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # (Para identificar si es de portada perfil o para la galeria)
    descripcion = db.Column(db.String(255))


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    comentario = db.Column(db.Text)
    calificacion = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='visible')  # (visisble oculto o reportado)
