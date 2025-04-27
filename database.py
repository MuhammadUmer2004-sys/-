from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define master and replica connection strings
engine_master = create_engine("postgresql://rep_user:Repl1ca@123@master_ip:5432/your_db")
engine_replica = create_engine("postgresql://rep_user:Repl1ca@123@replica_ip:5432/your_db")

# Create session makers
SessionMaster = sessionmaker(bind=engine_master)
SessionReplica = sessionmaker(bind=engine_replica)

# Function to get the session based on read/write
def get_session(is_read=False):
    return SessionReplica() if is_read else SessionMaster()
