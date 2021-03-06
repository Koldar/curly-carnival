import abc
import logging
from typing import Any, Iterable

from collections import OrderedDict

from psycopg2._psycopg import cursor

from sqldb_migration_ensurer.IDatabaseConnector import IDatabaseConnector
from sqldb_migration_ensurer.ISQLQueryDataType import ISQLQueryDataType
from sqldb_migration_ensurer.RowView import RowView
from sqldb_migration_ensurer.sql_query_data_type.DecimalSQLQueryDataType import DecimalSQLQueryDataType
from sqldb_migration_ensurer.sql_query_data_type.IntSQLQueryDataType import IntSQLQueryDataType
from sqldb_migration_ensurer.sql_query_data_type.StringSQLQueryDataType import StringSQLQueryDataType


class AbstractDatabaseConnector(IDatabaseConnector):

    def __init__(self):
        self._is_connected: bool = False

    @abc.abstractmethod
    def _perform_connect(self, **kwargs):
        pass

    @abc.abstractmethod
    def _perform_disconnect(self, **kwargs):
        pass

    @abc.abstractmethod
    def _query_sql_expression(self, query: str, **kwargs):
        """
        A side-effect function that execute a sql query like SELECT on the database
        :param query: the query to execute
        :param kwargs: connector dependent dictionary
        :return:
        """
        pass

    @abc.abstractmethod
    def _fetch_single_row(self, **kwargs) -> Any:
        """
        Side-effect function that fetch a single row from the query output
        :param kwargs:
        :return: the value representing a single row from the query output. None if there is no further row. We assume
        it is an iterable of values
        """
        pass

    def _dispatch_query_expression(self, row, column_types: OrderedDict[str, ISQLQueryDataType], **kwargs) -> RowView:
        """
        convert the result generated by the connector into a rowview
        :param row: row generated by _fetch_single_row
        :param column_types: types of the column
        :param kwargs:
        :return:
        """



    @abc.abstractmethod
    def _detect_row_types(self, query: str, value_from_db, **kwargs) -> OrderedDict[str, ISQLQueryDataType]:
        """
        Wheever requested, we detect the type of each column generated by the query
        :param query: the query that generated this method
        :param value_from_db: the db dependent object representing a single row from the query
        :param kwargs: database dependent arguments. Filled by IDatabaseConnector instance
        :return: a dictionary where each key is the column name while the value is the type of the column itself
        """
        result = OrderedDict()
        cur: cursor = kwargs["cursor"]

        types = {
            int: IntSQLQueryDataType(),
            float: DecimalSQLQueryDataType(),
            str: StringSQLQueryDataType()
        }

        for i, x in enumerate(value_from_db):
            column_name = cur.description[i].name
            # column_type = cur.description[i].type_code
            column_type = types[type(x)]

            result[column_name] = column_type

        return result

    def query(self, query: str, **kwargs) -> Iterable[RowView]:
        cur = kwargs["cursor"]

        fetch_types_in_runtime = self.support_fetching_query_column_type_while_running_query()
        if not fetch_types_in_runtime:
            logging.debug(f"Fetch the types of the outputting the column types")
            # we need to fetch the datatypes using a separate query
            raise NotImplementedError()

        logging.debug(query)
        self._query_sql_expression(query, **kwargs)
        types_found = False
        while True:
            row = self._fetch_single_row(**kwargs)
            if row is None:
                # the table has no more rows
                break
            # there is a row
            if fetch_types_in_runtime and not types_found:
                column_types = self._detect_row_types(
                    query=query,
                    value_from_db=row,
                    **kwargs
                )
                types_found = True
            row_to_yield = self._dispatch_query_expression(row, column_types, **kwargs)
            # yield row: we assume the value generated
            yield row_to_yield

    def connect(self, **kwargs):
        self._perform_connect(**kwargs)
        self._is_connected = True

    def disconnect(self, **kwargs):
        self._perform_disconnect(**kwargs)
        self._is_connected = False

    def is_connected(self) -> bool:
        return self._is_connected
