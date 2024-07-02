from functools import wraps

from django.forms.boundfield import BoundField
from django.template import Library, TemplateSyntaxError

register = Library()


NUMERIC_KEYS = frozenset(["min", "max", "step", "size", "minlength", "maxlength", "cols", "rows"])
INTEGER_KEYS = frozenset(["size", "minlength", "maxlength", "cols", "rows"])


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
                f"The '{func.__name__}' filter can only be applied to form fields (BoundField instances)."
            )
        return func(value, *args, **kwargs)
    return wrapper


@register.filter(name="set_attr")
@boundfield_required
def set_attr(value: BoundField, attributes_string: str) -> BoundField:
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

    3. To set a boolean attribute:
       {{ form.email|set_attr:"required" }}

    4. To set numeric attributes:
       {{ form.age|set_attr:"min=18,max=100" }}

    5. To use commas within attribute values:
       {{ form.email|set_attr:"placeholder=Email Address\, Username" }}

    Parameters:
    - value (BoundField): The form field instance to modify.
    - attributes_string (str): A string specifying the attribute(s) to set or update. 
                                Attributes are provided in key=value format, comma-separated for multiple attributes. 
                                If no value is provided (e.g., 'required'), the attribute is set with an empty string value. 
                                Use '\,' to include a literal comma in an attribute value.

    Returns:
    BoundField: The form field with the added or updated HTML attributes.

    Raises:
    TypeError: If the input is not a BoundField instance.
    TemplateSyntaxError: If the attribute format is invalid or cannot be parsed correctly.
    """
    def split_attributes(s):
        parts = []
        current = []
        escape_char = "\\"
        delimiter = ","

        i = 0
        while i < len(s):
            char = s[i]
            if char == delimiter and (not current or current[-1] != escape_char):
                parts.append("".join(current))
                current.clear()
            elif char == escape_char and i + 1 < len(s) and s[i + 1] == delimiter:
                current.append(delimiter)
                i += 1
            else:
                current.append(char)
            i += 1

        if current:
            parts.append("".join(current))

        return parts

    attrs = value.field.widget.attrs

    for attribute in split_attributes(attributes_string):
        attribute = attribute.strip()
        if "=" in attribute:
            key, val = attribute.split("=", 1)
            key = key.strip()
            val = val.strip()

            # Handle numeric attributes
            if key in NUMERIC_KEYS:
                try:
                    attrs[key] = int(val) if key in INTEGER_KEYS else float(val)
                except ValueError:
                    expected_type = "integer" if key in INTEGER_KEYS else "floating-point"
                    raise TemplateSyntaxError(
                        f"The value '{val}' for '{key}' attribute must be a valid {expected_type}."
                    )
            else:
                attrs[key] = val
        else:
            # Set attribute with an empty string value if no value is provided
            attrs[attribute] = ""

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
    if current_classes:
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
    - class_names (str): A string of CSS class names to remove from the 'class' attribute, 
                        separated by commas and/or spaces.

    Returns:
    BoundField: The form field with the specified classes removed from the 'class' attribute.

    Raises:
    TypeError: If the input is not a BoundField instance.
    """
    attrs = value.field.widget.attrs
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
    elif "class" in attrs:
        del attrs["class"]

    return value
