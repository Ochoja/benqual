import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


class DataValidator:
    """Handles data validation, missing value detection, and data quality reporting"""

    @staticmethod
    def detect_missing_values(data: List[Any]) -> Dict[str, Any]:
        """Detect missing values in the dataset"""
        if not isinstance(data, list):
            return {
                'total_records': 0,
                'missing_count': 0,
                'missing_percentage': 0,
                'valid_records': [],
                'missing_indices': [],
                'issues': ['Data is not a list']
            }

        missing_indices = []
        valid_records = []
        issues = []

        for idx, value in enumerate(data):
            if pd.isna(value) or value is None or (isinstance(value, str) and value.strip() == ''):
                missing_indices.append(idx)
                issues.append(f"Row {idx}: Missing value detected")
            else:
                valid_records.append(value)

        total = len(data)
        missing_count = len(missing_indices)
        missing_percentage = (missing_count / total * 100) if total > 0 else 0

        return {
            'total_records': total,
            'missing_count': missing_count,
            'missing_percentage': round(missing_percentage, 2),
            'valid_records': valid_records,
            'valid_count': len(valid_records),
            'missing_indices': missing_indices,
            'issues': issues
        }

    @staticmethod
    def validate_numeric_values(data: List[Any]) -> Dict[str, Any]:
        """Validate that values are numeric and suitable for Benford's Law analysis"""
        invalid_indices = []
        invalid_values = []
        valid_records = []
        issues = []

        for idx, value in enumerate(data):
            if pd.isna(value) or value is None:
                continue

            try:
                numeric_value = float(value)
                if numeric_value == 0:
                    invalid_indices.append(idx)
                    invalid_values.append(value)
                    issues.append(f"Row {idx}: Zero value not suitable for Benford's Law")
                elif numeric_value < 0:
                    issues.append(f"Row {idx}: Negative value - will use absolute value")
                    valid_records.append(abs(numeric_value))
                else:
                    valid_records.append(numeric_value)
            except (ValueError, TypeError):
                invalid_indices.append(idx)
                invalid_values.append(value)
                issues.append(f"Row {idx}: Non-numeric value '{value}'")

        return {
            'valid_records': valid_records,
            'valid_count': len(valid_records),
            'invalid_indices': invalid_indices,
            'invalid_values': invalid_values,
            'invalid_count': len(invalid_indices),
            'issues': issues
        }

    @staticmethod
    def generate_quality_report(data: List[Any]) -> Dict[str, Any]:
        """Generate a comprehensive data quality report"""
        missing_analysis = DataValidator.detect_missing_values(data)
        numeric_analysis = DataValidator.validate_numeric_values(data)

        total_records = len(data)
        valid_for_analysis = numeric_analysis['valid_count']
        data_completeness = (valid_for_analysis / total_records * 100) if total_records > 0 else 0

        return {
            'summary': {
                'total_records': total_records,
                'valid_records': valid_for_analysis,
                'data_completeness': round(data_completeness, 2),
                'ready_for_analysis': valid_for_analysis > 0
            },
            'missing_values': {
                'count': missing_analysis['missing_count'],
                'percentage': missing_analysis['missing_percentage'],
                'indices': missing_analysis['missing_indices']
            },
            'invalid_values': {
                'count': numeric_analysis['invalid_count'],
                'percentage': round((numeric_analysis['invalid_count'] / total_records * 100) if total_records > 0 else 0, 2),
                'indices': numeric_analysis['invalid_indices'],
                'values': numeric_analysis['invalid_values']
            },
            'issues': list(set(missing_analysis['issues'] + numeric_analysis['issues'])),
            'cleaned_data': numeric_analysis['valid_records']
        }

    @staticmethod
    def preprocess_for_analysis(data: List[Any]) -> Tuple[List[float], Dict[str, Any]]:
        """Preprocess data by removing invalid values and returning cleaned dataset with report"""
        report = DataValidator.generate_quality_report(data)
        cleaned_data = report['cleaned_data']

        return cleaned_data, report
