# database/db_config
from mysql.connector import pooling

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",          # change if you have another MySQL user
    "password": "wasayraza@9870",          # add your MySQL password here
    "database": "babu"
}

# Create a connection pool (recommended instead of new connections every time)
connection_pool = pooling.MySQLConnectionPool(
    pool_name="ledger_pool",
    pool_size=5,
    **db_config
)

def get_connection():
    """Get a connection from the pool"""
    return connection_pool.get_connection()

