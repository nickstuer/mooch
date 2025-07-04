import logging
from typing import NoReturn

from mooch.decorators import log_entry_exit, silent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("misc")


@log_entry_exit
@silent(fallback="fallback_value")
def raise_error() -> NoReturn:
    logger.info("function raises an error but returns 'fallback_value'")
    raise RuntimeError("fail")


print(raise_error())  # Should print "fallback_value"
