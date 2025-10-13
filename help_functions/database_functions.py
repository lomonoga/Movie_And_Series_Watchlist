import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from conf import Logger, Config


def check_connect_database(max_retries=5, retry_interval=5) -> bool:
    for attempt in range(max_retries):
        try:
            Logger.info(f"Attempting to connect to the database {attempt + 1}/{max_retries}")

            connection = psycopg2.connect(
                f"postgresql://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_URL}"
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

                if result and result[0] == 1:
                    Logger.info("Connection to the database has been established successfully")
                    connection.close()
                    return True

            connection.close()

        except psycopg2.OperationalError as e:
            Logger.warning(f"The attempt {attempt} failed: {e}")

            if attempt < max_retries:
                Logger.info(f"Trying again in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                Logger.error(f"Failed to connect to database after {max_retries} attempts")
                return False

        except Exception as e:
            Logger.error(f"Unexpected connection error: {e}")
            return False

    return False
