from enum import IntEnum
from dataclasses import dataclass
import logging
import sys


def config_logger(name="llmbench", *, level = logging.DEBUG):
    if sys.stderr.isatty():
        format_spec = "%(asctime)s %(levelname)s [%(module)s.py:%(lineno)d in %(funcName)s()]: %(message)s"
    else:
        format_spec = "%(levelname)s [%(module)s.py:%(lineno)d in %(funcName)s()]: %(message)s"
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR, format=format_spec)
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(sys.stderr)
    logger_handler.setFormatter(logging.Formatter(format_spec))
    logger_handler.setLevel(level)
    logger.addHandler(logger_handler)
    logger.propagate = False
    logger.setLevel(level)
    return logger


@dataclass(kw_only=True, frozen=True)
class BenchConfig:
    engine_list: list[str]
    engine_os: str
    engine_arch: str
    llama_cpp_version: str
    working_dir: str
    cleanup: bool


class ModelSize(IntEnum):
    TINY = 1
    SMALL = 2


@dataclass(kw_only=True, frozen=True)
class ModelDescription:
    size: ModelSize
    name: str
    url: str

