import os
from dotenv import load_dotenv

load_dotenv()

class Configuration:
    def __init__(self):

        # Source Database Configuration
        self.source_db_host = os.getenv('SOURCE_DB_HOST')
        self.source_db_port = os.getenv('SOURCE_DB_PORT')
        self.source_db_name = os.getenv('SOURCE_DB_NAME')
        self.source_db_user = os.getenv('SOURCE_DB_USER')
        self.source_db_password = os.getenv('SOURCE_DB_PASSWORD')
        self.source_db_url = f"postgresql://{self.source_db_user}:{self.source_db_password}@{self.source_db_host}:{self.source_db_port}/{self.source_db_name}"

        # Sink Database Configuration
        self.sink_db_host = os.getenv('SINK_DB_HOST')
        self.sink_db_port = os.getenv('SINK_DB_PORT')
        self.sink_db_name = os.getenv('SINK_DB_NAME')
        self.sink_db_user = os.getenv('SINK_DB_USER')
        self.sink_db_password = os.getenv('SINK_DB_PASSWORD')
        self.sink_db_url = f"postgresql://{self.sink_db_user}:{self.sink_db_password}@{self.sink_db_host}:{self.sink_db_port}/{self.sink_db_name}"

config = Configuration()