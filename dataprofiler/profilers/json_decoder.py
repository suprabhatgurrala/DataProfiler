"""Contains methods to decode components of a Profiler."""
from typing import TYPE_CHECKING, Dict, Optional, Type

if TYPE_CHECKING:
    from .base_column_profilers import BaseColumnProfiler
    from .profilers import column_profile_compilers as col_pro_compilers


# default, but set in the local __init__ to avoid circular imports
_profiles: Dict[str, Type["BaseColumnProfiler"]] = {}
_compilers: Dict[str, Type["col_pro_compilers.BaseCompiler"]] = {}


def get_column_profiler_class(class_name: str) -> Type["BaseColumnProfiler"]:
    """
    Use name of class to return default-constructed version of that class.

    Raises ValueError if class_name is not name of a subclass of
        BaseColumnProfiler.

    :param class_name: name of BaseColumnProfiler subclass retrieved by
        calling type(instance).__name__
    :type class_name: str representing name of class
    :return: subclass of BaseColumnProfiler object
    """
    profile_class: Optional[Type["BaseColumnProfiler"]] = _profiles.get(class_name)
    if profile_class is None:
        raise ValueError(f"Invalid profiler class {class_name} " f"failed to load.")
    return profile_class


def get_compiler_class(class_name: str) -> Type["col_pro_compilers.BaseCompiler"]:
    """
    Use name of class to return default-constructed version of that class.

    Raises ValueError if class_name is not name of a subclass of
        BaseCompiler.

    :param class_name: name of BaseCompiler subclass retrieved by
        calling type(instance).__name__
    :type class_name: str representing name of class
    :return: subclass of BaseCompiler object
    """
    compiler_class: Optional[Type["BaseColumnProfiler"]] = _compilers.get(class_name)
    if compiler_class is None:
        raise ValueError(f"Invalid compiler class {class_name} " f"failed to load.")
    return compiler_class


def load_column_profile(serialized_json: dict) -> "BaseColumnProfiler":
    """
    Construct subclass of BaseColumnProfiler given a serialized JSON.

    Expected format of serialized_json (see json_encoder):
        {
            "class": <str name of class that was serialized>
            "data": {
                <attr1>: <value1>
                <attr2>: <value2>
                ...
            }
        }

    :param serialized_json: JSON representation of column profiler that was
        # serialized using the custom encoder in profilers.json_encoder
    :type serialized_json: a dict that was created by calling json.loads on
        a JSON representation using the custom encoder
    :return: subclass of BaseColumnProfiler that has been deserialized from
        JSON

    """
    column_profiler_cls: Type["BaseColumnProfiler"] = get_column_profiler_class(
        serialized_json["class"]
    )
    return column_profiler_cls.load_from_dict(serialized_json["data"])


def load_compiler(serialized_json: dict) -> "col_pro_compilers.BaseCompiler":
    """
    Construct subclass of BaseCompiler given a serialized JSON.

    Expected format of serialized_json (see json_encoder):
        {
            "class": <str name of class that was serialized>
            "data": {
                <attr1>: <value1>
                <attr2>: <value2>
                ...
            }
        }

    :param serialized_json: JSON representation of column profiler that was
        serialized using the custom encoder in profilers.json_encoder
    :type serialized_json: a dict that was created by calling json.loads on
        a JSON representation using the custom encoder
    :return: subclass of BaseCompiler that has been deserialized from
        JSON

    """
    column_profiler_cls: Type["col_pro_compilers.BaseCompiler"] = get_compiler_class(
        serialized_json["class"]
    )
    return column_profiler_cls.load_from_dict(serialized_json["data"])
