import abc


class ISQLQueryDataType(abc.ABC):
    """
    Represents the type of a column of a table genrated by a SELECT query.
    It is different than a column from a table, since it does not have parameters:
    for isntance, a column table may be a VARCHAR(50) or VARCHAR(100). A tyep of a column from a SELECT
    is only a VARCHAR with **no** parameters
    """