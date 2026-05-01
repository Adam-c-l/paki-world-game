#!/usr/bin/env python3
"""
Initialize database with default accounts and run the lobby server.
This makes deployment easier - just run this script on first boot.
"""

import os
import sys
import time

# Set up paths early
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append("protocol")

DB_PATH = "/app/data/server.db"
DATA_DIR = "/app/data"

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created data directory: {DATA_DIR}")

def init_db_and_add_accounts():
    """Initialize database using SQLAlchemy and add default accounts"""
    import datetime
    import sqlalchemy
    import SQLUsers
    from SQLUsers import metadata, User, users_table
    
    print("Initializing database...")
    
    # Create engine (same settings as DataHandler)
    engine = sqlalchemy.create_engine('sqlite:///data/server.db', echo=False, pool_recycle=3600)
    
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('PRAGMA journal_mode = MEMORY')
        dbapi_con.execute('PRAGMA synchronous = OFF')
    
    from sqlalchemy import event
    event.listen(engine, 'connect', _fk_pragma_on_connect)
    
    # Create all tables
    metadata.create_all(engine)
    print("Database tables created.")
    
    # Create session
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    
    # Check if users exist
    existing = session.query(User).count()
    if existing > 0:
        print(f"Database already has {existing} users - skipping account creation")
        session.close()
        return
    
    print("Creating default accounts...")
    
    # Create default accounts for private lobby
    default_users = [
        ('player1', 'password1', '127.0.0.1', 'user'),
        ('player2', 'password2', '127.0.0.1', 'user'),
        ('friend', 'friendpass', '127.0.0.1', 'user'),
    ]
    
    now = datetime.datetime.now()
    
    for username, password, ip, access in default_users:
        user = User(
            username=username,
            password=password,
            last_ip=ip,
            email=None,
            access=access
        )
        user.last_login = now
        user.register_date = now
        session.add(user)
        print(f"  Created: {username}")
    
    session.commit()
    session.close()
    
    print("\n" + "=" * 50)
    print("DEFAULT ACCOUNTS CREATED:")
    print("  player1 / password1")
    print("  player2 / password2")
    print("  friend / friendpass")
    print("=" * 50 + "\n")

def main():
    print("=" * 60)
    print("Recoil/UberServer Lobby - Auto-Setup")
    print("=" * 60)
    
    # Ensure data directory exists
    ensure_data_dir()
    
    # Wait for filesystem
    time.sleep(0.5)
    
    # Initialize database and add accounts (one-time setup)
    db_exists = os.path.exists(DB_PATH)
    if not db_exists:
        try:
            init_db_and_add_accounts()
        except Exception as e:
            print(f"Warning during init: {e}")
            print("Server will attempt to create database...")
    else:
        print(f"Database exists at {DB_PATH}")
    
    print("\n" + "=" * 60)
    print("Starting Lobby Server...")
    print("Port: 8200 (Lobby) | Port: 8201 (NAT)")
    print("=" * 60 + "\n")
    
    # Set up arguments for the server
    sys.argv = [
        'server.py',
        '-s', 'sqlite:///data/server.db',
        '-p', '8200',
        '-n', '8201'
    ]
    
    # Import and run the server
    import server

if __name__ == "__main__":
    main()
