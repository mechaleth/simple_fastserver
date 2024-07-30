from pydantic import BaseModel
from pathlib import Path
from os.path import join as path_join
from loguru import logger

class LogConfig(BaseModel):
    file_path: str
    file_name: str
    format: str
    rotation: str
    level: str #TODO тут создать enum, пока лееень


# Просто чтобы скрыть детали логгинга
class LocalLoggerData:

    def __init__(self, log_config: LogConfig, logger_name: str):
        common_log_path = log_config.file_path
        # А вдруг не существует такого путя? Ну тогда создаем
        Path(common_log_path).mkdir(parents=True, exist_ok=True)
        common_parser_name = log_config.file_name
        log_path_name = path_join(common_log_path, common_parser_name)
        self._common_logger = logger.bind(logger_name=logger_name)  # имя логгера
        common_parser_logger_filter=lambda record: logger_name==record['extra'].get("logger_name") # функция-фильтр для нового логгера
        self._common_logger.add(log_path_name,
                                format=log_config.format,
                                level=log_config.level,
                                rotation=log_config.rotation,
                                filter=common_parser_logger_filter,
                                encoding='cp1251',
                                compression='zip')

    @property
    def common_logger(self):
        return self._common_logger