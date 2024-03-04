"""Contains utilities for calculating benford Law"""
import pandas


class Utils:
    """Checks the quality of data"""

    def check_dataSet(self, data: list[str | int | float]) -> bool:
        """Check data"""
        for item in data:
            if type(int(data)) is not int:
                return False
        return True

    def extract_csv_values(self, filename: str, column: str) -> list:
        """Extract values from a column"""
        try:
            df = pandas.read_csv(filename)  # loads file into dataframe
            values = df[column]  # extract values of a single column
            return values.dropna().tolist()  # convert values to python list and drop NaN values
        except Exception as e:
            return None
