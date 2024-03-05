from flask import jsonify, request
from db import db
from models.category import Categories, category_schema, categories_schema
from util.reflections import populate_object


def create_category(req):
    post_data = req.form if req.form else req.json

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({"message": "category name is required"}), 400

    new_category = Categories(category_name)
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "category added", "category": category_schema.dump(new_category)}), 201
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400


def get_all_categories():
    categories = Categories.query.all()
    return jsonify({'message': 'categories found', 'results': categories_schema.dump(categories)}), 200


def get_category_by_id(id):
    category = Categories.query.get(id)

    if category:
        return jsonify({'category': category_schema.dump(category)}), 200

    return jsonify({'message': 'Category not found'}), 404


def update_category(id):
    data = request.get_json()
    category = Categories.query.get(id)

    if category:
        if 'category_name' in data:
            category.category_name = data['category_name']
            populate_object(category, data)
            try:
                db.session.commit()
                return jsonify({'message': 'Category updated successfully', 'category': category_schema.dump(category)}), 200
            except:
                db.session.rollback()
                return jsonify({'message': 'Category update failed'}), 500

    return jsonify({'message': 'Category not found'}), 404


def delete_category(id):
    category = Categories.query.get(id)

    if category:
        try:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category deleted successfully'}), 200
        except:
            db.session.rollback()
            return jsonify({'message': 'Category deletion failed'}), 500

    return jsonify({'message': 'Category not found'}), 404
