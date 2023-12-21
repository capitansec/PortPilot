import os

import dotenv
import redis

dotenv.load_dotenv()


class RedisConnector:
    """
    This class is used for connecting to Redis and managing the connection lifecycle.
    """

    def __init__(self):
        """
        Initializes the Redis connection parameters.
        """
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.connection = None
        # Shared/bucket ?

    def __enter__(self):
        """
        Enters the context and establishes a Redis connection.
        """
        self.connection = redis.Redis(host=self.host, port=self.port, db=0)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context and closes the Redis connection.
        """
        if self.connection is not None:
            self.connection.close()
