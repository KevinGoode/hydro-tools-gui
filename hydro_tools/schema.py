# (C) Copyright 2020 
BOUNDARY_CONDITION = {"type": "object",
                      "additionalProperties": False,
                      "required": ["type", "rate", "final"], 
                      "properties": {
                            "type": {
                                "type": "integer",
                                "enum": [1, 2] # 1 is Flow 2 is depth
                            },
                            "rate": {
                                "type": "number",
                            },
                            "final": {
                                "type": "number", # Only needed if flow type. ignored otheriwise
                            }
                      }}

OCUSF_POST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["config"],
    "additionalProperties": False,
    "properties": {
        "config": {
            "type": "object",
            "additionalProperties": False,
            "required": ["shape", "width", "length", "angle", "manning", "slope", "qinit", "upstream", "downstream","reaches","iterations"],
            "properties": {
                "shape": {
                    "type": "integer",
                    "enum": [1, 2, 3]  # 1 CIRCULAR 2 RECTANGULAR 3 TRAPEZOIDAL
                },
                "width": {
                    "type": "number",
                    "minimum": 0.5
                },
                "length": {
                    "type": "number",
                    "minimum": 1.0
                },
                "angle": {
                    "type": "number",
                    "minimum": 1.0,
                    "maximum": 80.00,
                },
                "manning": {
                    "type": "number",
                    "maximum": 0.5,
                    "minimum": 0.005
                },
                "slope": {
                    "type": "number",
                    "maximum": 0.5,
                    "minimum": 0.00001
                },
                "qinit": {
                    "type": "number",
                    "maximum": 10000.0,
                    "minimum": -10000.0
                },
                "upstream": BOUNDARY_CONDITION,
                "downstream": BOUNDARY_CONDITION,
                "reaches": {
                    "type": "integer",
                    "maximum": 1000,
                    "minimum": 10,
                    "multipleOf" : 10
                    #"pattern": r"^[0-9]*0$",
                    #"error_message": "Number of reaches must be multiple of 10."
                },
                "iterations": {
                    "type": "integer",
                    "maximum": 10000,
                    "minimum": 1
                }
            }
        }
    }
}
