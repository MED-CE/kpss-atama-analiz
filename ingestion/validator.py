import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def validate_placement_data(data: List[Dict]) -> tuple[List[Dict], List[Dict]]:
    """
    Validates the raw placement data.
    Returns a tuple of (valid_data, validation_errors).
    """
    valid_data = []
    validation_errors = []
    
    for idx, row in enumerate(data):
        is_valid = True
        errors = []
        
        # In real OSYM data, column names vary so we check common names
        quota_keys = [k for k in row.keys() if 'KONTENJAN' in str(k).upper()]
        quota = row.get(quota_keys[0]) if quota_keys else None
        
        if quota is not None:
            try:
                if int(quota) < 0:
                    is_valid = False
                    errors.append("Quota cannot be negative")
            except ValueError:
                is_valid = False
                errors.append("Quota is not an integer")
                
        # More checks can be added here
        
        if is_valid:
            valid_data.append(row)
        else:
            validation_errors.append({
                "row_index": idx,
                "row_data": str(row),
                "errors": errors
            })
            
    return valid_data, validation_errors
