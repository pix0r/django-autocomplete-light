Integration with forms
======================

The purpose of this documentation is to describe every element in a
chronological manner. Because you want to know everything about this app and
hack like crazy.

It is complementary with the quick documentation.

Django startup
--------------

.. _registry-reference:

Registry
~~~~~~~~

.. automodule:: autocomplete_light.registry
   :members:

.. _channel-reference:

Channels basics
~~~~~~~~~~~~~~~

Example
>>>>>>>

:ref:`django-cities-light<citieslight:basic-channel>` ships the working example.

API
>>>

.. automodule:: autocomplete_light.channel.base
   :members:

Forms
~~~~~

Example
>>>>>>>

A simple example from test_project:

.. literalinclude:: ../../test_project/project_specific/forms.py
   :language: python

API
>>>

.. automodule:: autocomplete_light.forms
   :members:

Page rendering
~~~~~~~~~~~~~~

It is important to load jQuery first, and then autocomplete_light and
application specific javascript, it can look like this::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

However, ``autocomplete_light/static.html`` also includes "remote.js" which is
required only by remote channels. If you don't need it, you could either load
the static dependencies directly in your template, or override
``autocomplete_light/static.html``:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/static.html
   :language: django

Or, if you only want to make a global navigation autocomplete, you only need::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}autocomplete_light/autocomplete.js" type="text/javascript"></script>

.. include:: _admin_template.rst

.. _widget:

Widget in action
----------------

Widget definition
~~~~~~~~~~~~~~~~~

The first thing that happens is the definition of an AutocompleteWidget in a
form.

.. automodule:: autocomplete_light.widgets
   :members:

Widget rendering
~~~~~~~~~~~~~~~~

This is what the default widget template looks like:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/widget.html
   :language: django

Javascript initialization
-------------------------

deck.js initializes all widgets that have bootstrap='normal' (the default), as you can see::

    $('.autocomplete_light_widget[data-bootstrap=normal]').each(function() {
        $(this).yourlabs_deck();
    });

If you want to initialize the deck yourself, set the widget or channel
bootstrap to something else, say 'yourinit'. Then, add to
`yourapp/static/yourapp/autocomplete_light.js` something like::

    $('.autocomplete_light_widget[data-bootstrap=yourinit]').each(function() {
        $(this).yourlabs_deck({
            getValue: function(result) {
                // your own logic to get the value from an html result
                return ...;
            }
        });
    });

`yourapp/static/yourapp/autocomplete_light.js` will be automatically collected by
by autodiscover, and the script tag generated by
`{% autocomplete_light_static %}`.

In `django-cities-light source
<http://yourlabs.github.com/django-cities-light/>`_, you can see a `more interresting example
<https://github.com/yourlabs/django-cities-light/blob/master/cities_light/static/cities_light/autocomplete_light.js>`_
where two autocompletes depend on each other.

You should take a look at the code of `autocomplete.js
<https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/static/autocomplete_light/autocomplete.js>`_
and `deck.js
<https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/static/autocomplete_light/deck.js>`_,
as it lets you override everything.

One interresting note is that the plugins (yourlabs_autocomplete and
yourlabs_deck) hold a registry. Which means that:

- calling someElement.yourlabs_deck() will instanciate a deck with the passed
  overrides
- calling someElement.yourlabs_deck() again will return the deck instance for
  someElement

Javascript cron
~~~~~~~~~~~~~~~

deck.js includes a javascript function that is executed every two seconds. It
checks each widget's hidden select for a value that is not in the deck, and
adds it to the deck if any.

This is useful for example, when an item was added to the hidden select via the
'+' button in django admin. But if you create items yourself in javascript and
add them to the select it would work too.

.. _channel-view:

Javascript events
~~~~~~~~~~~~~~~~~

When the autocomplete input is focused, autocomplete.js checks if there are
enought caracters in the input to display an autocomplete box. If minCharacters
is 0, then it would open even if the input is empty, like a normal select box.

If the autocomplete box is empty, it will fetch the channel view. The channel
view will delegate the rendering of the autocomplete box to the actual channel.
So that you can override anything you want directly in the channel.

.. autoclass:: autocomplete_light.views.ChannelView
   :members:

.. automethod:: autocomplete_light.channel.base.ChannelBase.render_autocomplete
   :noindex:

.. automethod:: autocomplete_light.channel.base.ChannelBase.result_as_html
   :noindex:

Then, autocomplete.js recognizes options with a selector. By default, it is
'.result'. This means that any element with the '.result' class in the
autocomplete box is considered as an option.

When an option is selected, deck.js calls it's method getValue() and adds this
value to the hidden select. Also, it will copy the result html to the deck.

When an option is removed from the deck, deck.js also removes it from the
hidden select.

.. _templates:

This is the default HTML template for the autocomplete:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/autocomplete.html
   :language: django

This is the default HTML template for results:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/result.html
   :language: django
