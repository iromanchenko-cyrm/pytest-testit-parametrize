import testit_api_client
from testit_api_client import ApiClient, Configuration
from testit_api_client.apis import ParametersApi, WorkItemsApi
from testit_api_client.model.api_v2_parameters_search_post_request import (
    ApiV2ParametersSearchPostRequest,
)
from testit_api_client.model.create_parameter_request import (
    CreateParameterRequest,
)
from testit_api_client.model.update_work_item_request import (
    UpdateWorkItemRequest,
)
from testit_python_commons.client import ClientConfiguration
from testit_python_commons.services.logger import (
    adapter_logger as official_logger,
)

from pytest_testit_parametrize.logger import Logger

logger = Logger("api_client").get_logger()


class ApiClientWorker:
    def __init__(self, config: ClientConfiguration):
        api_client_config = self.__get_api_client_configuration(
            url=config.get_url(),
            verify_ssl=config.get_cert_validation() != "false",
            proxy=config.get_proxy(),
        )
        api_client = self.__get_api_client(
            api_client_config, config.get_private_token()
        )

        self.__work_items_api = WorkItemsApi(api_client=api_client)
        self.__parameters_api = ParametersApi(api_client=api_client)
        self.__config = config

    @staticmethod
    @official_logger
    def __get_api_client_configuration(
        url: str, verify_ssl: bool = True, proxy: str = None
    ) -> Configuration:
        api_client_configuration = Configuration(host=url)
        api_client_configuration.verify_ssl = verify_ssl
        api_client_configuration.proxy = proxy

        return api_client_configuration

    @staticmethod
    @official_logger
    def __get_api_client(api_client_config: Configuration, token: str) -> ApiClient:
        return ApiClient(
            configuration=api_client_config,
            header_name="Authorization",
            header_value="PrivateToken " + token,
        )

    @official_logger
    def get_iterations(self, workitem_id):
        api_response = None
        try:
            api_response = self.__work_items_api.get_iterations(id=workitem_id)
        except testit_api_client.ApiException as e:
            logger.error("Exception when calling WorkItemsApi->get_iterations: %s\n", e)

        return api_response

    @official_logger
    def get_workitem(self, workitem_id):
        logger.info("Getting workitem with workitem_id: %s", workitem_id)
        api_response = None
        try:
            api_response = self.__work_items_api.get_work_item_by_id(workitem_id)
        except testit_api_client.ApiException as e:
            logger.error(
                "Exception when calling WorkItemsApi->get_work_item_by_id: %s\n", e
            )
        return api_response

    @official_logger
    def put_workitem(self, workitem):
        update_work_item_request = UpdateWorkItemRequest(
            attachments=workitem["attachments"],
            id=workitem["id"],
            section_id=workitem["section_id"],
            state=workitem["state"],
            priority=workitem["priority"],
            steps=workitem["steps"],
            precondition_steps=workitem["precondition_steps"],
            postcondition_steps=workitem["postcondition_steps"],
            duration=workitem["duration"],
            attributes=workitem["attributes"],
            tags=workitem["tags"],
            links=workitem["links"],
            name=workitem["name"],
            iterations=workitem["iterations"],
            auto_tests=workitem["auto_tests"],
            description=workitem["description"],
            _check_type=False,
        )
        try:
            # Update Test Case, Checklist or Shared Step
            self.__work_items_api.update_work_item(
                update_work_item_request=update_work_item_request
            )
        except testit_api_client.ApiException as e:
            logger.error(
                "Exception when calling WorkItemsApi->update_work_item: %s\n", e
            )

    @official_logger
    def parameters_search_groups(self, param_name):
        skip = 0
        take = 1000
        order_by = "name asc"
        api_v2_parameters_search_post_request = ApiV2ParametersSearchPostRequest()
        api_response = None
        try:
            api_response = self.__parameters_api.api_v2_parameters_search_groups_post(
                skip=skip,
                take=take,
                order_by=order_by,
                search_field="name",
                search_value=param_name,
                api_v2_parameters_search_post_request=api_v2_parameters_search_post_request,
            )
        except testit_api_client.ApiException as e:
            logger.error(
                "Exception when calling ParametersApi->api_v2_parameters_search_groups_post: %s\n",
                e,
            )

        return api_response

    @official_logger
    def create_parameter(self, param_name, param_value):
        api_response = None
        try:
            create_parameter_request = CreateParameterRequest(
                name=param_name, value=param_value
            )
            api_response = self.__parameters_api.create_parameter(
                create_parameter_request=create_parameter_request
            )
        except testit_api_client.ApiException as e:
            logger.error(
                "Exception when calling ParametersApi->create_parameter: %s\n",
                e,
            )
        return api_response
