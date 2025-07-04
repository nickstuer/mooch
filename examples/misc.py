import logging
from typing import NoReturn

from mooch.decorators import log_entry_exit, retry, silent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@log_entry_exit
@silent(fallback="nick")
@retry(times=2, delay=1)
def get_name() -> NoReturn:
    logger.info("function raises an error but returns fallback value'")
    raise RuntimeError("fail")


print(get_name())  # Should print "nick""
