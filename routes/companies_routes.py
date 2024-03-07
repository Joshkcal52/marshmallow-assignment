from flask import Blueprint, request
import controllers

company = Blueprint('company', __name__)


@company.route('/company', methods=['POST'])
def create_company_route():
    return controllers.create_company(request)


@company.route('/companies', methods=['GET'])
def get_all_companies_route():
    return controllers.get_all_companies()


@company.route('/company/<id>', methods=['GET'])
def get_company_by_id_route(id):
    return controllers.get_company_by_id(id)


@company.route('/company/<id>', methods=['PUT'])
def update_company_route(id):
    return controllers.update_company(request, id)


@company.route('/company/delete/<id>', methods=['DELETE'])
def delete_company_route(id):
    return controllers.delete_company(id)
