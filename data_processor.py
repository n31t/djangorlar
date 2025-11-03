"""
Data Processing Utility Module

This module provides various data processing and analysis functions
for handling complex data transformations and calculations.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from collections import defaultdict
import statistics


class DataProcessor:
    """A comprehensive data processing class for various data operations."""

    def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
        """Initialize the DataProcessor with optional data."""
        self.data = data or []
        self.processed_count = 0
        self.error_log = []

    def add_record(self, record: Dict[str, Any]) -> None:
        """Add a single record to the data collection."""
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary")
        self.data.append(record)

    def add_records(self, records: List[Dict[str, Any]]) -> None:
        """Add multiple records to the data collection."""
        for record in records:
            self.add_record(record)

    def filter_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """Filter records by a specific field value."""
        return [record for record in self.data if record.get(field) == value]

    def filter_by_date_range(self, date_field: str, start_date: datetime,
                            end_date: datetime) -> List[Dict[str, Any]]:
        """Filter records by a date range."""
        filtered = []
        for record in self.data:
            record_date = record.get(date_field)
            if isinstance(record_date, datetime):
                if start_date <= record_date <= end_date:
                    filtered.append(record)
        return filtered

    def group_by_field(self, field: str) -> Dict[Any, List[Dict[str, Any]]]:
        """Group records by a specific field."""
        grouped = defaultdict(list)
        for record in self.data:
            key = record.get(field)
            if key is not None:
                grouped[key].append(record)
        return dict(grouped)

    def calculate_statistics(self, numeric_field: str) -> Dict[str, float]:
        """Calculate statistical metrics for a numeric field."""
        values = []
        for record in self.data:
            value = record.get(numeric_field)
            if isinstance(value, (int, float)):
                values.append(value)

        if not values:
            return {}

        return {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'sum': sum(values),
            'count': len(values)
        }

    def transform_field(self, field: str, transform_func) -> None:
        """Apply a transformation function to a specific field in all records."""
        for record in self.data:
            if field in record:
                try:
                    record[field] = transform_func(record[field])
                    self.processed_count += 1
                except Exception as e:
                    self.error_log.append({
                        'record': record,
                        'field': field,
                        'error': str(e)
                    })

    def remove_duplicates(self, key_field: str) -> int:
        """Remove duplicate records based on a key field."""
        seen = set()
        unique_data = []
        duplicates_removed = 0

        for record in self.data:
            key = record.get(key_field)
            if key not in seen:
                seen.add(key)
                unique_data.append(record)
            else:
                duplicates_removed += 1

        self.data = unique_data
        return duplicates_removed

    def sort_by_field(self, field: str, reverse: bool = False) -> None:
        """Sort records by a specific field."""
        self.data.sort(key=lambda x: x.get(field, ''), reverse=reverse)

    def export_to_json(self, filename: str) -> bool:
        """Export data to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            return True
        except Exception as e:
            self.error_log.append({'export_error': str(e)})
            return False

    def export_to_csv(self, filename: str, fields: Optional[List[str]] = None) -> bool:
        """Export data to a CSV file."""
        if not self.data:
            return False

        try:
            if fields is None:
                fields = list(self.data[0].keys())

            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.data)
            return True
        except Exception as e:
            self.error_log.append({'export_error': str(e)})
            return False

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the current data state."""
        return {
            'total_records': len(self.data),
            'processed_count': self.processed_count,
            'error_count': len(self.error_log),
            'fields': list(self.data[0].keys()) if self.data else []
        }

    def clear_data(self) -> None:
        """Clear all data and reset counters."""
        self.data = []
        self.processed_count = 0
        self.error_log = []


def create_sample_dataset(num_records: int = 100) -> List[Dict[str, Any]]:
    """Create a sample dataset for testing purposes."""
    dataset = []
    base_date = datetime.now()

    for i in range(num_records):
        record = {
            'id': i + 1,
            'name': f'Item_{i + 1}',
            'value': (i + 1) * 10.5,
            'category': f'Category_{(i % 5) + 1}',
            'date': base_date - timedelta(days=i),
            'active': i % 2 == 0
        }
        dataset.append(record)

    return dataset
