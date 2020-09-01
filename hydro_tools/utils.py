# (C) Copyright 2020
import jsonschema
import hydro_tools.errors as errors
def build_error_message(err_obj):
    def get_err_message(validator=''):
        if validator == 'required':
            return (
                errors.ERROR_MISSING_REQUIRED_ELEMENTS
                % {'OBJECT_LOCATION': '.'.join(
                    str(v) for v in err_obj.absolute_path),
                    'REQUIRED_VALUES': err_obj.validator_value}
            )

        elif validator == 'additionalProperties':
            return (
                errors.ERROR_INVALID_ELEMENTS
                % {
                    'ELEMENTS': err_obj.message,
                    'PATH': ".".join(map(str, err_obj.path))
                }
            )

        elif validator == 'oneOf':
            required_props = []
            validator_value = err_obj.validator_value
            if validator_value and isinstance(validator_value, list):
                for validator_val in validator_value:
                    if isinstance(validator_val, dict) and\
                            'required' in validator_val:
                        required_props.extend(validator_val['required'])

            if required_props:
                return (
                    errors.ERROR_REQUIRED_ONEOF_ELEMENTS
                    % {
                        'PATH': ".".join(map(str, err_obj.path)),
                        'ELEMENTS': ", ".join(required_props)
                    }
                )
            else:
                return (
                    errors.ERROR_INVALID_ELEMENTS_ONEOF
                    % {
                        'PATH': ".".join(map(str, err_obj.path)),
                        'ELEMENTS': ", ".join([
                            str(ctx.message) for ctx in err_obj.context])
                    }
                )

        elif validator == 'anyOf':
            required_props = []
            validator_value = err_obj.validator_value
            if validator_value and isinstance(validator_value, list):
                for validator_val in validator_value:
                    if isinstance(validator_val, dict) and \
                            'required' in validator_val:
                        required_props.append(validator_val['required'])
            if required_props:
                return (
                    errors.ERROR_INVALID_ELEMENTS_ANYOF
                    % {
                        'PATH': ".".join(map(str, err_obj.path)),
                        'ELEMENTS': ", ".join(
                            ["'" + ", ".join(req_props) + "'"
                             for req_props in required_props])
                    }
                )
            else:
                return (
                    errors.ERROR_INVALID_ELEMENTS_ANYOF
                    % {
                        'PATH': ".".join(map(str, err_obj.path)),
                        'ELEMENTS': ", ".join(["'" + ", ".join(
                            ctx.validator_value
                        ) + "'" for ctx in err_obj.context])
                    }
                )

        elif validator == 'not':
            return (
                errors.ERROR_NOT_ALLOWED_PROP
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'ELEMENTS': (
                        err_obj.validator_value['required']
                        if isinstance(err_obj.validator_value, dict) and
                        'required' in err_obj.validator_value
                        else err_obj.validator_value)
                }
            )

        elif validator == 'enum':
            return (
                errors.ERROR_NOT_ALLOWED_VALUE
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUES': err_obj.validator_value
                }
            )

        elif validator == 'type':
            return (
                errors.ERROR_INVALID_VALUE_TYPE
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUES': err_obj.validator_value
                }
            )

        elif validator == 'minLength':
            return (
                errors.ERROR_STRING_MIN_LENGTH
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('minLength', '')
                }
            )

        elif validator == 'maxLength':
            return (
                errors.ERROR_STRING_MAX_LENGTH
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('maxLength', '')
                }
            )

        elif validator == 'minimum':
            return (
                errors.ERROR_INTEGER_MIN_LENGTH
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('minimum', '')
                }
            )

        elif validator == 'maximum':
            return (
                errors.ERROR_INTEGER_MAX_LENGTH
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('maximum', '')
                }
            )

        elif validator == 'maxItems':
            return (
                errors.ERROR_ARRAY_MAX_ITEMS
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('maxItems', '')
                }
            )

        elif validator == 'minItems':
            return (
                errors.ERROR_ARRAY_MIN_ITEMS
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'VALUE': err_obj.schema.get('minItems', '')
                }
            )

        elif validator == 'uniqueItems':
            return (
                errors.ERROR_ARRAY_UNIQUE_ITMES
                % {'PATH': ".".join(map(str, err_obj.path))}
            )

        elif validator == 'minProperties':
            return (
                errors.ERROR_MIN_ONE_PROP
                % {'PATH': ".".join(map(str, err_obj.path))}
            )
        elif validator == 'pattern' and err_obj.schema.get("error_message"):
            # Default pattern validator message is not human readable.
            # To add custom message, add field 'error_message' next to
            # pattern field in schema. Make sure 'error_message' is localised
            # by using _ function imported from atlcom.i18n.
            return (
                errors.ERROR_PATTERN_MESSAGE
                % {
                    'PATH': ".".join(map(str, err_obj.path)),
                    'MSG': err_obj.schema['error_message']
                }
            )
        else:
            return (
                errors.ERROR_UNKNOWN_VALIDATION_ERROR
                % {
                    "VALIDATOR": err_obj.validator,
                    "PATH": ".".join(map(str, err_obj.path)),
                    "MESSAGE": err_obj.message
                }
            )
    try:
        error_message = get_err_message(err_obj.validator)
    except Exception:
        # Even if we fail to form a valid message we send back the original
        # message in exception body
        error_message = err_obj.message
    return error_message


def validate_json(json_data: dict, json_schema: dict):
    try:
        jsonschema.validate(instance=json_data, schema=json_schema)
    except (jsonschema.ValidationError, jsonschema.SchemaError) as e:
        return build_error_message(e)
    return None

