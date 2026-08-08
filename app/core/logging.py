import logging


def setup_logging(level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
