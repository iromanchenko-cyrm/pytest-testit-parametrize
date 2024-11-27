from pluggy import HookimplMarker

from pytest_testit_parametrize.services.parameter_manager import ParameterManager
from pytest_testit_parametrize.services.plugin_manager import TmsPluginManager

hookimpl = HookimplMarker("testit-parametrize")

__all__ = [
    'ParameterManager',
    'TmsPluginManager',
    'hookimpl'
]
