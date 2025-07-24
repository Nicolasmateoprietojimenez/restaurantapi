from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import Restaurante, Mesa, Cliente, Reserva, Foto, Comentario
from . import db
from flask_admin import Admin, AdminIndexView, expose
from flask import render_template

def init_admin(app):
    admin = Admin(app, name='Panel de Administración', index_view=MyAdminHome(), template_mode='bootstrap4')


    admin.add_view(RestauranteAdmin(Restaurante, db.session))
    admin.add_view(MesaAdmin(Mesa, db.session))
    admin.add_view(ModelView(Cliente, db.session))
    admin.add_view(ReservaAdmin(Reserva, db.session))
    admin.add_view(FotoAdmin(Foto, db.session))
    admin.add_view(ModelView(Comentario, db.session))


class MesaAdmin(ModelView):
    column_list = ['id', 'restaurante_id', 'numero', 'capacidad','ubicacion', 'estado']
class FotoAdmin(ModelView):
    form_columns = ['restaurante_id', 'url', 'tipo', 'descripcion']
class ReservaAdmin(ModelView):
    form_columns = ['cliente_id','restaurante_id', 'mesa_id', 'fecha', 'comentarios','estado']    
    column_list = ['cliente_id','restaurante_id', 'mesa_id', 'fecha', 'comentarios','estado']   
class RestauranteAdmin(ModelView):
    column_list = ['id', 'nombre', 'direccion', 'estado']
    
    
class MyAdminHome(AdminIndexView):
    @expose('/')
    def index(self):

        #Conteo de totales por modelo
        total_restaurantes = Restaurante.query.count()
        total_mesas = Mesa.query.count()
        total_reservas = Reserva.query.count()
        total_clientes = Cliente.query.count()

        # Top 5 restaurantes con mas reservas
        from sqlalchemy import func
        reservas_por_restaurante = db.session.query(
            Restaurante.nombre,
            func.count(Reserva.id)
        ).join(Reserva).group_by(Restaurante.id).order_by(func.count(Reserva.id).desc()).limit(5).all()

        top_restaurantes_nombres = [r[0] for r in reservas_por_restaurante]
        top_restaurantes_reservas = [r[1] for r in reservas_por_restaurante]

        # Clientes unicos por restaurante
        clientes_por_restaurante = db.session.query(
            Restaurante.nombre,
            func.count(func.distinct(Reserva.cliente_id))
        ).join(Reserva).group_by(Restaurante.id).order_by(func.count(func.distinct(Reserva.cliente_id)).desc()).limit(5).all()

        clientes_restaurantes_nombres = [r[0] for r in clientes_por_restaurante]
        clientes_restaurantes_cantidad = [r[1] for r in clientes_por_restaurante]
        
        top_clientes = db.session.query(
            Cliente.nombre, func.count(Reserva.id)
        ).join(Reserva).group_by(Cliente.id).order_by(func.count(Reserva.id).desc()).limit(5).all()

        top_clientes_nombres = [c[0] for c in top_clientes]
        top_clientes_reservas = [c[1] for c in top_clientes]


        #Top 3 restaurantes con mejor valoraicon 
        top_valorados = db.session.query(
            Restaurante.nombre,
            func.avg(Comentario.calificacion)
        ).join(Comentario).filter(
            Comentario.calificacion.isnot(None)
        ).group_by(Restaurante.id).order_by(func.avg(Comentario.calificacion).desc()).limit(3).all()



        #Estado de las mesas
        
        estados_mesas = db.session.query(
            Mesa.estado, func.count()
        ).group_by(Mesa.estado).all()

        mesas_estados_labels = [e[0] for e in estados_mesas]
        mesas_estados_valores = [e[1] for e in estados_mesas]
        top_valorados_nombres = [r[0] for r in top_valorados]
        top_valorados_promedios = [round(r[1], 2) for r in top_valorados]
        return self.render('admin/home.html',
            total_restaurantes=total_restaurantes,
            total_mesas=total_mesas,
            total_reservas=total_reservas,
            total_clientes=total_clientes,
            
            top_restaurantes_nombres=top_restaurantes_nombres,
            top_restaurantes_reservas=top_restaurantes_reservas,
            clientes_restaurantes_nombres=clientes_restaurantes_nombres,
            clientes_restaurantes_cantidad=clientes_restaurantes_cantidad,
            
            top_clientes_nombres=top_clientes_nombres,
            top_clientes_reservas=top_clientes_reservas,
            
            top_valorados_nombres=top_valorados_nombres,
            top_valorados_promedios=top_valorados_promedios,
            mesas_estados_labels=mesas_estados_labels,
            mesas_estados_valores=mesas_estados_valores
        )
