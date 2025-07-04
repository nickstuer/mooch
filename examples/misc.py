import logging
from typing import NoReturn

from mooch.decorators import log_entry_exit, retry, silent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@log_entry_exit
@silent(fallback="fallback_value")
@retry(times=2, delay=1)
def raise_error() -> NoReturn:
    logger.info("function raises an error but returns 'fallback_value'")
    raise RuntimeError("fail")


print(raise_error())  # Should print "fallback_value"
