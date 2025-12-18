"""SQLAlchemy ORM - E-commerce Models"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nombre = Column(String(100))
    fecha_registro = Column(DateTime, default=datetime.now)
    activo = Column(Boolean, default=True)
    
    ordenes = relationship("Orden", back_populates="usuario")

class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Orden(Base):
    __tablename__ = 'ordenes'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float)
    
    usuario = relationship("Usuario", back_populates="ordenes")

# Database setup
def setup_database(db_url='sqlite:///ecommerce.db'):
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# CRUD operations
def crear_usuario(session, email, nombre):
    usuario = Usuario(email=email, nombre=nombre)
    session.add(usuario)
    session.commit()
    return usuario

def crear_producto(session, nombre, precio, stock):
    producto = Producto(nombre=nombre, precio=precio, stock=stock)
    session.add(producto)
    session.commit()
    return producto

def listar_usuarios(session):
    return session.query(Usuario).all()

if __name__ == "__main__":
    session = setup_database()
    
    # Ejemplos
    usuario = crear_usuario(session, "test@example.com", "Test User")
    producto = crear_producto(session, "Laptop", 1299.99, 10)
    
    print(f"✅ Usuario creado: {usuario.email}")
    print(f"✅ Producto creado: {producto.nombre}")
    
    usuarios = listar_usuarios(session)
    print(f"\n📊 Total usuarios: {len(usuarios)}")
