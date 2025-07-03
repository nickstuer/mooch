from typing import NoReturn

from mooch.enhancers import log_entry_exit, silent


@log_entry_exit
@silent(fallback="fallback_value")
def raise_error() -> NoReturn:
    raise RuntimeError("fail")


print(raise_error())  # Should print "fallback_value"
