from typing import Dict, Any, Iterable

from sqldb_migration_ensurer.AbstractMigrationEngine import AbstractMigrationEngine
from sqldb_migration_ensurer.IMigrationEngine import IMigrationEngine


class StandardMigrationEngine(AbstractMigrationEngine):


    def set_target(self, name: str):
        pass

    def get_target(self) -> str:
        pass

    def set_database_involved_parameters(self, parameters: Dict[str, Any]):
        pass

    def set_migration_files(self, files: Iterable[str]):
        pass