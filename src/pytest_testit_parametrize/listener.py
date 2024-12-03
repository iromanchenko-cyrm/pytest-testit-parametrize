import pytest
from testit_python_commons.services import AdapterManager

from pytest_testit_parametrize.logger import Logger
from pytest_testit_parametrize.services import ParameterManager

logger = Logger("listener").get_logger()


class TmsListener:
    __pytest_info = None

    def __init__(
        self, adapter_manager: AdapterManager, parameter_manager: ParameterManager
    ):
        self.__adapter_manager = adapter_manager
        self.parameter_manager = parameter_manager

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, config, items):
        if config.option.flush_params:
            logger.info("Flushing testit parameters...")
            for item in items.copy():
                if hasattr(item, "callspec"):  # if parameterized
                    self.parameter_manager.flush_params(item)

        if config.option.set_params:
            logger.info("Setting testit parameters...")
            for item in items.copy():
                if hasattr(item, "callspec"):
                    self.parameter_manager.enrich_workitem_by_params(item)

        logger.info("Finished! \nEmptying suite...")
        items.clear()
