import json
from fastapi import APIRouter, FastAPI, File, Response
from fastapi.responses import JSONResponse
from starlette import status
import uvicorn

from verificator_manager import ManagerStates, verificator_manager


context = ""

prefix_router = APIRouter(prefix=context)

# todo пока секьюрность на нуле
app = FastAPI(title="Сервис парсинга/расчётов по методике для формирования документации для СИЭР",
              description="""Внешний Python-сервис для верификации json""",
              version="0.0.1",
              docs_url=f"{context}/docs",
              redoc_url=f"{context}/redoc",
              openapi_url=f'{context}/openapi.json')  # noqa: pylint=invalid-name


# todo: вынести в отдельный тест
@prefix_router.post("/test_json_load", summary="Верификация JSON по файлу json")
async def test_json_load(*, file_bytes: bytes = File()):
    json_data = json.loads(file_bytes.decode('utf-8'))
    with open('test_data/test_get_data.json', 'wb') as f:
        f.write(file_bytes)
    with open('test_data/test_get_data_1.json', 'w') as f:
        json.dump(json_data, f)

# Эта проверка дико плоха, так как вообще не понятно, где ошибка
# @prefix_router.post("/verificate_schema_only", summary="Верификация JSON по телу запроса")
# async def test_json_get(body: ModelDatabaseSchema):
#     return Response(status_code=status.HTTP_200_OK)


def verificate_base_json(json_data: dict):
    verification_state = verificator_manager(json_data)
    if verification_state.state==ManagerStates.PARSED_SUCCESSFULLY:
        return Response(status_code=status.HTTP_200_OK)
    return JSONResponse(verification_state.message._asdict(),
                        status_code=status.HTTP_400_BAD_REQUEST)

@prefix_router.post("/verificate_by_json", summary="Верификация JSON по файлу json")
async def verificate_by_json(*, file_bytes: bytes = File()):
    json_data = json.loads(file_bytes.decode('utf-8'))
    return verificate_base_json(json_data)
    


app.include_router(prefix_router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)