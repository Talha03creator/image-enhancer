from sqlalchemy import create_engine, inspect
from backend.database import SQLALCHEMY_DATABASE_URL

def inspect_db():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        inspector = inspect(engine)
        print("Tables found:", inspector.get_table_names())
        for table_name in inspector.get_table_names():
            print(f"\nColumns in {table_name}:")
            for column in inspector.get_columns(table_name):
                print(f" - {column['name']} ({column['type']})")
    except Exception as e:
        print(f"Error inspecting DB: {e}")

if __name__ == "__main__":
    inspect_db()
