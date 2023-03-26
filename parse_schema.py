from dataclasses import dataclass
import json

from enum import Enum
from pprint import pprint
from typing import Dict, List, Optional

class FieldType(Enum):
    VALUE = "value"
    UNSTRUCTURED = "unstructured"   # json string
    OBJECT = "object"
    LIST = "list"

@dataclass
class Schema:
    field_type: FieldType
    fields: Optional[Union[Dict[str, "Schema"], "Schemagit ad"]] = None
        
    def __str__(self):
        string = f"type: {self.field_type.value}\n"  
        if self.fields:
            print(type(self.fields))
            for name, field in self.fields.items():
                string += f"\t{name}\n\t{field}"
        return string
                
"""
    {
        "match_id" : {
            "type": value
        }
        "metadata" : {
            "type": "dict",
            "fields": {
                ...
            }
        }
    }

"""

def parse_schema(json_object):
    """Inferschema so that we can use that to create a database and retrieve one from it
        TODO: check if objects in a list have same schema, if not we can treat it as string literals
    """
    def dfs(node) -> Schema:
        
        def parse_list(items):
            schemas = [
                dfs(item)
                for item in items
            ]
            return schemas[0]
        
        if isinstance(node, Dict):
            return Schema(
                field_type=FieldType.OBJECT,
                fields={
                    k: dfs(v)
                    for k, v in node.items()
                }
            )
        #  TODO: check if objects in a list have same schema, if not we can treat it as string literals
        elif isinstance(node, List):
            return Schema(
                field_type=FieldType.LIST,
                fields=parse_list(node)
            )
        else:
            return Schema(
                field_type=FieldType.VALUE
            )
    return dfs(json_object)
        
        


        
def to_csv(json_object, schema):
    pass

def from_csv():
    pass

if __name__ == "__main__":
    with open("example.json") as f:
        json_object = json.load(f)
    print(len(json_object))
    print(parse_schema(json_object))