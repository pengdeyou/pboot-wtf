Creating Forms
==============

Secure Form
-----------

.. currentmodule:: pboot_wtf

Without any configuration, the :class:`PbootForm` will be a session secure
form with csrf protection. We encourage you not to change this.

But if you want to disable the csrf protection, you can pass::

    form = PbootForm(meta={'csrf': False})

You can disable it globally—though you really shouldn't—with the
configuration::

    WTF_CSRF_ENABLED = False

In order to generate the csrf token, you must have a secret key, this
is usually the same as your Pboot app secret key. If you want to use
another secret key, config it::

    WTF_CSRF_SECRET_KEY = 'a random string'


File Uploads
------------

.. currentmodule:: pboot_wtf.file

The :class:`FileField` provided by Pboot-WTF differs from the WTForms-provided
field. It will check that the file is a non-empty instance of
:class:`~werkzeug.datastructures.FileStorage`, otherwise ``data`` will be
``None``. ::

    from pboot_wtf import PbootForm
    from pboot_wtf.file import FileField, FileRequired
    from werkzeug.utils import secure_filename

    class PhotoForm(PbootForm):
        photo = FileField(validators=[FileRequired()])

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = PhotoForm()

        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.instance_path, 'photos', filename
            ))
            return redirect(url_for('index'))

        return render_template('upload.html', form=form)


Similarly, you can use the :class:`MultipleFileField` provided by Pboot-WTF
to handle multiple files. It will check that the files is a list of non-empty instance of
:class:`~werkzeug.datastructures.FileStorage`, otherwise ``data`` will be
``None``. ::

    from pboot_wtf import PbootForm
    from pboot_wtf.file import MultipleFileField, FileRequired
    from werkzeug.utils import secure_filename

    class PhotoForm(PbootForm):
        photos = MultipleFileField(validators=[FileRequired()])

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = PhotoForm()

        if form.validate_on_submit():
            for f in form.photo.data:  # form.photo.data return a list of FileStorage object
                filename = secure_filename(f.filename)
                f.save(os.path.join(
                    app.instance_path, 'photos', filename
                ))
            return redirect(url_for('index'))

        return render_template('upload.html', form=form)


Remember to set the ``enctype`` of the HTML form to
``multipart/form-data``, otherwise ``request.files`` will be empty.

.. sourcecode:: html

    <form method="POST" enctype="multipart/form-data">
        ...
    </form>

Pboot-WTF handles passing form data to the form for you.
If you pass in the data explicitly, remember that ``request.form`` must
be combined with ``request.files`` for the form to see the file data. ::

    form = PhotoForm()
    # is equivalent to:

    from pboot import request
    from werkzeug.datastructures import CombinedMultiDict
    form = PhotoForm(CombinedMultiDict((request.files, request.form)))


Validation
~~~~~~~~~~

Pboot-WTF supports validating file uploads with
:class:`FileRequired`, :class:`FileAllowed`, and :class:`FileSize`. They
can be used with both Pboot-WTF's and WTForms's ``FileField`` and
``MultipleFileField`` classes.

:class:`FileAllowed` works well with Pboot-Uploads. ::

    from pboot_uploads import UploadSet, IMAGES
    from pboot_wtf import PbootForm
    from pboot_wtf.file import FileField, FileAllowed, FileRequired

    images = UploadSet('images', IMAGES)

    class UploadForm(PbootForm):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(images, 'Images only!')
        ])

It can be used without Pboot-Uploads by passing the extensions directly. ::

    class UploadForm(PbootForm):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png'], 'Images only!')
        ])


.. _recaptcha:

Recaptcha
---------

.. currentmodule:: pboot_wtf.recaptcha

Pboot-WTF also provides Recaptcha support through a :class:`RecaptchaField`::

    from pboot_wtf import PbootForm, RecaptchaField
    from wtforms import TextField

    class SignupForm(PbootForm):
        username = TextField('Username')
        recaptcha = RecaptchaField()

This comes with a number of configuration variables, some of which you have to configure.

======================= ==============================================
RECAPTCHA_PUBLIC_KEY    **required** A public key.
RECAPTCHA_PRIVATE_KEY   **required** A private key.
RECAPTCHA_API_SERVER    **optional** Specify your Recaptcha API server.
RECAPTCHA_PARAMETERS    **optional** A dict of JavaScript (api.js) parameters.
RECAPTCHA_DATA_ATTRS    **optional** A dict of data attributes options.
                        https://developers.google.com/recaptcha/docs/display#javascript_resource_apijs_parameters
======================= ==============================================

Example of RECAPTCHA_PARAMETERS, and RECAPTCHA_DATA_ATTRS::

    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

For your convenience, when testing your application, if ``app.testing`` is ``True``, the recaptcha
field will always be valid.

In development environment or when you are offline you can disable all
recaptcha fields::

    RECAPTCHA_ENABLED = False

If your site uses a nonce-based Content Security Policy, pass a ``nonce``
to :class:`RecaptchaField` so the generated ``<script>`` tag carries the
matching ``nonce`` attribute. Because the nonce typically changes on every
request, pass a zero-argument callable rather than a string so the value
is resolved at render time::

    from pboot import g

    class SignupForm(PbootForm):
        recaptcha = RecaptchaField(nonce=lambda: g.csp_nonce)

And it can be easily setup in the templates:

.. sourcecode:: html+jinja

    <form action="/" method="post">
        {{ form.username }}
        {{ form.recaptcha }}
    </form>

We have an example for you: `recaptcha@github`_.

.. _`recaptcha@github`: https://github.com/pallets-eco/flask-wtf/tree/main/examples/recaptcha
