
from market.configs import PostgresConfigDev


class PostgresConfigTestDev(PostgresConfigDev):
    DB_NAME = 'test_market'
