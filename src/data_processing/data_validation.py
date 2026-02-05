import pandas as pd
import numpy as np
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list
    warnings: list

class DataValidator:
    def __init__(self):
        self.schema = {
            'feature1': {'type': 'float', 'range': (0, 1)},
            'feature2': {'type': 'int', 'range': (0, 100)},
            'feature3': {'type': 'category', 'values': ['A', 'B', 'C']}
        }
    
    def validate(self, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Validate data against schema"""
        errors = []
        warnings = []
        
        # Check columns
        missing_cols = set(self.schema.keys()) - set(data.columns)
        if missing_cols:
            errors.append(f"Missing columns: {missing_cols}")
        
        # Check data types and ranges
        for col, rules in self.schema.items():
            if col in data.columns:
                if rules['type'] == 'float':
                    if not pd.api.types.is_float_dtype(data[col]):
                        errors.append(f"Column {col} must be float")
                
                if 'range' in rules:
                    min_val, max_val = rules['range']
                    if (data[col] < min_val).any() or (data[col] > max_val).any():
                        warnings.append(f"Column {col} has values outside range {rules['range']}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )