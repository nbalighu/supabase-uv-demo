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
    
    # Test connection first
    print("=== Testing Supabase Connection ===")
    try:
        # Try to get table info
        tables_response = supabase.table("sneaker_listings").select("id").limit(1).execute()
        print(f"✅ Connection successful! Table accessible.")
        print(f"Response status: {tables_response}")
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return
    
    # Example 1: Query a common table (adjust table name as needed)
    print("\n=== Querying Supabase Table ===")
    try:
        # Try common table names - adjust based on your Supabase project
        table_names = ["sneaker_listings", "todos", "users", "posts", "products", "customers"]
        
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
                    # Try to get table info even if no data
                    if table_name == "sneaker_listings":
                        print(f"  Table exists but may have RLS policies or be empty")
                        # Try a count query
                        try:
                            count_response = supabase.table(table_name).select("id", count="exact").execute()
                            print(f"  Total records in table: {count_response.count}")
                        except Exception as count_e:
                            print(f"  Count query error: {str(count_e)}")
            except Exception as e:
                print(f"  Error querying {table_name}: {str(e)}")
        
        # Example 2: More specific query with filtering
        print(f"\n=== Advanced Query Example ===")
        try:
            # Query sneaker listings with specific filters
            response = supabase.table("sneaker_listings").select("id, brand, model, size_us, condition, price_usd").eq("condition", "new").limit(5).execute()
            
            if response.data:
                print("New condition sneakers:")
                for sneaker in response.data:
                    print(f"  - {sneaker.get('brand', 'Unknown')} {sneaker.get('model', 'Unknown')} (Size: {sneaker.get('size_us')}, Price: ${sneaker.get('price_usd')})")
            else:
                print("No new condition sneakers found")
                
            # Another query - show all Jordan sneakers
            print(f"\n=== Jordan Sneakers Query ===")
            jordan_response = supabase.table("sneaker_listings").select("id, brand, model, size_us, price_usd, tags").eq("brand", "Jordan").limit(3).execute()
            
            if jordan_response.data:
                print("Jordan sneakers:")
                for sneaker in jordan_response.data:
                    tags = sneaker.get('tags', [])
                    print(f"  - {sneaker.get('brand')} {sneaker.get('model')} (Size: {sneaker.get('size_us')}, Price: ${sneaker.get('price_usd')}, Tags: {tags})")
            else:
                print("No Jordan sneakers found")
                
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
