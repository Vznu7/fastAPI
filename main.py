from fastapi import FastAPI,Depends
from models import Product
from fastapi.middleware.cors import CORSMiddleware
from database import session , engine
import databse_models
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:3000"],
    allow_methods =["*"],
    # allow_headers=["*"],


)
databse_models.Base.metadata.create_all(bind = engine)


@app.get("/")
def greet():
    return "ASALAMALAIKUM LYARII"


products = [
    Product(
        id=1,
        name="Smart TV",
        description="42-inch full HD smart television",
        price=19999.0,
        quantity=10
    ),
    Product(
        id=2,
        name="Laptop",
        description="Lightweight laptop with 16GB RAM",
        price=55999.0,
        quantity=5
    ),
    Product(
        id=3,
        name="Bluetooth Speaker",
        description="Portable wireless speaker with deep bass",
        price=2499.0,
        quantity=20
    ),
    Product(
        id=4,
        name="Smartphone",
        description="5G smartphone with AMOLED display",
        price=29999.0,
        quantity=15
    ),
    Product(
        id=5,
        name="Wireless Earbuds",
        description="Noise-cancelling true wireless earbuds",
        price=3999.0,
        quantity=25
    )
]



def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():

    db = session()

    count =db.query(databse_models.Product).count
    if count == 0:

        for product in products:
            db.add(databse_models.Product(**product.model_dump()))
        db.commit()
init_db()


@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(databse_models.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product = db.query(databse_models.Product).filter(databse_models.Product.id == id).first()
    if  db_product:
        return db_product 
    return "product not found"



@app.post("/products")
def add_product(product:Product,db:Session = Depends(get_db)):
    db.add(databse_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session = Depends(get_db)):
    db_product = db.query(databse_models.Product).filter(databse_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated successfully"
    else:
        return f"no product found on id named {id}"



@app.delete("/products/{id}")
def delete_product(id:int,db:Session = Depends(get_db)):
    db_product= db.query(databse_models.Product).filter(databse_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "deleted successfully"
    else:
        return "product not in list"




