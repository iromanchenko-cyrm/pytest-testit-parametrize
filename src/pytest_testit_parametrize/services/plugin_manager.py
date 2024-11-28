import logging

from pluggy import PluginManager

from pytest_testit_parametrize.services.parameter_manager import ParameterManager
from testit_python_commons.app_properties import AppProperties


class TmsPluginManager:
    __plugin_manager = None
    __parameters_manager = None
    __logger = None

    @classmethod
    def get_plugin_manager(cls):
        if cls.__plugin_manager is None:
            cls.__plugin_manager = PluginManager('testit-parametrize')

        return cls.__plugin_manager

    @classmethod
    def get_parameters_manager(cls, option=None):
        if cls.__parameters_manager is None:
            from testit_python_commons.client.client_configuration import ClientConfiguration

            app_properties = AppProperties.load_properties(option)

            cls.get_logger(app_properties.get('logs') == 'true')

            client_configuration = ClientConfiguration(app_properties)

            cls.__parameters_manager = ParameterManager(client_configuration)

        return cls.__parameters_manager

    @classmethod
    def get_logger(cls, debug: bool = False):
        if cls.__logger is None:
            if debug:
                logging.basicConfig(format='\n%(levelname)s (%(asctime)s): %(message)s', level=logging.DEBUG)

            cls.__logger = logging.getLogger('TmsLogger')

        return cls.__logger

    @classmethod
    def __getattr__(cls, attribute):
        return getattr(cls.get_plugin_manager(), attribute)
