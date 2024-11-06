import requests

url = "https://seeking-alpha.p.rapidapi.com/symbols/get-summary"

querystring = {"symbols":"tkhvy"}

headers = {
	"x-rapidapi-key": rapid_key,
	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()
    company_data = data['data'][0]['attributes']

    # Prepare formatted data, capturing all attributes
    formatted_data = f"""
    Company Information:
    --------------------
    ID: {data['data'][0]['id']}
    Ticker ID: {data['data'][0]['tickerId']}
    Company Name: {company_data['companyName']}
    Location: {company_data.get('city', 'N/A')}, {company_data.get('country', 'N/A')}
    Address: {company_data.get('streetaddress', 'N/A')}, {company_data.get('streetaddress2', '')}, {company_data.get('zipcode', 'N/A')}
    Phone: {company_data.get('officephonevalue', 'N/A')}
    Year Founded: {company_data.get('yearfounded', 'N/A')}
    Website: {company_data.get('webpage', 'N/A')}
    Sector: {company_data.get('sectorname', 'N/A')}
    Industry: {company_data.get('primaryname', 'N/A')}
    Description: {company_data.get('longDesc', 'N/A')}

    Key Financial Metrics:
    ----------------------
    Market Cap: ${company_data.get('marketCap', 'N/A')}
    Total Debt: ${company_data.get('totalDebt', 'N/A')}
    Total Enterprise Value: ${company_data.get('totalEnterprise', 'N/A')}
    Debt to Equity Ratio: {company_data.get('debtEq', 'N/A')}%
    Long-term Debt to Capital: {company_data.get('ltDebtCap', 'N/A')}%
    Payout Ratio: {company_data.get('payoutRatio', 'N/A')}%
    Price-to-Book Ratio: {company_data.get('priceBook', 'N/A')}
    Revenue Growth (1 Year): {company_data.get('revenueGrowth', 'N/A')}%
    Revenue Growth (3 Years): {company_data.get('revenueGrowth3', 'N/A')}%
    Net Margin: {company_data.get('netMargin', 'N/A')}%
    Gross Margin: {company_data.get('grossMargin', 'N/A')}%
    EBITDA Margin: {company_data.get('ebitMargin', 'N/A')}%
    Earnings Per Share (EPS) Growth: {company_data.get('dilutedEpsGrowth', 'N/A')}%
    Return on Assets (ROA): {company_data.get('roa', 'N/A')}%
    Return on Equity (ROE): {company_data.get('roe', 'N/A')}%
    Levered Free Cash Flow YoY: {company_data.get('leveredFreeCashFlowYoy', 'N/A')}%
    Total Liabilities to Total Assets: {company_data.get('totLiabTotAssets', 'N/A')}%

    Dividends:
    ----------
    Dividend Rate: {company_data.get('divRate', 'N/A')}
    Forward Dividend Rate: {company_data.get('divRateFwd', 'N/A')}
    TTM Dividend Rate: {company_data.get('divRateTtm', 'N/A')}
    Dividend Yield: {company_data.get('divYield', 'N/A')}%
    Forward Dividend Yield: {company_data.get('divYieldFwd', 'N/A')}%
    TTM Dividend Yield: {company_data.get('divYieldTtm', 'N/A')}%
    Dividend Distribution: {company_data.get('divDistribution', 'N/A')}
    Dividend Growth: {company_data.get('dividendGrowth', 'N/A')}

    Recent Dividend Payments:
    -------------------------
    """

    # Add each dividend record
    for dividend in company_data.get('dividends', []):
        formatted_data += f"  - Amount: {dividend['amount']}, Ex Date: {dividend['exDate']}, Pay Date: {dividend['payDate']}, Record Date: {dividend['recordDate']}, Declare Date: {dividend['declareDate']}\n"

    # Additional Metrics and Estimates
    formatted_data += f"""
    Additional Metrics:
    -------------------
    Estimated EPS: {company_data.get('estimateEps', 'N/A')}
    Estimated FFO: {company_data.get('estimateFfo', 'N/A')}
    EV/EBITDA: {company_data.get('evEbitda', 'N/A')}
    EV/Sales: {company_data.get('evSales', 'N/A')}
    Last Close Price/Earnings Ratio: {company_data.get('lastClosePriceEarningsRatio', 'N/A')}
    Forward PE Ratio: {company_data.get('peRatioFwd', 'N/A')}
    Non-GAAP PE Ratio: {company_data.get('peNongaapFy1', 'N/A')}
    Short Interest Percent of Float: {company_data.get('shortIntPctFloat', 'N/A')}
    Analyst Recommendations Count: {company_data.get('totAnalystsRecommendations', 'N/A')}
    52-Week High: {company_data.get('high52', 'N/A')}
    52-Week Low: {company_data.get('low52', 'N/A')}

    Address Details:
    ----------------
    Street Address: {company_data.get('streetaddress', 'N/A')}
    Street Address 2: {company_data.get('streetaddress2', 'N/A')}
    Street Address 3: {company_data.get('streetaddress3', 'N/A')}
    Street Address 4: {company_data.get('streetaddress4', 'N/A')}
    Postal Code: {company_data.get('zipcode', 'N/A')}
    """

    # Save to a text file
    with open("company_summary_full.txt", "w") as file:
        file.write(formatted_data)
    
    print("Full data saved to company_summary_full.txt")
else:
    print("Failed to retrieve data:", response.status_code)