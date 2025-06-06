import json
from typing import Dict, List, Any
from pathlib import Path

class JSONReader:
    def __init__(self, file_path: str):
        """
        Initialize JSONReader with a file path
        
        Args:
            file_path (str): Path to the JSON file
        """
        self.file_path = Path(file_path)
        self.data = {}
        self.headers = []
        
    def read_file(self) -> None:
        """
        Read the JSON file and store its contents
        """
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
                if isinstance(self.data, list):
                    # If data is a list of objects, get headers from first item
                    if self.data:
                        self.headers = list(self.data[0].keys())
                elif isinstance(self.data, dict):
                    # If data is a single object, get headers from it
                    self.headers = list(self.data.keys())
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found")
            raise
        except json.JSONDecodeError:
            print(f"Error: '{self.file_path}' is not a valid JSON file")
            raise
            
    def get_headers(self) -> List[str]:
        """
        Get all headers from the JSON data
        
        Returns:
            List[str]: List of header names
        """
        return self.headers
    
    def get_data_by_header(self, header: str) -> List[Any]:
        """
        Get all values for a specific header
        
        Args:
            header (str): The header name to get values for
            
        Returns:
            List[Any]: List of values for the specified header
        """
        if not self.data:
            return []
            
        if isinstance(self.data, list):
            return [item.get(header) for item in self.data]
        elif isinstance(self.data, dict):
            return [self.data.get(header)]
        return []
    
    def get_all_data(self) -> Dict[str, List[Any]]:
        """
        Get all data organized by headers
        
        Returns:
            Dict[str, List[Any]]: Dictionary with headers as keys and lists of values as values
        """
        if not self.data:
            return {}
            
        result = {}
        for header in self.headers:
            result[header] = self.get_data_by_header(header)
        return result

# Example usage
if __name__ == "__main__":
    # Example JSON file path
    json_file = "example.json"
    
    try:
        # Create JSONReader instance
        reader = JSONReader(json_file)
        
        # Read the JSON file
        reader.read_file()
        
        # Get all headers
        headers = reader.get_headers()
        print("Headers:", headers)
        
        # Get data for each header
        for header in headers:
            values = reader.get_data_by_header(header)
            print(f"\nValues for {header}:", values)
            
        # Get all data organized by headers
        all_data = reader.get_all_data()
        print("\nAll data organized by headers:", all_data)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}") 