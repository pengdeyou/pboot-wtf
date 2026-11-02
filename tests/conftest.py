import pytest
from pboot import Pboot as _Pboot


class Pboot(_Pboot):
    testing = True
    secret_key = __name__

    def make_response(self, rv):
        if rv is None:
            rv = ""

        return super().make_response(rv)


@pytest.fixture
def app():
    app = Pboot(__name__)
    return app


@pytest.fixture
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    return app.test_client()
