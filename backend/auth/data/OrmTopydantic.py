# orm模型转化为pydantic模型
from typing import Optional, List, Type, Literal, Any
from sqlalchemy import  DateTime,inspect
from sqlalchemy.types import String as SAString, Integer as SAInteger, Float as SAFloat
from pydantic import Field, create_model
from sqlalchemy.orm import  DeclarativeBase, RelationshipProperty
import datetime
def orm_to_pydantic(
        orm_model: Type[DeclarativeBase],
        model_type: Literal["create", "response", "update"] = "create",
        exclude_fields: Optional[List[str]] = None,
        model_suffix: str = ""
) -> Type[Any]:
    orm_name = orm_model.__name__
    inspector = inspect(orm_model)
    primary_keys = [col.name for col in inspector.primary_key]
    if exclude_fields is None:
        exclude_fields = []
    if model_type in ["create", "update"]:
        exclude_fields = list(set(exclude_fields + primary_keys))
    # 自动排除 SQLAlchemy 关系属性
    for attr_name, attr_value in orm_model.__dict__.items():
        if isinstance(attr_value, RelationshipProperty):
            exclude_fields.append(attr_name)
    # ========== SQLAlchemy 类型 → Python 原生类型 映射 ==========
    type_mapping = {
        SAInteger: int,
        SAString: str,
        SAFloat: float,
        DateTime: datetime.datetime,
    }
    if model_type == "create":
        field_default = ...
    elif model_type == "update":
        field_default = None
    else:
        field_default = ...
    model_fields = {}
    for name, type_ in orm_model.__annotations__.items():
        if name in exclude_fields:
            continue
        # 提取 Mapped 底层类型
        orm_field_type = type_.__args__[0] if hasattr(type_, "__args__") else type_
        # ========== 应用类型映射，转换为 Python 原生类型 ==========
        python_type = orm_field_type
        # 遍历类型映射，替换 SQLAlchemy 类型
        for sa_type, py_type in type_mapping.items():
            if isinstance(orm_field_type, sa_type) or orm_field_type is sa_type:
                python_type = py_type
                break
        # =================================================================
        comment = inspector.columns[name].comment if name in inspector.columns else ""
        model_fields[name] = (python_type, Field(field_default, description=comment))
    model_name = f"{orm_name}{model_type.capitalize()}{model_suffix}"
    pydantic_model = create_model(model_name, **model_fields)

    return pydantic_model