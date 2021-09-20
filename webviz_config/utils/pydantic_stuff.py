import pydantic

# from pydantic.main import BaseModel
from pydantic.decorator import ValidatedFunction
from typing import Callable, Optional, Union, List, Type, Set
import copy
import inspect


def validate_params_for_single_func(
    func: Callable, param_names_to_ignore: Set[str], arg_dict: dict
) -> Optional[dict]:

    # Make copies since we may end up modifying them
    func = copy.deepcopy(func)
    param_names_to_ignore = copy.deepcopy(param_names_to_ignore)
    arg_dict = copy.deepcopy(arg_dict)

    func_signature = inspect.signature(func)

    for param_name in param_names_to_ignore:
        if param_name in func_signature.parameters:
            # Create a fake argument value of None in the arg dictionary
            arg_dict[param_name] = None

            # Must also remove any annotations (type-hints) for this param so
            # that the None value specified above will be accepted
            if param_name in func.__annotations__:
                del func.__annotations__[param_name]

    dummy_validate_func_decorator = ValidatedFunction(func, config=None)
    # vd = ValidatedFunction(func, config={"arbitrary_types_allowed": True})

    model_class: Type[pydantic.BaseModel] = dummy_validate_func_decorator.model

    try:
        model: pydantic.BaseModel = model_class(**arg_dict)
    except pydantic.ValidationError as e:
        print("Dumping error start ====================")
        print(e)
        print("input arg dict")
        print(arg_dict)
        print("Dumping error end ====================")
        return None

    # If we get to this point, pydantic has sucessfully both parsed/converted the input data
    # and validated it against the specified function.
    # Now we want to extract (in pydantic lingo: "export the model") the possibly converted
    # values from the pydantic model and return them as a dictionary
    # Build set containing keys/fields we don't want to include in the returned dict
    fields_to_exclude = param_names_to_ignore.union({"args", "kwargs"})
    output_arg_dict = model.dict(exclude=fields_to_exclude)
    return output_arg_dict


#    return {
#        key: value
#        for key, value in model.dict().items()
#        if key not in ["args", "kwargs"]
#    }


def schema_for_single_func(
    func: Callable,
    param_names_to_ignore: List[str],
) -> dict:
    # Make copies since we may end up modifying them
    func = copy.deepcopy(func)

    sig = inspect.signature(func)

    for param_name in param_names_to_ignore:
        if param_name in sig.parameters:
            # Remove any annotations (type-hints) for this param
            if param_name in func.__annotations__:
                # print(f"DELETING annotation: {param_name}")
                del func.__annotations__[param_name]

    # vd = ValidatedFunction(func, config= { "arbitrary_types_allowed": True })
    vd = ValidatedFunction(func, config=None)

    schema_dict = vd.model.schema()

    properties_dict = schema_dict["properties"]
    if isinstance(properties_dict, dict):
        if "args" in properties_dict:
            del properties_dict["args"]

        if "kwargs" in properties_dict:
            del properties_dict["kwargs"]

        for param_name in param_names_to_ignore:
            if param_name in properties_dict:
                del properties_dict[param_name]

    required_list = schema_dict["required"]
    if isinstance(required_list, list):
        for param_name in param_names_to_ignore:
            if param_name in required_list:
                required_list.remove(param_name)

    return schema_dict
