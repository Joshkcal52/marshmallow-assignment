from flask import Blueprint, request
import controllers

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def create_category_route():
    return controllers.create_category(request)


@category.route('/categories', methods=['GET'])
def get_all_categories_route():
    return controllers.get_all_categories(request)


@category.route('/category/<id>', methods=['GET'])
def get_category_by_id_route(id):
    return controllers.get_category_by_id(request, id)


@category.route('/category/<id>', methods=['PUT'])
def update_category_route(id):
    return controllers.update_category(id)


@category.route('/category/delete/<id>', methods=['DELETE'])
def delete_category_by_id_route(id):
    return controllers.delete_category(id)
