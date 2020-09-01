# (C) Copyright 2020

ERROR_UNKNOWN_VALIDATION_ERROR = "Failed validation: %(VALIDATOR)s, for element: %(PATH)s, Details: %(MESSAGE)s"

ERROR_MISSING_REQUIRED_ELEMENTS = "Missing required elements. The required elements for '%(OBJECT_LOCATION)s': '%(REQUIRED_VALUES)s'"

ERROR_INVALID_ELEMENTS = "%(ELEMENTS)s in %(PATH)s"

ERROR_INVALID_ELEMENTS_ONEOF = "%(PATH)s contains invalid element(s). '%(ELEMENTS)s'."

ERROR_REQUIRED_ONEOF_ELEMENTS = "'%(PATH)s' must have at most one of the element(s) [%(ELEMENTS)s]."

ERROR_INVALID_ELEMENTS_ANYOF = "'%(PATH)s' must have at least one of the element(s) [%(ELEMENTS)s]."

ERROR_NOT_ALLOWED_PROP = "%(ELEMENTS)s is not allowed for '%(PATH)s' with current parameters."

ERROR_NOT_ALLOWED_VALUE = "'%(PATH)s' should be one of '%(VALUES)s'."

ERROR_INVALID_VALUE_TYPE = "'%(PATH)s' value type should be '%(VALUES)s'."

ERROR_STRING_MIN_LENGTH = "Min length for element '%(PATH)s' is '%(VALUE)s' characters."

ERROR_STRING_MAX_LENGTH = "Max length for element '%(PATH)s' is '%(VALUE)s' characters."

ERROR_INTEGER_MIN_LENGTH = "Minimum value for numeric element '%(PATH)s' is '%(VALUE)s'."

ERROR_INTEGER_MAX_LENGTH = "Maximum value for numeric element '%(PATH)s' is '%(VALUE)s'."

ERROR_ARRAY_MAX_ITEMS = "Max items for array '%(PATH)s' is '%(VALUE)s'."

ERROR_ARRAY_MIN_ITEMS = "Min items for array '%(PATH)s' is '%(VALUE)s'."

ERROR_ARRAY_UNIQUE_ITMES = "Items in the array should be unique for element '%(PATH)s'."

ERROR_MIN_ONE_PROP = "At least one property required for element '%(PATH)s'."

ERROR_PATTERN_MESSAGE = "Element '%(PATH)s' does not have the correct format. %(MSG)s"

ERROR_QUERY_PARAMS_REASON = "Query parameters are not supported for '%(METHOD)s' method"

ERROR_QUERY_PARAMS_MESSAGE = "Unsupported query"

ERROR_DUPLICATE_KEYS_REASON = "Duplicate property: %(PROPERTY)s"

ERROR_INVALID_INPUT_MESSAGE = "Unable to process request. Invalid input parameter."