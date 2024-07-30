from local_parser_core.local_parser_core import ErrorMessage, ParsingStates
import schema_model.json_model.json_model as json_model


def create_good_database_data() -> dict:
    substruct_1 = {
        'name': 'Ololo',
        'number': 9
    }
    substruct_2 = {
        'name': 'Ha ha',
        'number': 12}
    
    return {
                'main_name': 'Main name',
                'some_base_struct': [substruct_1, substruct_2]
            }


def create_bad_database_data() -> dict:
    substruct_1 = {
        'number': 9
    }
    substruct_2 = {
        'name': 'Ha ha',
        'number': 12}
    
    return {
                'main_name': 'Main name',
                'some_base_struct': [substruct_1, substruct_2]
            }



def create_good_model_data():
    return json_model.BaseStruct.model_validate(create_good_database_data())