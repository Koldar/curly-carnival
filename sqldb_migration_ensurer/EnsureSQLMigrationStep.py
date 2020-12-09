from sqldb_migration_ensurer.ISQLMigrationStep import ISQLMigrationStep


class EnsureSQLMigrationStep(ISQLMigrationStep):
    """
    A migration that declaratively perform an action on the database involved
    """

    def __init__(self):

    def name(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass