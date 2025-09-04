import os
from dotenv import load_dotenv
from supabase import create_client, Client

def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

def main():
    supabase = get_client()
    
    # Example 1: Query a common table (adjust table name as needed)
    print("=== Querying Supabase Table ===")
    try:
        # Try common table names - adjust based on your Supabase project
        table_names = ["todos", "users", "posts", "products", "customers"]
        
        for table_name in table_names:
            try:
                print(f"\n--- Querying table: {table_name} ---")
                response = supabase.table(table_name).select("*").limit(3).execute()
                
                if response.data:
                    print(f"Found {len(response.data)} records in {table_name}:")
                    for i, row in enumerate(response.data, 1):
                        print(f"  Record {i}: {row}")
                    break  # Found data, stop trying other tables
                else:
                    print(f"  No data found in {table_name}")
            except Exception as e:
                print(f"  Error querying {table_name}: {str(e)}")
        
        # Example 2: More specific query with filtering
        print(f"\n=== Advanced Query Example ===")
        try:
            # This is an example of a more complex query
            # Adjust the table name and column names based on your actual schema
            response = supabase.table("todos").select("id, title, completed").eq("completed", False).limit(5).execute()
            
            if response.data:
                print("Incomplete todos:")
                for todo in response.data:
                    print(f"  - {todo.get('title', 'No title')} (ID: {todo.get('id')})")
            else:
                print("No incomplete todos found")
        except Exception as e:
            print(f"Advanced query error: {str(e)}")
            
    except Exception as e:
        print(f"Connection error: {str(e)}")
        print("\nMake sure to:")
        print("1. Update SUPABASE_URL and SUPABASE_KEY in your .env file")
        print("2. Ensure your Supabase project has at least one table with data")
        print("3. Check that your table names match what's in your database")

if __name__ == "__main__":
    main()
