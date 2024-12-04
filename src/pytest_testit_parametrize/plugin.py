import pytest

from pytest_testit_parametrize.listener import TmsListener
from pytest_testit_parametrize.services import TmsPluginManager


def pytest_addoption(parser):
    group = parser.getgroup("testit-parametrize")
    group.addoption(
        "--testit-params-flush",
        action="store_true",
        dest="flush_params",
        help="Flush parameters for related testcases from Test IT",
    )
    group.addoption(
        "--testit-params-init",
        action="store_true",
        dest="set_params",
        help="Upload parameters from autotests into Test IT",
    )


@pytest.mark.tryfirst
def pytest_cmdline_main(config):
    if config.option.flush_params or config.option.set_params:
        config.option.set_adapter_mode = "2"
        listener = TmsListener(
            TmsPluginManager.get_adapter_manager(config.option),
            TmsPluginManager.get_parameter_manager(config.option),
        )

        config.pluginmanager.register(listener)
        TmsPluginManager.get_plugin_manager().register(listener)
