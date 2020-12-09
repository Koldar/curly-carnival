import argparse
import importlib
import os
import sys
import logging
from typing import Any, Dict, Iterable

import toml

from sqldb_migration_ensurer.IDatabaseConnector import IDatabaseConnector
from sqldb_migration_ensurer.IMigrationEngine import IMigrationEngine
from sqldb_migration_ensurer.StandardMigrationEngine import StandardMigrationEngine


def parse_options(args):

    parser = argparse.ArgumentParser(
        prog="sqldb-migration-ensurer",
        description="""
            A SQL-like DB migration tool that acts using a declarative language rather than an imperative one.
            Imperative commands are supported as well though.
        """
    )

    parser.add_argument("-c", "--configuration_file", type=str, required=True, default="migration.toml", help="""
        The configuration file used to retrieve 
    """)
    parser.add_argument("-l", "--log_level", type=str, required=True, default="INFO", help="""
        the log level we wuill use to log
    """)

    return parser.parse_args(args)


def read_configuration(path: str):
    with open(path, encoding="utf-8", mode="r") as f:
        content = f.read()
    return toml.loads(content)


def get_engine(config: Dict[str, Any]):
    """
    Generate migration engine
    :param config:
    :return:
    """
    engine_name = str(config["engine"])
    if engine_name == "standard":
        logging.info(f"generating instance StandardMigrationEngine...")
        result = StandardMigrationEngine()
    else:
        raise ValueError(f"Invalid engine name {engine_name}")

    return result


def load_database_connector(module_name: str, class_name: str) -> "IDatabaseConnector":
    """

    :param module_name:
    :param class_name:
    :return:
    :see: https://stackoverflow.com/a/19228066
    """
    # module_name: my_package._my_module"
    # classname: MyClass
    logging.info(f"Loading module {module_name}...")
    module = importlib.import_module(module_name)
    logging.info(f"Loading class {class_name} from module {module.__name__}...")
    connector_class = getattr(module, class_name)
    return connector_class()


def set_database_connector(engine: IMigrationEngine, config: Dict[str, Any]):
    connector_module_name = str(config["connector"]["module"])
    connector_class_name = str(config["connector"]["class"])
    engine.set_database_connector(load_database_connector(connector_module_name, connector_class_name))


def get_migration_files(config: Dict[str, Any]) -> Iterable[str]:
    if "directory" in config:
        yield from get_migration_files_by_directory(
            path=str(config["directory"]["path"]),
            consider_files_that=str(config["directory"]["consider_files_that"])
        )
    else:
        raise ValueError(f"invalid files statements in config. Allowed types are 'directory'")


def safe_eval(expr: str) -> Any:
    env = {}
    return eval(expr, env, env)


def get_migration_files_by_directory(path: str, consider_files_that: str) -> Iterable[str]:
    function = safe_eval(consider_files_that)
    for folder, directories_in_folder, files_in_folder in os.walk(path):
        for x in files_in_folder:
            p = os.path.abspath(os.path.join(folder, x))
            if function(p):
                logging.info(f"Consider migration file {p}")
                yield p


def main():
    options = parse_options(sys.argv[1:])

    # set the log level
    logging.basicConfig(
        level=options.log_level
    )
    # read config
    config = read_configuration(os.path.abspath(os.path.join(options.configuration_file)))
    # generate engine
    engine = get_engine(config["engine"])
    # set target
    engine.set_target(str(config["engine"]["target"]))
    # set migration files
    engine.set_migration_files(get_migration_files(
        config=config["files"]
    ))
    # set database connector
    set_database_connector(
        engine=engine,
        config=config["database"],
    )
    # set database parameters
    engine.set_database_involved_parameters(
        parameters=config["database"]["parameters"]
    )
    # configuration completed! Now let's run the migration tool
    engine.migrate()


if __name__ == "__main__":
    main()
