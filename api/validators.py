import pandas as pd
from typing import Any, List, Dict, Tuple


class DataValidator:

    @staticmethod
    def is_missing_value(value: Any) -> bool:
        if pd.isna(value) or value is None:
            return True

        if isinstance(value, str):
            return value.strip().upper() in {
                '', 'NULL', 'NONE', 'NA', 'N/A', 'NAN',
                '#N/A', 'MISSING', '-', '--', '?'
            }

        return False

    @staticmethod
    def generate_quality_report(data: List[Any]) -> Dict[str, Any]:
        missing_indices = []
        cleaned = []

        for i, v in enumerate(data):
            if DataValidator.is_missing_value(v):
                missing_indices.append(i)
            else:
                cleaned.append(v)

        valid_records = []
        invalid_indices = []
        invalid_values = []
        issues = []

        for idx, value in enumerate(cleaned):
            try:
                valid_records.append(abs(float(value)))
            except (ValueError, TypeError):
                invalid_indices.append(idx)
                invalid_values.append(value)
                issues.append(f"Row {idx}: Non-numeric value '{value}'")

        total_records = len(data)
        valid_count = len(valid_records)
        completeness = (valid_count / total_records *
                        100) if total_records else 0

        ready_for_analysis = valid_count >= 10 and completeness >= 50

        return {
            'summary': {
                'total_records': total_records,
                'valid_records': valid_count,
                'data_completeness': round(completeness, 2),
                'ready_for_analysis': ready_for_analysis
            },
            'missing_values': {
                'count': len(missing_indices),
                'indices': missing_indices
            },
            'invalid_values': {
                'count': len(invalid_indices),
                'indices': invalid_indices,
                'values': invalid_values
            },
            'issues': issues,
            'cleaned_data': valid_records
        }

    @staticmethod
    def preprocess_for_analysis(data: List[Any]) -> Tuple[List[float], Dict[str, Any]]:
        report = DataValidator.generate_quality_report(data)
        return report['cleaned_data'], report
