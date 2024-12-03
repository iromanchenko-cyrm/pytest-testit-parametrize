from testit_python_commons.client.api_client import (
    ApiClientWorker as CommonApiClientWorker,
)

from pytest_testit_parametrize.client import (
    ApiClientWorker,
    ClientConfiguration,
)
from pytest_testit_parametrize.logger import Logger

logger = Logger("parameter_manager").get_logger()


class ParameterManager:

    def __init__(self, client_configuration: ClientConfiguration):
        self.__common_api_client = CommonApiClientWorker(client_configuration)
        self.__api_client = ApiClientWorker(client_configuration)

    def flush_params(self, item):
        logger.info('Flush parameters for "%s"', item.nodeid)
        workitem_ids = self.__get_workitem_ids(item)
        if not workitem_ids:
            return
        if not isinstance(workitem_ids, list):
            workitem_ids = [workitem_ids]
        for workitem_id in workitem_ids:
            self.clean_iterations(workitem_id)

    def enrich_workitem_by_params(self, item):
        logger.info('Enrich workitem by parameters for "%s"', item.nodeid)
        workitem_ids = self.__get_workitem_ids(item)
        if not workitem_ids:
            return
        if not isinstance(workitem_ids, list):
            workitem_ids = [workitem_ids]
        for workitem_id in workitem_ids:
            iterations = self.__api_client.get_iterations(workitem_id)
            if iterations is None:
                continue
            if iterations:
                if self.__can_iteration_being_existed(item, iterations):
                    if self.__is_iteration_exist(item, iterations):
                        logger.info(
                            "Workitem with workitem_id %s already has desired parameters. Skipped",
                            workitem_id,
                        )
                        return
                else:
                    logger.info(
                        "Workitem with workitem_id %s has wrong count of parameters. Flushing...",
                        workitem_id,
                    )
                    self.clean_iterations(workitem_id)
            parameters = self.serve_params(item)
            self.add_iteration(workitem_id, parameters)

    @staticmethod
    def __get_workitem_ids(item):
        if not hasattr(item.function, "test_workitems_id"):
            return None
        if "work_item_id" in item.callspec.params:
            return item.callspec.params["work_item_id"]

        return item.function.test_workitems_id

    @staticmethod
    def __can_iteration_being_existed(item, iterations) -> bool:

        return len(item.callspec.params) == len(iterations[0]["parameters"])

    @staticmethod
    def __is_iteration_exist(item, iterations) -> bool:
        test_params_dict = item.callspec.params
        test_params_dict = {str(k): str(v) for k, v in test_params_dict.items()}
        for iteration in iterations:
            iteration_params_dict = {}
            for parameter in iteration["parameters"]:
                iteration_params_dict.update({parameter["name"]: parameter["value"]})
            if test_params_dict == iteration_params_dict:
                return True

        return False

    def get_iterations(self, workitem_id):
        logger.info("Getting iterations for workitem with workitem_id: %s", workitem_id)

        return self.__api_client.get_iterations(workitem_id)

    def clean_iterations(self, workitem_id):
        workitem = self.__api_client.get_workitem(workitem_id)
        if not workitem:
            return
        if not workitem["iterations"]:
            logger.info(
                "Workitem with workitem_id %s has no parameters. Skipped", workitem_id
            )
        else:
            workitem["iterations"] = []
            self.__api_client.put_workitem(workitem)
            logger.info(
                "Flushed params for workitem with workitem_id %s. Success", workitem_id
            )

    def add_iteration(self, workitem_id, parameters):
        workitem = self.__api_client.get_workitem(workitem_id)
        iterations = self.__extract_iterations(workitem)
        workitem.iterations = []
        workitem.iterations.extend(iterations)
        workitem.iterations.append(
            {"id": "00000000-0000-0000-0000-000000000000", "parameters": parameters}
        )
        self.__api_client.put_workitem(workitem)
        logger.info(
            "Add iteration into workitem with workitem_id %s. Success", workitem_id
        )

    @staticmethod
    def __extract_iterations(workitem):
        iterations = workitem.to_dict()["iterations"]
        for iteration in iterations:
            for parameter in iteration["parameters"]:
                del parameter["parameter_key_id"]
                del parameter["value"]
                del parameter["name"]

        return iterations

    def serve_params(self, item) -> list[dict]:
        logger.info("Serving parameters...")
        parameters_list = []
        for param_name, param_value in item.callspec.params.items():
            param_name, param_value = str(param_name), str(param_value)
            found_param_value = {}
            parameters = self.__api_client.parameters_search_groups(param_name)
            filtered_param = [
                parameter
                for parameter in parameters
                if parameter.get("name") == param_name
            ]
            if filtered_param:
                found_param_value = {
                    id_: value
                    for id_, value in filtered_param[0]["values"].items()
                    if value == param_value
                }
            if not found_param_value:
                created_parameter = self.__api_client.create_parameter(
                    param_name, param_value
                )
                found_param_value = {
                    created_parameter["id"]: created_parameter["value"]
                }
            parameters_list.append({"id": (*found_param_value,)[0]})

        return parameters_list
