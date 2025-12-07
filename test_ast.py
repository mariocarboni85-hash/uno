
class DataProcessor:
    """Process data efficiently"""
    
    def __init__(self, data):
        self.data = data
    
    def process(self):
        """Process all data"""
        return [x * 2 for x in self.data]
    
    def validate(self, threshold=100):
        """Validate data against threshold"""
        return all(x < threshold for x in self.data)
