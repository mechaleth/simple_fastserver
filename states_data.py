from enum import IntEnum, auto
from typing import NamedTuple, Union


class Level(IntEnum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()

class ErrorMessage(NamedTuple):
    message: str
    description: dict

    def __repr__(self):
        return str({'message': self.message,
                    'description': self.description})


class StatesData:
    __slots__ = ('_state',
                 '_level',
                 '_state_message')

    def __init__(self,
                 state: IntEnum,
                 state_message: Union[str, ErrorMessage] = "Некорректная обработка данных",
                 level: Level = Level.ERROR,
                 ):
        self._state = state
        self._level = level
        if not isinstance(state_message, (str, ErrorMessage)):
            raise ValueError(f"Uncorrect datatype {type(state_message)} vas set in parser error location, need a {ErrorMessage.__name__} or str") 
        if isinstance(state_message, str):
            self._state_message = ErrorMessage(message=state_message, description={})
        else:
            self._state_message = state_message

    @property
    def state(self) -> IntEnum:
        return self._state

    @property
    def level(self) -> Level:
        return self._level

    @property
    def message(self) -> ErrorMessage:
        return self._state_message