@app.route("/api/benford_test/")
def benford_test():
    data = request.args.get('data')

    if not data:
        return jsonify({'error': 'Missing data parameter', 'details': 'The data parameter is required and must be a JSON array'}), 400

    try:
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        # You can directly use `data` as `values` for analysis
        values = data  # No need to use get_number_pool; just use the data list

        # Use existing methods for analysis
        observed_counts = Utils.count_digits(values)
        actual_percentages = {digit: count / len(values) for digit, count in observed_counts.items()}
        expected_percentages = Utils.get_expected_percentages()
        p_value, chi2_stat = Utils.get_p_value(values)

        # Compute KS Statistic and MAD using existing methods
        ks_statistic, ks_p_value = Utils.get_ks_test(values)
        mad = Utils.get_mad(values)

        return jsonify({
            'actual_percentages': actual_percentages,
            'expected_percentages': expected_percentages,
            'p-value': p_value,
            'chi2_stat': chi2_stat,
            'ks_statistic': ks_statistic,
            'ks_p_value': ks_p_value,
            'mad': mad
        })
    except Exception as e:
        return jsonify({'error': 'Invalid parameter or format', 'details': str(e)}), 400
