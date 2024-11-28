import pytest

from pytest_testit_parametrize.logger import Logger
from pytest_testit_parametrize.services import ParameterManager

logger = Logger("listener").get_logger()


class TmsListener:
    def __init__(self, parameters_manager: ParameterManager):
        self.__parameters_manager = parameters_manager

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, config, items):
        if config.option.flush_params:
            logger.info("Flushing testit parameters...")
            for item in items.copy():
                if hasattr(item, "callspec"):  # if parameterized
                    self.__parameters_manager.flush_params(item)

        if config.option.set_params:
            logger.info("Setting testit parameters...")
            for item in items.copy():
                if hasattr(item, "callspec"):
                    self.__parameters_manager.enrich_workitem_by_params(item)

        logger.info("Finished! \nEmptying suite...")
        items.clear()