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


@register.filter(name="set_attr")
@boundfield_required
def set_attr(value: BoundField, arg: str) -> BoundField:
    """
    Adds or updates HTML attributes for a Django form field widget dynamically.

    This template filter enhances Django forms by allowing the addition or modification
    of HTML attributes such as CSS classes, placeholder text, etc., while preserving
    existing attributes. It supports setting multiple attributes in a single call.

    Usage:
    1. To set a single attribute:
    {{ form.email|set_attr:"placeholder=Email Address" }}

    2. To set multiple attributes:
    {{ form.email|set_attr:"class=form-control,placeholder=Email Address" }}

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
                f"Invalid format for set_attr filter: '{attribute}'. "
                "Use 'key=value' format."
            )

    return value


@register.filter(name="clear_attr")
@boundfield_required
def clear_attr(value: BoundField, attr_names: str) -> BoundField:
    """
    Removes specified HTML attributes from a Django form field widget.

    This template filter allows you to dynamically remove one or more HTML attributes
    (e.g., 'class', 'placeholder') from a Django form field widget. Multiple attributes
    can be removed simultaneously by providing a comma-separated list of attribute names.

    Usage:
    1. To remove a single attribute:
       {{ form.email|clear_attr:"class" }}

    2. To remove multiple attributes:
       {{ form.email|clear_attr:"class,placeholder" }}

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

        # Check if the attribute exists and remove it
        if attr_name in attrs:
            del attrs[attr_name]

    return value


@register.filter(name="append_class")
@boundfield_required
def append_class(value: BoundField, new_classes: str) -> BoundField:
    """
    Appends CSS classes to the 'class' attribute of a Django form field widget.

    This filter adds additional CSS classes to the existing 'class' attribute of a Django form field,
    preserving already present classes.

    Usage:
    1. To append classes separated by commas:
       {{ form.email|append_class:"new-class1,new-class2" }}

    2. To append classes separated by spaces:
       {{ form.email|append_class:"new-class1 new-class2" }}

    3. To append classes separated by both commas and spaces:
       {{ form.email|append_class:"new-class1,new-class2 new-class3" }}

    Parameters:
    - value (BoundField): The form field instance to modify.
    - new_classes (str): A string of CSS classes to append, separated by commas and/or spaces.

    Returns:
    BoundField: The form field with the appended CSS classes.

    Raises:
    TypeError: If the input is not a BoundField instance.
    """
    attrs = value.field.widget.attrs
    current_classes = set(attrs.get("class", "").split())

    # Split new classes based on commas and spaces, then add them if not already present
    for class_set in new_classes.split(","):
        for class_name in class_set.split():
            stripped_class_name = class_name.strip()
            if stripped_class_name:
                current_classes.add(stripped_class_name)

    # Update the 'class' attribute with the modified list
    attrs["class"] = " ".join(current_classes)

    return value


@register.filter(name="remove_class")
@boundfield_required
def remove_class(value: BoundField, class_names: str) -> BoundField:
    """
    Removes specified CSS classes from the 'class' attribute of a Django form field widget.

    This filter allows you to dynamically remove one or more CSS classes from the 'class'
    attribute of a Django form field widget. Multiple classes can be removed simultaneously
    by providing a string of class names separated by commas and/or spaces.

    Usage:
    1. To remove classes separated by commas:
       {{ form.email|remove_class:"old-class1,old-class2" }}

    2. To remove classes separated by spaces:
       {{ form.email|remove_class:"old-class1 old-class2" }}

    3. To remove classes separated by both commas and spaces:
       {{ form.email|remove_class:"old-class1,old-class2 old-class3" }}

    Parameters:
    - value (BoundField): The form field instance from which classes will be removed.
    - class_names (str): A string of CSS class names to remove from the 'class' attribute, separated by commas and/or spaces.

    Returns:
    BoundField: The form field with the specified classes removed from the 'class' attribute.

    Raises:
    TypeError: If the input is not a BoundField instance.
    """
    attrs = value.field.widget.attrs

    # Get current classes as a set
    current_classes = set(attrs.get("class", "").split())

    # Split class names based on commas and spaces, then remove them if present
    for class_set in class_names.split(","):
        for class_name in class_set.split():
            stripped_class_name = class_name.strip()
            if stripped_class_name in current_classes:
                current_classes.remove(stripped_class_name)

    # Update the 'class' attribute with the modified list or remove it if empty
    if current_classes:
        attrs["class"] = " ".join(current_classes)
    else:
        del attrs["class"]

    return value
