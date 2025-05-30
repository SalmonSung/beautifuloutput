from typing import Type, Dict
from pydantic import BaseModel, Field
import re
from pydantic.fields import FieldInfo
from beautifuloutput.prompts import *

# def retrieve_pydantic(item: BaseModel) -> dict:
#     cls = item.__class__
#     # class_name = cls.__name__
#     # print(class_name)
#     str_dict = {}
#     for attr_name, model_field in cls.model_fields.items():
#         # print("===================================================")
#         # print(f"Attribute name: {attr_name}")
#         # print(f"Type: {model_field.annotation}")
#         # print(f"Model field: {model_field}")
#         # print(f"Description: {model_field.description}")
#         str_dict[attr_name] = model_field
#     return str_dict

def retrieve_pydantic(model_cls: type[BaseModel]) -> Dict[str, FieldInfo]:
    """
    Given a Pydantic model class, returns a dictionary mapping attribute names
    to their Pydantic FieldInfo (includes type, description, default, etc.).

    Args:
        model_cls (Type[BaseModel]): The Pydantic model class (not an instance).

    Returns:
        Dict[str, FieldInfo]: Mapping from attribute name to field metadata.
    """
    str_dict = {}
    for attr_name, model_field in model_cls.model_fields.items():
        str_dict[attr_name] = model_field
    return str_dict

def pydantic2tag(item: dict) -> str:
    final_str = "\n###Answer Format:\n"
    for key, _ in item.items():
        final_str += f"<{key}></{key}>\n"
    return final_str

def pydantic2prompt(item: dict) -> str:
    final_str = prompt_pydantic
    final_str += "\n###Field details:"
    for key, value in item.items():
        final_str += f"\nField name: {key}"
        final_str += f"\nField description: {value}"
        final_str += "\n"
    final_str += pydantic2tag(item)
    return final_str

def parse_tagged_string_to_pydantic(s: str, model_cls: Type[BaseModel]) -> BaseModel:
    """
    Parse a tagged string and return a Pydantic object of the given class.

    Args:
        s (str): The string with fields wrapped in tags, e.g. <field>value</field>
        model_cls (Type[BaseModel]): The Pydantic model class

    Returns:
        BaseModel: An instance of the model class populated with values from the string.
    """
    field_values = {}
    for field in model_cls.model_fields.keys():
        # Regex to find content between <field> and </field>
        pattern = rf"<{field}>(.*?)</{field}>"
        match = re.search(pattern, s, re.DOTALL)
        if match:
            value = match.group(1).strip()
            field_values[field] = value
        else:
            raise ValueError(f"Field '{field}' not found in the input string.")

    return model_cls(**field_values)



if __name__ == "__main__":
    class SectionInput(BaseModel):
        task: str = Field(description="Question that needs to be answered")
        solution: str = Field(description="The default answer")

    section = SectionInput(task="foo", solution="bar")

    temp_dict = retrieve_pydantic(section)
    temp_str = pydantic2prompt(temp_dict)
    print(temp_str)