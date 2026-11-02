from pboot import Pboot
from pboot import render_template
from wtforms import FieldList

from pboot_wtf import PbootForm
from pboot_wtf.file import FileField


class FileUploadForm(PbootForm):
    uploads = FieldList(FileField())


DEBUG = True
SECRET_KEY = "secret"

app = Pboot(__name__)
app.config.from_object(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    form = FileUploadForm()

    for _ in range(5):
        form.uploads.append_entry()

    filedata = []

    if form.validate_on_submit():
        for upload in form.uploads.entries:
            filedata.append(upload)

    return render_template("index.html", form=form, filedata=filedata)


if __name__ == "__main__":
    app.run()
