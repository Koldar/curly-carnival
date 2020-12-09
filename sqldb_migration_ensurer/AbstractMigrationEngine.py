from typing import Dict, Any, Iterable, List

from sqldb_migration_ensurer.IDatabaseConnector import IDatabaseConnector
from sqldb_migration_ensurer.IMigrationEngine import IMigrationEngine


class AbstractMigrationEngine(IMigrationEngine):

    def __init__(self):
        self.__target: str = None
        self.__database_connector: "IDatabaseConnector" = None
        self.__database_parameters: Dict[str, Any] = {}
        self.__migration_files: List[str] = []
        self.__userdefined_params: Dict[str, Any] = {}

    def set_target(self, name: str):
        self.__target = name

    def get_target(self) -> str:
        return self.__target

    def set_database_connector(self, connector: IDatabaseConnector):
        self.__database_connector = connector

    def get_database_connector(self) -> IDatabaseConnector:
        return self.__database_connector

    def set_database_involved_parameters(self, parameters: Dict[str, Any]):
        self.__database_parameters = parameters

    def set_migration_files(self, files: Iterable[str]):
        self.__migration_files = list(files)

    def set_engine_params(self, d: Dict[str, Any]):
        self.__userdefined_params = d

    def get_engine_params(self, d: Dict[str, Any]):
        return self.__userdefined_params

    def inspect_db(self):
        """
        Scan the involved database and generate a model representing the whole database.
        We also scan user and permissions
        :return:
        """
        


    def migrate(self):
        pass