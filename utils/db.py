from sqlalchemy import create_engine
from utils.settings import config

# Create source database engine
source_engine = create_engine(config.source_db_url)

# Create sink database engine
sink_engine = create_engine(config.sink_db_url)