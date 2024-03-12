from flask import jsonify
from db import db
from models.products import Products, product_schema, products_schema
from models.category import Categories
from util.reflections import populate_object
from lib.authenticate import auth, auth_admin


@auth_admin
def create_product(req):
    post_data = req.form if req.form else req.json

    product_name = post_data.get('product_name')
    exists_query = db.session.query(Products).filter(Products.product_name == product_name).first()

    if exists_query:
        return jsonify({'message': f'product "{product_name}" already exists in the database'}), 400

    new_product = Products.new_product_obj()

    populate_object(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'product could not be created'}), 400

    return jsonify({'message': 'product created', 'result': product_schema.dump(new_product)}), 201


@auth
def get_all_products(req):
    product_query = db.session.query(Products).all()

    return jsonify({'message': 'products found', 'result': products_schema.dump(product_query)}), 200


@auth
def get_product_by_id(req, product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    return jsonify({'message': 'product found', 'result': product_schema.dump(product_query)}), 200


@auth
def get_active_products(req):

    product_query = db.session.query(Products).filter(Products.active == True).all()
    return jsonify({'message': 'Active products found', 'result': products_schema.dump(product_query)}), 200


@auth
def get_products_by_company_id(company_id):

    product_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not product_query:
        return jsonify({'message': f'No products found for company {company_id}'}), 404

    return jsonify({'message': f'Products for company {company_id} found', 'result': products_schema.dump(product_query)}), 200


@auth_admin
def update_product(req, product_id):
    post_data = req.form if req.form else req.json
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    populate_object(product_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'product could not be updated'}), 400

    return jsonify({'message': 'product updated', 'result': product_schema.dump(product_query)}), 200


@auth_admin
def product_add_category(req):
    post_data = req.form if req.form else req.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()

    return jsonify({'message': 'relationship added.', 'product info': product_schema.dump(product_query)}), 200


@auth_admin
def delete_product(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": f"product by id {product_id} does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "product has been deleted"}), 200
