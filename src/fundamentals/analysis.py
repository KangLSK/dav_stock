def analyze_financials(financial_data):
    """
    Analyze financial data to extract key metrics.
    
    Parameters:
    financial_data (dict): A dictionary containing financial statements such as income statement, balance sheet, and cash flow statement.

    Returns:
    dict: A dictionary containing key financial ratios and metrics.
    """
    analysis_results = {}

    # Example calculations
    if 'income_statement' in financial_data:
        income_statement = financial_data['income_statement']
        analysis_results['gross_margin'] = (income_statement['gross_profit'] / income_statement['revenue']) * 100
        analysis_results['net_margin'] = (income_statement['net_income'] / income_statement['revenue']) * 100

    if 'balance_sheet' in financial_data:
        balance_sheet = financial_data['balance_sheet']
        analysis_results['debt_to_equity'] = balance_sheet['total_liabilities'] / balance_sheet['total_equity']

    if 'cash_flow_statement' in financial_data:
        cash_flow_statement = financial_data['cash_flow_statement']
        analysis_results['free_cash_flow'] = cash_flow_statement['operating_cash_flow'] - cash_flow_statement['capital_expenditures']

    return analysis_results

def evaluate_valuation_ratios(price, earnings_per_share, book_value_per_share):
    """
    Evaluate valuation ratios such as P/E and P/B ratios.

    Parameters:
    price (float): Current stock price.
    earnings_per_share (float): Earnings per share.
    book_value_per_share (float): Book value per share.

    Returns:
    dict: A dictionary containing valuation ratios.
    """
    valuation_ratios = {}
    valuation_ratios['price_to_earnings'] = price / earnings_per_share if earnings_per_share else None
    valuation_ratios['price_to_book'] = price / book_value_per_share if book_value_per_share else None

    return valuation_ratios