import abc
from typing import Any, Dict

from sqldb_migration_ensurer.EnsureSQLMigrationStep import EnsureSQLMigrationStep
from sqldb_migration_ensurer.IMigrationEngine import IMigrationEngine


class ISQLMigrationStep(abc.ABC):

    @abc.abstractmethod
    def engine(self) -> IMigrationEngine:
        """
        Gain access to the migration engine

        :return:
        """
        pass

    @abc.abstractmethod
    def context(self) -> EnsureSQLMigrationStep:
        """
        Gain access to a set shared to values among all the migrations

        :return:
        """
        pass

    @abc.abstractmethod
    def name(self) -> str:
        """
        Name that uniquely represents this migration step
        :return:
        """
        pass

    def description(self) -> str:
        """
        A description of the migration. Used for logging
        :return:
        """
        pass

    @abc.abstractmethod
    def commit(self):
        """
        Operations to perform to apply this migration

        :return:
        """
        pass

    @abc.abstractmethod
    def rollback(self):
        """
        Operations to perform to rollback this migration
        :return:
        """
        pass