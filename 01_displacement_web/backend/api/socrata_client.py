from sodapy import Socrata
import pandas as pd

class SocrataClient:
    def __init__(self):
        self.client = Socrata("www.datos.gov.co", None)
        self.dataset_id = "dyjp-uwwh"
    
    def query_exact_match(self, filters):
        where_clauses = []
        
        for key, value in filters.items():
            api_key = key.lower()
            
            if isinstance(value, str):
                escaped_value = value.replace("'", "''")
                where_clauses.append(f"{api_key}='{escaped_value}'")
            else:
                where_clauses.append(f"{api_key}='{value}'")
        
        where_str = " AND ".join(where_clauses)
        
        print(f"\n=== QUERY DEBUG ===")
        print(f"WHERE: {where_str}")
        print(f"==================\n")
        
        try:
            results = self.client.get(
                self.dataset_id,
                where=where_str,
                limit=1000
            )
            
            print(f"Results found: {len(results)}")
            
            if results:
                df = pd.DataFrame.from_records(results)
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error querying API: {e}")
            return pd.DataFrame()
    
    def get_unique_values(self, column):
        try:
            results = self.client.get(
                self.dataset_id,
                select=f"DISTINCT {column}",
                limit=1000
            )
            
            if results:
                values = [r[column.lower()] for r in results if column.lower() in r]
                return sorted(list(set(values)))
            else:
                return []
        except Exception as e:
            print(f"Error getting unique values: {e}")
            return []
    
    def close(self):
        self.client.close()