from typing import List , Optional
from sqlalchemy import ForeignKey , String , create_engine , LargeBinary
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column , relationship , Session


class Base(DeclarativeBase):
    pass

class Product (Base):
    __tablename__ = "products"

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dicreption: Mapped[str] = mapped_column(String(100))
    price: Mapped[str] = mapped_column(String(30))
    discount: Mapped[str] = mapped_column(String(50) )
    image: Mapped[bytes] = mapped_column( LargeBinary , nullable=True)
    link: Mapped[str] = mapped_column(String())

class Login (Base):
    __tablename__ = "login"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    password : Mapped[str] = mapped_column(String(50))

engine = create_engine("sqlite:///database.db", echo=False)
Base.metadata.create_all(engine)    



def product_save(name , dicreption , price , discount , image , link):

    with Session(engine) as session:
        product_Save = Product(name=name , dicreption=dicreption , price=price , discount=discount , image=image , link=link)

        session.add(product_Save)
        session.commit()


def Login_save(name , password):
    with Session(engine) as session:
        login_save = Login(name=name , password=password)

        session.add(login_save)
        session.commit()


def Show_product():
    with Session(engine) as db:
        return db.query(Product).all()
