"""
Advanced Data Processing Tool
Handles data transformation, analysis, and manipulation
"""
import json
import csv
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union
from io import StringIO
import statistics
from datetime import datetime
from collections import Counter


class DataProcessor:
    """Process and transform various data formats."""
    
    def __init__(self):
        self.transformations = []
    
    def parse_json(self, data: Union[str, bytes]) -> Dict:
        """Parse JSON string."""
        try:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            return json.loads(data)
        except Exception as e:
            return {"error": f"JSON parse error: {e}"}
    
    def to_json(self, data: Any, indent: int = 2) -> str:
        """Convert data to JSON string."""
        try:
            return json.dumps(data, indent=indent, ensure_ascii=False)
        except Exception as e:
            return f"Error: {e}"
    
    def parse_csv(self, data: str, delimiter: str = ',',
                  has_header: bool = True) -> List[Dict]:
        """Parse CSV string."""
        try:
            reader = csv.DictReader(StringIO(data), delimiter=delimiter)
            return list(reader)
        except Exception as e:
            return [{"error": str(e)}]
    
    def to_csv(self, data: List[Dict], delimiter: str = ',') -> str:
        """Convert list of dicts to CSV string."""
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    def parse_xml(self, data: str) -> Dict:
        """Parse XML string to dict."""
        try:
            root = ET.fromstring(data)
            return self._xml_to_dict(root)
        except Exception as e:
            return {"error": str(e)}
    
    def _xml_to_dict(self, element: ET.Element) -> Dict:
        """Convert XML element to dict."""
        result = {}
        
        if element.attrib:
            result['@attributes'] = element.attrib
        
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
        
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Ensure we always return a Dict
        if result:
            return result
        elif element.text:
            return {'text': element.text}
        else:
            return {}
    
    def filter_data(self, data: List[Dict], conditions: Dict) -> List[Dict]:
        """Filter data based on conditions."""
        filtered = []
        
        for item in data:
            match = True
            for key, value in conditions.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                filtered.append(item)
        
        return filtered
    
    def sort_data(self, data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sort data by key."""
        try:
            return sorted(data, key=lambda x: x.get(key, 0), reverse=reverse)
        except Exception as e:
            return data
    
    def group_by(self, data: List[Dict], key: str) -> Dict[str, List[Dict]]:
        """Group data by key."""
        groups = {}
        
        for item in data:
            group_key = item.get(key, 'unknown')
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)
        
        return groups
    
    def aggregate(self, data: List[Dict], key: str, 
                 operation: str = 'sum') -> Union[float, int, str]:
        """
        Aggregate data.
        
        Args:
            data: Data to aggregate
            key: Key to aggregate on
            operation: sum, avg, min, max, count
        """
        values = [item.get(key, 0) for item in data if key in item]
        
        if not values:
            return 0
        
        if operation == 'sum':
            return sum(values)
        elif operation == 'avg':
            return statistics.mean(values)
        elif operation == 'min':
            return min(values)
        elif operation == 'max':
            return max(values)
        elif operation == 'count':
            return len(values)
        elif operation == 'median':
            return statistics.median(values)
        elif operation == 'stdev':
            return statistics.stdev(values) if len(values) > 1 else 0
        else:
            return 0
    
    def merge_data(self, data1: List[Dict], data2: List[Dict], 
                  on_key: str) -> List[Dict]:
        """Merge two datasets on common key."""
        merged = []
        
        # Create lookup dict for data2
        lookup = {item.get(on_key): item for item in data2}
        
        for item1 in data1:
            key_value = item1.get(on_key)
            if key_value in lookup:
                merged_item = {**item1, **lookup[key_value]}
                merged.append(merged_item)
        
        return merged
    
    def pivot_data(self, data: List[Dict], index: str, 
                  columns: str, values: str) -> Dict:
        """Create pivot table."""
        pivot = {}
        
        for item in data:
            idx = item.get(index)
            col = item.get(columns)
            val = item.get(values)
            
            if idx not in pivot:
                pivot[idx] = {}
            pivot[idx][col] = val
        
        return pivot
    
    def calculate_statistics(self, data: List[Union[int, float]]) -> Dict[str, float]:
        """Calculate statistics for numerical data."""
        if not data:
            return {}
        
        return {
            'count': len(data),
            'sum': sum(data),
            'mean': statistics.mean(data),
            'median': statistics.median(data),
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data),
            'stdev': statistics.stdev(data) if len(data) > 1 else 0,
            'variance': statistics.variance(data) if len(data) > 1 else 0
        }
    
    def find_duplicates(self, data: List[Dict], key: str) -> List[Dict]:
        """Find duplicate records based on key."""
        counter = Counter(item.get(key) for item in data)
        duplicates = [k for k, v in counter.items() if v > 1]
        
        return [item for item in data if item.get(key) in duplicates]
    
    def remove_duplicates(self, data: List[Dict], key: str) -> List[Dict]:
        """Remove duplicates keeping first occurrence."""
        seen = set()
        unique = []
        
        for item in data:
            key_value = item.get(key)
            if key_value not in seen:
                seen.add(key_value)
                unique.append(item)
        
        return unique
    
    def normalize_data(self, data: List[float], 
                      min_val: float = 0.0, max_val: float = 1.0) -> List[float]:
        """Normalize data to range [min_val, max_val]."""
        if not data:
            return []
        
        data_min = min(data)
        data_max = max(data)
        
        if data_max == data_min:
            return [min_val] * len(data)
        
        normalized = []
        for value in data:
            norm_value = ((value - data_min) / (data_max - data_min)) * (max_val - min_val) + min_val
            normalized.append(round(norm_value, 4))
        
        return normalized
    
    def transform_column(self, data: List[Dict], column: str, 
                        function: str) -> List[Dict]:
        """
        Apply transformation to column.
        
        Functions: upper, lower, capitalize, strip, int, float
        """
        for item in data:
            if column in item:
                value = item[column]
                
                if function == 'upper' and isinstance(value, str):
                    item[column] = value.upper()
                elif function == 'lower' and isinstance(value, str):
                    item[column] = value.lower()
                elif function == 'capitalize' and isinstance(value, str):
                    item[column] = value.capitalize()
                elif function == 'strip' and isinstance(value, str):
                    item[column] = value.strip()
                elif function == 'int':
                    try:
                        item[column] = int(value)
                    except:
                        pass
                elif function == 'float':
                    try:
                        item[column] = float(value)
                    except:
                        pass
        
        return data


# Global instance
_processor = DataProcessor()

def parse_json(data: str) -> Dict:
    """Parse JSON."""
    return _processor.parse_json(data)

def to_json(data: Any, indent: int = 2) -> str:
    """Convert to JSON."""
    return _processor.to_json(data, indent)

def parse_csv(data: str, delimiter: str = ',') -> List[Dict]:
    """Parse CSV."""
    return _processor.parse_csv(data, delimiter)

def filter_data(data: List[Dict], conditions: Dict) -> List[Dict]:
    """Filter data."""
    return _processor.filter_data(data, conditions)

def aggregate(data: List[Dict], key: str, operation: str = 'sum') -> Union[float, int, str]:
    """Aggregate data."""
    return _processor.aggregate(data, key, operation)

def calculate_stats(data: List[float]) -> Dict:
    """Calculate statistics."""
    return _processor.calculate_statistics(data)
