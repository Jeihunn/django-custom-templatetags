from functools import wraps

from django.forms.boundfield import BoundField
from django.template import Library, TemplateSyntaxError

register = Library()


def boundfield_required(func):
    """
    Decorator to ensure that the provided value is a BoundField instance."

    This decorator is used to validate that the input to a template filter
    is a BoundField instance, raising a TypeError if it is not.

    Usage:
    @boundfield_required
    def your_filter(value, arg):
        ...
    """
    @wraps(func)
    def wrapper(value, *args, **kwargs):
        if not isinstance(value, BoundField):
            raise TypeError(
                f"The '{
                    func.__name__}' filter can only be applied to form fields (BoundField instances)."
            )
        return func(value, *args, **kwargs)
    return wrapper


@register.filter(name="set_field_attr")
@boundfield_required
def set_field_attr(value: BoundField, arg: str) -> BoundField:
    """
    Adds or updates HTML attributes for a Django form field widget dynamically.

    This template filter enhances Django forms by allowing the addition or modification
    of HTML attributes such as CSS classes, placeholder text, etc., while preserving
    existing attributes. It supports setting multiple attributes in a single call.

    Usage:
    1. To set a single attribute:
    {{ form.email|set_field_attr:"placeholder=Email Address" }}

    2. To set multiple attributes:
    {{ form.email|set_field_attr:"class=form-control,placeholder=Email Address" }}

    Parameters:
    - value (BoundField): The form field instance to modify.
    - arg (str): The attribute(s) to set or update in key=value format, comma-separated for multiple attributes.

    Returns:
    BoundField: The form field with the added or updated HTML attributes.

    Raises:
    TypeError: If the input is not a BoundField instance.
    TemplateSyntaxError: If the attribute format is invalid or cannot be parsed correctly.
    """
    attrs = value.field.widget.attrs

    for attribute in arg.split(","):
        try:
            key, val = attribute.split("=", 1)
            key = key.strip()
            val = val.strip()

            # Validate numeric attributes
            numeric_keys = ["min", "max", "step",
                            "size", "minlength", "maxlength", "cols", "rows"]
            if key in numeric_keys:
                try:
                    if key in ["size", "minlength", "maxlength", "cols", "rows"]:
                        attrs[key] = int(val)
                    else:
                        attrs[key] = float(val)
                except ValueError:
                    if key in ["size", "minlength", "maxlength", "cols", "rows"]:
                        expected_type = "integer"
                    else:
                        expected_type = "floating-point"

                    raise TemplateSyntaxError(
                        f"The value '{val}' for '{
                            key}' attribute must be a valid {expected_type}."
                    )

            # Default handling for other attributes (including 'class')
            else:
                attrs[key] = val

        except ValueError:
            raise TemplateSyntaxError(
                f"Invalid format for set_field_attr filter: '{attribute}'. "
                "Use 'key=value' format."
            )

    return value


@register.filter(name="remove_field_attr")
@boundfield_required
def remove_field_attr(value: BoundField, attr_names: str) -> BoundField:
    """
    Removes specified HTML attributes from a Django form field widget.

    This template filter allows you to dynamically remove one or more HTML attributes
    (e.g., 'class', 'placeholder') from a Django form field widget. It supports removing
    multiple attributes in a single call by providing a comma-separated list of attribute names.

    Usage:
    1. To remove a single attribute:
       {{ form.email|remove_field_attr:"class" }}

    2. To remove multiple attributes:
       {{ form.email|remove_field_attr:"class,placeholder" }}

    Parameters:
    - value (BoundField): The form field instance from which attributes will be removed.
    - attr_names (str): A comma-separated string of attribute names to remove.

    Returns:
    BoundField: The form field with the specified attributes removed.

    Raises:
    TypeError: If the input is not a BoundField instance.
    """
    attrs = value.field.widget.attrs
    for attr_name in attr_names.split(","):
        attr_name = attr_name.strip()
        if attr_name in attrs:
            del attrs[attr_name]

    return value


@register.filter(name="append_field_class")
@boundfield_required
def append_field_class(value: BoundField, new_class: str) -> BoundField:
    """
    Appends a CSS class to the 'class' attribute of a Django form field widget.

    This filter is used to add additional CSS classes to the 'class' attribute of a Django form field,
    preserving existing classes.

    Usage:
    {{ form.email|append_field_class:"new-class-name" }}

    Parameters:
    value: The form field (BoundField)
    new_class: The CSS class to append

    Returns:
    The form field with the appended CSS class

    Raises:
    TypeError: If the input is not a BoundField
    """
    attrs = value.field.widget.attrs
    current_classes = attrs.get("class", "").split()

    # Add the new class if it's not already present
    if new_class not in current_classes:
        current_classes.append(new_class)
        attrs["class"] = " ".join(current_classes)

    return value
