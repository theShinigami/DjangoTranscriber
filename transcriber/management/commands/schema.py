# encoding=utf-8
from typing import Any
import logging

from django.db import connection

from django.core.management.base import BaseCommand, CommandParser

# logging
logger = logging.getLogger(__name__)


def schema_exist(schema_name: str) -> bool:
    """
    check if schema exist or not
    :param schema_name: schema name to check
    :type schema_name: str
    :return: bool
    :rtype: bool
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = %s)", [schema_name])
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error("[schema_exist]: unable to check if schema exist or not!")
        logger.error("[schema_exist]: %s", str(e))

    raise Exception("unable to check if schema exist or not!")


def create_schema(schema_name: str) -> bool:
    """
    create schema_name if not exist
    :param schema_name: schema name
    :type schema_name: schema name
    :return: bool
    :rtype: bool
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        return True
    except Exception as e:
        logger.error("[create_schema]: unable to create if schema!")
        logger.error("[create_schema]: %s", str(e))

    return False


class Command(BaseCommand):
    help = "Help to check or create db schema"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('command', choices=['check', 'create', 'cnc'], help='Specify the command to execute.')
        parser.add_argument("-n", "--name", type=str, nargs='?', help="schema name")

    def handle(self, *args: Any, **options: Any) -> None:
        command = options['command']

        if options['name'] is None:
            self.stdout.write(self.style.ERROR("-> schema name must be specified"))
            return

        schema_name = options['name']

        if command == 'check':
            is_exist = schema_exist(schema_name=schema_name)
            self.stdout.write(self.style.SUCCESS(f"-> Schema '{schema_name}', exist: {is_exist}"))
            return
        elif command == 'create':
            is_created = create_schema(schema_name=schema_name)
            self.stdout.write(self.style.SUCCESS(f"-> Schema '{schema_name}' created: {is_created}"))
            return
        elif command == 'cnc':
            # check if the schema exist
            if schema_exist(schema_name=schema_name):
                self.stdout.write(self.style.HTTP_INFO(f"-> The schema {schema_name} has already been created!"))
                return

            is_created = create_schema(schema_name=schema_name)
            if is_created:
                self.stdout.write(self.style.SUCCESS(f"-> The schema '{schema_name}' has been created!"))
                return
            else:
                self.stdout.write(self.style.ERROR(f"-> The Schema '{schema_name}' has not been created!"))
                return
