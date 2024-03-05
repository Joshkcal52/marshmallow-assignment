from flask import jsonify, request
from db import db
from models.company import Companies, company_schema, companies_schema
from util.reflections import populate_object


def create_company(req):
    post_data = req.form if req.form else req.json

    company_name = post_data.get('company_name')

    if not company_name:
        return jsonify({"message": "Company name is required"}), 400

    new_company = Companies(company_name)
    populate_object(new_company, post_data)

    try:
        db.session.add(new_company)
        db.session.commit()
        return jsonify({"message": "Company added", "company": company_schema.dump(new_company)}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Unable to create record"}), 400


def get_all_companies():
    companies = Companies.query.all()
    return jsonify({'message': 'Companies found', 'results': companies_schema.dump(companies)}), 200


def get_company_by_id(id):
    company = Companies.query.get(id)

    if company:
        return jsonify({'company': company_schema.dump(company)}), 200

    return jsonify({'message': 'Company not found'}), 404


def update_company(id):
    data = request.get_json()
    company = Companies.query.get(id)

    if company:
        if 'company_name' in data:
            company.company_name = data['company_name']
            populate_object(company, data)
            try:
                db.session.commit()
                return jsonify({'message': 'Company updated successfully', 'company': company_schema.dump(company)}), 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({'message': 'Company update failed'}), 500

    return jsonify({'message': 'Company not found'}), 404


def delete_company(id):
    company = Companies.query.get(id)

    if company:
        try:
            db.session.delete(company)
            db.session.commit()
            return jsonify({'message': 'Company deleted successfully'}), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'message': 'Company deletion failed'}), 500

    return jsonify({'message': 'Company not found'}), 404
