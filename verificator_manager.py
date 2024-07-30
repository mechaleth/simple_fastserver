from enum import IntEnum, auto
from local_parser import Model_Parsing
from states_data import ErrorMessage, StatesData


class ManagerStates(IntEnum):
    NOT_PARSED = auto()
    PARSED_SUCCESSFULLY = auto()
    

def verificator_manager(json_model: dict):
    parser = Model_Parsing(json_model)
    if not parser.parsed_well:
        final_state = parser.parser_final_state
        return StatesData(state=ManagerStates.NOT_PARSED,
                          state_message=ErrorMessage(message=final_state.message.message,
                                                     description=final_state.message.description))
    return StatesData(state=ManagerStates.PARSED_SUCCESSFULLY,
                      state_message="Модель успешно проверена")
    
    