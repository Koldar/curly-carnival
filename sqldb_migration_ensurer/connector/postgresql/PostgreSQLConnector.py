import logging
from typing import Iterable, Dict, Any

import psycopg2

from sqldb_migration_ensurer.AbstractDatabaseConnector import AbstractDatabaseConnector
from sqldb_migration_ensurer.IDatabaseConnector import IDatabaseConnector
from sqldb_migration_ensurer.RowView import RowView


class PostgreSQLConnector(AbstractDatabaseConnector):

    def get_database_names(self) -> Iterable[str]:
        with self.__connection.cursor() as cur:


    def __init__(self):
        super().__init__()

        self.__connection = None

    def _perform_connect(self, **kwargs):
        if self.__connection is None:
            c = {}
            if "databasename" in kwargs:
                c["dbname"] = kwargs["databasename"]
            if "username" in kwargs:
                c["user"] = kwargs["username"]
            if "password" in kwargs:
                c["password"] = kwargs["password"]
            if "host" in kwargs:
                c["host"] = kwargs["host"]
            if "port" in kwargs:
                c["port"] = kwargs["port"]

            self.__connection = psycopg2.connect(**c)

    def _perform_disconnect(self, **kwargs):
        if self.__connection is not None:
            self.__connection.close()

    def _detect_row_types(self, query: str, value_from_db, **kwargs) -> Dict[str, Any]:


        # SELECT datname FROM pg_database
    # WHERE datistemplate = false;

    def _query_sql_expression(self, query: str, **kwargs):
        kwargs["cursor"].execute(query)

    def _fetch_single_row(self, **kwargs) -> Any:
        return kwargs["cursor"].fetchone()

    def query(self, query: str, **kwargs) -> Iterable[RowView]:



