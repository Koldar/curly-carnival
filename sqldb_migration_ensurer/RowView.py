from typing import Dict, Any, OrderedDict, Tuple

from sqldb_migration_ensurer.ISQLQueryDataType import ISQLQueryDataType


class RowView(object):

    def __init__(self):
        self.row: OrderedDict[str, Tuple[Any, ISQLQueryDataType]] = {}
        """
        A dictionary where each key is a column name.
        Each value is a pair where the first value is the column type while the second is the column value
        """