/*
  # Create validation_reports table for data quality tracking

  ## Overview
  This migration creates a table to store data quality validation reports for uploaded datasets,
  tracking missing values, invalid values, and overall data completeness metrics.

  ## New Tables
  
  ### `validation_reports`
  Stores comprehensive validation reports for each dataset analysis:
  - `id` (uuid, primary key) - Unique identifier for each validation report
  - `dataset_name` (text) - Name or identifier of the dataset
  - `total_records` (integer) - Total number of records in the dataset
  - `valid_records` (integer) - Number of records suitable for Benford's Law analysis
  - `missing_count` (integer) - Count of missing values detected
  - `invalid_count` (integer) - Count of invalid values (non-numeric, zeros, etc.)
  - `data_completeness` (numeric) - Percentage of valid records (0-100)
  - `issues` (text[]) - Array of specific data quality issues found
  - `created_at` (timestamptz) - Timestamp when report was created
  - `updated_at` (timestamptz) - Timestamp when report was last updated

  ## Security
  - Enable Row Level Security (RLS) on validation_reports table
  - Policy: Allow anyone to read validation reports (public read access)
  - Policy: Allow anyone to create new validation reports (public insert access)

  ## Indexes
  - Index on `created_at` for efficient sorting by date
  - Index on `dataset_name` for filtering by dataset
*/

CREATE TABLE IF NOT EXISTS validation_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_name text NOT NULL DEFAULT 'Unnamed Dataset',
  total_records integer NOT NULL DEFAULT 0,
  valid_records integer NOT NULL DEFAULT 0,
  missing_count integer NOT NULL DEFAULT 0,
  invalid_count integer NOT NULL DEFAULT 0,
  data_completeness numeric(5, 2) NOT NULL DEFAULT 0.00,
  issues text[] DEFAULT ARRAY[]::text[],
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE validation_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to validation reports"
  ON validation_reports
  FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert of validation reports"
  ON validation_reports
  FOR INSERT
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_validation_reports_created_at 
  ON validation_reports(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_validation_reports_dataset_name 
  ON validation_reports(dataset_name);

CREATE OR REPLACE FUNCTION update_validation_reports_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_validation_reports_updated_at
  BEFORE UPDATE ON validation_reports
  FOR EACH ROW
  EXECUTE FUNCTION update_validation_reports_updated_at();
