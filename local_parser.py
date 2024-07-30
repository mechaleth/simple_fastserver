from schema_model.json_model.json_model import BaseStruct

from local_parser_core.local_parser_core import Model_Parsing_Core, ParsingStates
from common_logs_settings.create_logger import LocalLoggerData, LogConfig


import configparser


_log_config = configparser.ConfigParser()
_log_config.read('./configs/log_configs.cfg')


# Просто чтобы скрыть детали логгинга
common_parser_logger = LocalLoggerData(LogConfig.model_validate(_log_config['parser.common']),
                                       "parcer_common_logger").common_logger


class Model_Parsing(Model_Parsing_Core):
    def __init__(self, json_data: dict):
        super().__init__(json_data)
        common_parser_logger.info(f"Инициализирован парсер dict-объекта целевого JSON")
        if self._data_parced_state.state == ParsingStates.NOT_PARSED:
            common_parser_logger.error(f'"Ошибки при парсинге - JSON-объект не соответствует целевой структуре": {self._data_parced_state}')
            return
        common_parser_logger.info("Парсинг произведён успешно")

    @staticmethod
    def _parse_model(json_data: dict) -> BaseStruct:
        return BaseStruct.model_validate(json_data)