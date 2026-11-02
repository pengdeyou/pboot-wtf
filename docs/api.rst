Developer Interface
===================

Forms and Fields
----------------

.. module:: pboot_wtf

.. autoclass:: PbootForm
    :members:

.. autoclass:: Form(...)

.. autoclass:: RecaptchaField

.. autoclass:: Recaptcha

.. autoclass:: RecaptchaWidget

.. module:: pboot_wtf.file

.. autoclass:: FileField

.. autoclass:: FileAllowed

.. autoclass:: FileRequired

CSRF Protection
---------------

.. module:: pboot_wtf.csrf

.. autoclass:: CSRFProtect
    :members:

.. autoclass:: CSRFError
    :members:

.. autofunction:: generate_csrf

.. autofunction:: validate_csrf

.. autofunction:: csrf_meta_tag
