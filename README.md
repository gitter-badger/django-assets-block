## What is `assetsblock`

`Assetsblock` is a django app that provides an `assets` template tag
and enables you to write more encapsulated templates that define their
javascript and css dependencies. Those dependencies will always render at the correct place.

The `assets` is an extension on the `block` tag but adding content to it works in every way:

 - extending template
 - including template
 - using inclusion tag

This is possible via the `django-output-context`

## Usage & Limitations

*layout.html*
```
<html>
  <head></head>
  <body>

    {% include widget_a.html %}
    {% assets footerjs %}
        <script src="{% static 'js/jquery.js' %}"></script>
    {% endassets%}
  </body>
</html>
```

*home.html*
```
{% extends 'layout.html' %}
{% assets footerjs %}
    <script src="{% static 'js/myscript.js' %}"></script>
{% endassets %}
{% include widget_b.html %}
```

*widget_a.html*
```
{% extends 'widget_b.html' %}
{% assets footerjs %}
    <script src="{% static 'js/widget_a.js' %}"></script>
{% endassets %}
{% include widget.html %}
```

*widget_b.html*
```
{% extends 'widget_b.html' %}
{% assets footerjs %}
    <script src="{% static 'js/widget_b.js' %}"></script>
{% endassets %}
{% include widget.html %}
```

### Output
```
<html>
  <head></head>
  <body>
    <script src="{% static 'js/jquery.js' %}"></script>
    <script src="{% static 'js/widget_a.js' %}"></script>
    <script src="{% static 'js/myscript.js' %}"></script>
    <script src="{% static 'js/widget_b.js' %}"></script>
  </body>
</html>

```

## What `assetsblock` doesn't do
It doesn't clean duplicate scripts, however the easiest solution would be to use a `uniquelines` filter when outputing 