# generated by datamodel-codegen:
#   filename:  JSON_schema_meta.json
#   timestamp: 2024-04-01T11:05:53+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, constr, ValidationError, root_validator, validator


class BaseSubStruct(BaseModel):
    name: str = Field(description="Some name")
    number: int = Field(description="Some number")

class BaseStruct(BaseModel):
    main_name: str = Field(description="some main name")
    some_base_struct: List[BaseSubStruct] = Field("Some silent array")