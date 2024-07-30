from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, NamedTuple, Union
from enum import IntEnum, auto
from pydantic import BaseModel, ValidationError


_main_fields=MappingProxyType({'attributes' : 'name',
                               'tables' : 'name',
                               'schema' : 'name'})


class MainEntitiesName:
    def __init__(self):
        self._datadict = {}

    def add_data(self, key, val):
        assert key in _main_fields, "Такому значению нет сопоставления"
        self._datadict[key] = val
   
    @property
    def attributes(self):
        return {key: val for key, val in self._datadict.items() if val is not None and len(val) > 0}

    def __repr__(self):
        return str(self._datadict)

# мне похер, если я задал путь к list или json, я его должен увидеть

# попробуй рекурсию с last_level_name = 'attributes', например, и дальше получаешь name
# короче, напиши функцию, которая вызывает саму себя и возвращает JSON с текущего уровня
class Pathfinder:
    def __init__(self, json_file, pathway_tuple: tuple):
        self._errors = MainEntitiesName()
        self._pathway: tuple = pathway_tuple
        self._final_entity = self._get_next_level_data(json_file, pathway_tuple, None)
        
    # функция, по сути, метод класса, она завязана на get_next_level_data
    def _get_next_level_data(self, json_file, pathway: tuple, last_level_name: str = None) -> Union[dict, list, Any]:
        # условие выхода из рекурсии
        if len(pathway) == 0:
            # если путь пуст, то возвращаем json_file, мы в точке назначения 
            return json_file
        # отрабатываем по маршруту
        current_level_name = pathway[0]
        # там же может быть говно, нужны проверки ключа
        if isinstance(json_file, dict):
            next_level_json = json_file.get(current_level_name, None)
        elif isinstance(json_file, (list, tuple)):
            if not isinstance(current_level_name, int):
                next_level_json = None
            elif current_level_name >= len(json_file):
                next_level_json = None
            else:
                next_level_json = json_file[current_level_name]
        # если дальше идти не можем, то всё
        if next_level_json is None:
            return json_file
        if isinstance(next_level_json, (list, tuple)):
            return self._get_next_level_data(next_level_json, pathway[1:], current_level_name)
        elif isinstance(next_level_json, dict):
            if last_level_name in _main_fields:
                self._errors.add_data(last_level_name, next_level_json[_main_fields[last_level_name]])
            return self._get_next_level_data(next_level_json, pathway[1:], last_level_name)
        else:
            return next_level_json
    
    @property
    def entity_pathway_main_entities(self) -> dict:
        return self._errors.attributes

    @property
    def entity_pathway_str(self) -> str:
        return '.'.join(str(x) for x in self._pathway)
    
    @property
    def entity_pathway_tuple(self) -> tuple:
        return self._pathway

    @property
    def final_entity(self):
        return self._final_entity

def flatten_dict(d):
    if isinstance(d, dict):
        result = {}
        for key, value in d.items():
            if isinstance(value, (dict, list, tuple)):
                result[key] = type(value).__name__
            else:
                result[key] = value
    elif isinstance(d, (list, tuple)):
        result = type(d).__name__
    else:
        result = d
    return result


class ParsingStates(IntEnum):
    INITED = auto()
    FILE_OPENED = auto()
    DATA_READ = auto()
    DATA_WIP = auto()
    PARSER_SET = auto()
    PARSED_WELL = auto()
    NOT_PARSED = auto()

class ErrorLocationData:
    __slots__ = ('_main_entities', '_pathway')
    def __init__(self, main_entities: str,
                       pathway: str):
        self._main_entities = main_entities
        self._pathway = pathway

    @property
    def error_location_data(self) -> dict:
        return {'main_entities': self._main_entities,
                'pathway': self._pathway}

    def __repr__(self):
        return str(self.error_location_data)


class ErrorData:
    __slots__ = (
        "_type",
        "_error_message",
        "_location",
        "_final_value",
    )

    def __init__(self, error_type: str,
                       error_message: str,
                       location: ErrorLocationData,
                       final_entity: Union[dict, list, Any],
                ):
        if not isinstance(location, ErrorLocationData):
            raise ValueError(f"Uncorrect datatype {type(location)} vas set in parser error location, need a {self.ErrorLocationData.__name__}")
        self._type = error_type
        self._error_message = error_message
        self._location = location
        self._final_value = flatten_dict(final_entity)

    @property
    def description(self):
        return {'type': self._type,
                'error': self._error_message,
                'location' : self._location.error_location_data,
                'final_value' : self._final_value
                }

    def __repr__(self):
        return str(self.description)

class ErrorMessage:
    def __init__(self, message: str, description: dict) -> None:
        self.message = message
        if not isinstance(description, dict):
            raise ValueError(f"Uncorrect datatype {type(description)} vas set in parser error location, need a {dict.__name__}")
        self._description = description

    def __repr__(self):
        return str(self._asdict())

    def _asdict(self):
        return {'message': self.message,
                'description': self._description}

    @property
    def description(self):
        return self._description


class StatesData:
    __slots__ = ('_state',
                 '_state_message')

    def __init__(self,
                 state: ParsingStates,
                 state_message: Union[str, ErrorMessage] = "Некорректная обработка данных"
                 ):
        self._state = state
        if not isinstance(state_message, (str, ErrorMessage)):
            raise ValueError(f"Uncorrect datatype {type(state_message)} vas set in parser error location, need a {ErrorMessage.__name__} or str") 
        if isinstance(state_message, str):
            self._state_message = ErrorMessage(message=state_message, description={})
        else:
            self._state_message = state_message

    @property
    def state(self) -> bool:
        return self._state

    @property
    def message(self) -> ErrorMessage:
        return self._state_message

    def __repr__(self) -> str:
        return str({'state': self.state,
                    'message': self.message})



class Model_Parsing_Core(ABC):
    def __init__(self, json_data: dict):
        self._data_parced_state = StatesData(ParsingStates.INITED, "Попытка парсинга JSON-объекта")
        try:
            self._model_data = self._parse_model(json_data)
            self._data_parced_state = self._data_parced_state = StatesData(ParsingStates.PARSED_WELL,
                                                                           "JSON-объект успешно считан и соответствует целевой структуре")
        except ValidationError as val_err:
            self._data_parced_mark = False
            for error_msg in val_err.errors():
                error_path = Pathfinder(json_data, error_msg['loc'])
                self._data_parced_state = StatesData(ParsingStates.NOT_PARSED,
                                                     ErrorMessage(message="Ошибка при разборе структуры",
                                                                  description=ErrorData(error_type=error_msg['type'],
                                                                                        error_message=error_msg['msg'],
                                                                                        location=ErrorLocationData(main_entities=error_path.entity_pathway_main_entities,
                                                                                                                   pathway=error_path.entity_pathway_str),
                                                                                        final_entity=error_path.final_entity).description
                                                                 )
                                                            )

    @staticmethod
    @abstractmethod
    def _parse_model(json_data: dict) -> BaseModel:
        pass


    @property
    def parsed_well(self):
        return self._data_parced_state.state == ParsingStates.PARSED_WELL

    @property
    def parser_final_state(self) -> StatesData:
        return self._data_parced_state

    @property
    def model_data(self) -> BaseModel:
        return self._model_data