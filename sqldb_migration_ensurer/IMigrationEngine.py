import abc
from typing import Dict, Any, Iterable

from sqldb_migration_ensurer.IDatabaseConnector import IDatabaseConnector


class IMigrationEngine(abc.ABC):
    """
    Class that manage the whole application
    """

    @abc.abstractmethod
    def set_target(self, name: str):
        """
        Set the target migration the user wants to arrive to

        :param name: name of the migration step
        :return:
        """
        pass

    @abc.abstractmethod
    def get_target(self) -> str:
        """
        get the target migration the user wants to arrive to
        :return: target the user wants to arrive to
        """
        pass

    @abc.abstractmethod
    def set_database_connector(self, connector: IDatabaseConnector):
        """
        set the instance allowing you to connect to the database
        :param connector:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_database_connector(self) -> IDatabaseConnector:
        """

        :return: the instance allowing you to connect to the database
        """
        pass

    @abc.abstractmethod
    def set_engine_params(self, d: Dict[str, Any]):
        """
        Set the user-defined parameters. The engine treats them as is
        :param d:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_engine_params(self, d: Dict[str, Any]):
        pass

    @abc.abstractmethod
    def set_database_involved_parameters(self, parameters: Dict[str, Any]):
        """
        Set the database we need to alter. Note that we might need to alter the database server as well (e.g., users)
        :param parameters: parameters used to create the connector
        """
        pass

    @abc.abstractmethod
    def set_migration_files(self, files: Iterable[str]):
        """
        Set the files representing the migrations we need to handle
        :param files: set of migration file to consider
        :return:
        """
        pass

    @abc.abstractmethod
    def migrate(self):
        """
        perform the migration
        :return:
        """
        pass
