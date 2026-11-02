import warnings


class PbootWTFDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter("always", PbootWTFDeprecationWarning)
warnings.filterwarnings(
    "ignore", category=PbootWTFDeprecationWarning, module="wtforms|pboot_wtf"
)
