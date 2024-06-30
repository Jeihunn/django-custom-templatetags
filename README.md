# Django Custom Template Tags

Custom Template Tags is a collection of Django template filters designed to enhance form field customization by dynamically adding, removing, and modifying HTML attributes and CSS classes. These template tags provide advanced attribute manipulation capabilities for form fields, making it easier to create dynamic and responsive forms in your Django applications.

## ✨ Features

- **Dynamic Attribute Manipulation**: Add, update, or remove HTML attributes for form field widgets on the fly.
- **CSS Class Management**: Easily append or remove CSS classes from form fields.
- **Flexible Syntax**: Support for various input formats, including comma-separated and space-separated values.
- **Type-Safe Operations**: Ensures that operations are performed only on valid Django form fields (BoundField instances).
- **Numeric Attribute Handling**: Special handling for numeric attributes to ensure proper data types.

By integrating these custom template tags and filters, you can significantly improve the flexibility and maintainability of your Django templates, especially when working with forms.

## 🛠️ Usage

1. **Add the custom template tags to your project**:

   Create a new file in your Django app, for example, `your_app/templatetags/field_attrs.py`:

   ```python
   from django import template
   from django.forms.boundfield import BoundField
   from django.template import TemplateSyntaxError

   register = template.Library()

   # Paste the custom filter functions here
   ```

2. **Load the custom template tags in your template**:

   At the top of your Django template, add:

   ```django
   {% load field_attrs %}
   ```

3. **Use the custom filters in your templates**:

   ```django
   {{ form.email|set_attr:"placeholder=Email Address,class=form-control,readonly" }}
   {{ form.name|clear_attr:"disabled" }}
   {{ form.password|append_class:"strong-password" }}
   {{ form.username|remove_class:"optional-field" }}
   ```

## 🔧 Available Filters

### set_attr

Adds or updates HTML attributes for a form field widget.

```django
{{ form.field|set_attr:"attribute1=value1,attribute2=value2" }}
```

### clear_attr

Removes specified HTML attributes from a form field widget.

```django
{{ form.field|clear_attr:"attribute1,attribute2" }}
```

### append_class

Appends CSS classes to the 'class' attribute of a form field widget.

```django
{{ form.field|append_class:"class1 class2,class3" }}
```

### remove_class

Removes specified CSS classes from the 'class' attribute of a form field widget.

```django
{{ form.field|remove_class:"class1,class2 class3" }}
```

## 💡 Examples

```django
{# Adding a placeholder and class #}
{{ form.email|set_attr:"placeholder=Enter your email,class=form-control" }}

{# Removing the class attribute #}
{{ form.firstname|clear_attr:"class" }}

{# Adding multiple classes #}
{{ form.password|append_class:"form-control,strong-password" }}

{# Removing specific classes #}
{{ form.username|remove_class:"optional,hidden" }}
```

## 🎥 Video Tutorial

For a detailed explanation of using these custom template tags and filters in your Django projects, check out my video tutorial:

[Custom Django Template Tags and Filters Tutorial](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

In this video, you'll learn:
- How to integrate these custom template tags into your Django projects.
- Advanced usage examples and best practices.
- Tips for creating your own custom template tags and filters.

## 📚 Medium Article

For an in-depth look at these custom template tags and filters, along with advanced usage scenarios, read my Medium article:

[Enhancing Django Templates with Custom Tags and Filters](https://medium.com/@your_username/your-article-link)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.