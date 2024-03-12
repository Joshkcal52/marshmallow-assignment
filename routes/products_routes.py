from flask import Blueprint, request
import controllers

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def create_product_route():
    return controllers.create_product(request)


@products.route('/products', methods=['GET'])
def get_all_products_route():
    return controllers.get_all_products(request)


@products.route('/product/<id>', methods=['GET'])
def get_product_by_id_route(id):
    return controllers.get_product_by_id(request, id)


@products.route('/product/<id>', methods=['PUT'])
def update_product_route(id):
    return controllers.update_product(request, id)


@products.route('/products/active', methods=['GET'])
def get_active_products_route():
    return controllers.get_active_products(request)


@products.route('/product/category', methods=['POST'])
def product_add_category():
    return controllers.product_add_category(request)


@products.route('/products/company/<company_id>', methods=['GET'])
def get_products_by_company_id_route(company_id):
    return controllers.get_products_by_company_id(company_id)


@products.route('/product/delete/<id>', methods=['DELETE'])
def delete_product_route(id):
    return controllers.delete_product(id)
