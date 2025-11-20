import os
from typing import Dict, Any, Optional
from datetime import datetime


class ValidationReportDB:
    """Handle database operations for validation reports using Supabase"""

    def __init__(self):
        self.url = os.getenv('VITE_SUPABASE_URL')
        self.key = os.getenv('VITE_SUPABASE_SUPABASE_ANON_KEY')
        self.supabase_client = None

        if self.url and self.key:
            try:
                from supabase import create_client
                self.supabase_client = create_client(self.url, self.key)
                self._init_table()
            except Exception as e:
                print(f"Warning: Could not initialize Supabase client: {e}")

    def _init_table(self):
        """Initialize the validation_reports table if it doesn't exist"""
        if not self.supabase_client:
            return

        try:
            from supabase import create_client
            admin_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            if admin_key:
                admin_client = create_client(self.url, admin_key)
                admin_client.rpc('create_validation_reports_table').execute()
        except Exception as e:
            pass

    def save_validation_report(self, report: Dict[str, Any]) -> Optional[str]:
        """Save a validation report to the database"""
        if not self.supabase_client:
            return None

        try:
            response = self.supabase_client.table('validation_reports').insert({
                'dataset_name': report.get('dataset_name', 'Unnamed Dataset'),
                'total_records': report['summary']['total_records'],
                'valid_records': report['summary']['valid_records'],
                'missing_count': report['missing_values']['count'],
                'invalid_count': report['invalid_values']['count'],
                'data_completeness': report['summary']['data_completeness'],
                'issues': report['issues']
            }).execute()

            return response.data[0]['id'] if response.data else None
        except Exception as e:
            print(f"Error saving validation report: {e}")
            return None

    def get_validation_reports(self, limit: int = 10) -> list:
        """Retrieve recent validation reports"""
        if not self.supabase_client:
            return []

        try:
            response = self.supabase_client.table('validation_reports').select(
                '*'
            ).order('created_at', desc=True).limit(limit).execute()

            return response.data if response.data else []
        except Exception as e:
            print(f"Error retrieving validation reports: {e}")
            return []

    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific validation report"""
        if not self.supabase_client:
            return None

        try:
            response = self.supabase_client.table('validation_reports').select(
                '*'
            ).eq('id', report_id).maybeSingle().execute()

            return response.data if response.data else None
        except Exception as e:
            print(f"Error retrieving validation report: {e}")
            return None
