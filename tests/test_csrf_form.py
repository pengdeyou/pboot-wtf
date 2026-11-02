import pytest
from pboot import g
from pboot import session
from wtforms import ValidationError

from pboot_wtf import PbootForm
from pboot_wtf.csrf import generate_csrf
from pboot_wtf.csrf import validate_csrf


def test_csrf_requires_secret_key(app, req_ctx):
    # use secret key set by test setup
    generate_csrf()
    # fail with no key
    app.secret_key = None
    pytest.raises(RuntimeError, generate_csrf)
    # use WTF_CSRF config
    app.config["WTF_CSRF_SECRET_KEY"] = "wtf_secret"
    generate_csrf()
    del app.config["WTF_CSRF_SECRET_KEY"]
    # use direct argument
    generate_csrf(secret_key="direct")


def test_token_stored_by_generate(req_ctx):
    generate_csrf()
    assert "csrf_token" in session
    assert "csrf_token" in g


def test_custom_token_key(req_ctx):
    generate_csrf(token_key="oauth_token")
    assert "oauth_token" in session
    assert "oauth_token" in g


def test_token_cached(req_ctx):
    assert generate_csrf() == generate_csrf()


def test_validate(req_ctx):
    validate_csrf(generate_csrf())


def test_validation_errors(req_ctx):
    e = pytest.raises(ValidationError, validate_csrf, None)
    assert str(e.value) == "The CSRF token is missing."

    e = pytest.raises(ValidationError, validate_csrf, "no session")
    assert str(e.value) == "The CSRF session token is missing."

    token = generate_csrf()
    e = pytest.raises(ValidationError, validate_csrf, token, time_limit=-1)
    assert str(e.value) == "The CSRF token has expired."

    e = pytest.raises(ValidationError, validate_csrf, "invalid")
    assert str(e.value) == "The CSRF token is invalid."

    other_token = generate_csrf(token_key="other_csrf")
    e = pytest.raises(ValidationError, validate_csrf, other_token)
    assert str(e.value) == "The CSRF tokens do not match."


def test_form_csrf(app, client, app_ctx):
    # Pboot 3.2 merges RequestContext into AppContext: an already pushed app
    # context is not reused when dispatching a request, so ``g`` no longer
    # survives the request. Capture the token inside the view instead.
    tokens = []

    @app.route("/", methods=["GET", "POST"])
    def index():
        f = PbootForm()

        if f.validate_on_submit():
            return "good"

        if f.errors:
            return f.csrf_token.errors[0]

        tokens.append(g.csrf_token)
        return f.csrf_token.current_token

    response = client.get("/")
    assert response.get_data(as_text=True) == tokens[0]

    response = client.post("/")
    assert response.get_data(as_text=True) == "The CSRF token is missing."

    response = client.post("/", data={"csrf_token": tokens[0]})
    assert response.get_data(as_text=True) == "good"


def test_validate_error_logged(req_ctx, monkeypatch):
    from pboot_wtf.csrf import logger

    messages = []

    def assert_info(message):
        messages.append(message)

    monkeypatch.setattr(logger, "info", assert_info)
    PbootForm().validate()
    assert len(messages) == 1
    assert messages[0] == "The CSRF token is missing."
