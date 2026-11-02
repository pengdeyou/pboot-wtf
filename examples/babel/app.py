from pboot import Pboot
from pboot import render_template
from pboot import request
from pboot_babel import Babel
from pboot_babel import lazy_gettext as _
from wtforms import StringField
from wtforms.validators import DataRequired

from pboot_wtf import PbootForm


class BabelForm(PbootForm):
    name = StringField(_("Name"), validators=[DataRequired()])


DEBUG = True
SECRET_KEY = "secret"
WTF_I18N_ENABLED = True


def get_locale():
    """how to get the locale is defined by you.

    Match by the Accept Language header::

        match = app.config.get('BABEL_SUPPORTED_LOCALES', ['en', 'zh'])
        default = app.config.get('BABEL_DEFAULT_LOCALES', 'en')
        return request.accept_languages.best_match(match, default)
    """
    # this is a demo case, we use url to get locale
    code = request.args.get("lang", "en")
    return code


app = Pboot(__name__)
app.config.from_object(__name__)

# config babel
babel = Babel(app, locale_selector=get_locale)


@app.route("/", methods=("GET", "POST"))
def index():
    form = BabelForm()
    if form.validate_on_submit():
        pass
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run()
