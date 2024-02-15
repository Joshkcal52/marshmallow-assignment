from flask import jsonify

# obj = the_actual_record_in_the_db
# data_dictionary = post_data


def populate_object(obj, data_dictionary):
    fields = data_dictionary.keys()

    for field in fields:
        try:
            getattr(obj, field)
            setattr(obj, field, data_dictionary[field])

        except AttributeError:
            return jsonify({'message': f'attribute {field} not in obj'})
