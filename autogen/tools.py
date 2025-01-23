import os
import json
import financedatabase as fd
import financetoolkit as ftk
import numpy as np
from typing_extensions import Annotated
import pandas as pd
import requests
from pathlib import Path
from configs import COMPANIES_JSON_PATH
from tavily import TavilyClient


def save_response_json(
    response_json: Annotated[str, "JSON String to save"],
    path: Annotated[str, "Path to save"],
) -> None:
    """
    Save the given JSON string to a file.

    Parameters:
    response_json (str): The JSON string to be saved.
    path (str): The path to the file where the JSON string will be saved.
    """
    data = json.loads(response_json)
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"JSON response saved to {path}")


def save_to_markdown(
    content: str,
    file_path: Annotated[str, "Path to save markdown file"] = "output.md",
) -> None:
    """
    Save the given content to a markdown file, overwriting the file if it already exists.

    Parameters:
    content (str): The content to be saved.
    file_path (str): The path to the markdown file. Default is 'output.md'.
    """
    with open(file_path, "w") as file:
        file.write(content)
    print(f"Content written to {file_path}")


def read_from_markdown(
    filepath: Annotated[str, "Path of Strategy Report"]
) -> Annotated[str, "Content of Strategy Report"]:
    """
    Read the content from a markdown file.

    Parameters:
    filepath (str): The path to the markdown file.

    Returns:
    str: The content of the markdown file.
    """
    with open(filepath, "r") as file:
        content = file.read()
    return content


def save_json_to_disk(
    data: dict, file_path: Annotated[str, "Path to save JSON file"] = "data.json"
) -> None:
    """
    Save the given dictionary as a JSON file.

    Parameters:
    data (dict): The dictionary to be saved.
    file_path (str): The path to the JSON file. Default is 'data.json'.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"JSON data written to {file_path}")


def read_json_from_disk(file_path: Annotated[str, "Path to JSON file"]) -> dict:
    """
    Read the content from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The content of the JSON file.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def get_options(parameter: Annotated[str, "Parameter you want options for"]) -> dict:
    """
    Retrieve options for a given parameter.

    Args:
        parameter (str): The parameter you want options for.

    Returns:
        dict: A dictionary containing the options for the specified parameter.
    """

    options = fd.obtain_options("equities")
    return convert_ndarray_to_list(options[parameter])


def convert_ndarray_to_list(data):
    """
    Recursively convert numpy ndarrays to lists in a dictionary.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, dict):
        return {key: convert_ndarray_to_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_ndarray_to_list(element) for element in data]
    else:
        return data


def get_companies(
    currency: Annotated[str, "Currency"] = "USD",
    sector: Annotated[str, "Sector"] = "Information Technology",
    industry_group: Annotated[str, "Industry Group"] = "Software & Services",
    industry: Annotated[str, "Industry"] = "Software",
    exchange: Annotated[str, "Exchange"] = "NASDAQ",
    market: Annotated[str, "Market"] = "us_market",
    country: Annotated[str, "Country"] = "United States",
    market_cap: Annotated[str, "Market Cap"] = "Small Cap",
    path: Annotated[str, "Path to save JSON file"] = "companies.json",
) -> str:
    """
    Filters and saves a list of companies based on specified criteria.
    Args:
        currency (str): The currency in which the companies operate. Default is "USD".
        sector (str): The sector to which the companies belong. Default is "Information Technology".
        industry_group (str): The industry group to which the companies belong. Default is "Software & Services".
        industry (str): The industry to which the companies belong. Default is "Software".
        exchange (str): The stock exchange on which the companies are listed. Default is "NASDAQ".
        market (str): The market in which the companies operate. Default is "us_market".
        country (str): The country in which the companies are based. Default is "United States".
        market_cap (str): The market capitalization of the companies. Default is "Small Cap".
        path (str): The file path to save the filtered companies in JSON format. Default is "companies.json".
    Returns:
        str: A message indicating the completion of the operation.
    """

    equities = fd.Equities()
    companies = equities.select()

    # Filter the DataFrame based on specific values of multiple columns using .loc
    filtered_companies = companies.loc[
        (companies["currency"] == currency)
        & (companies["sector"] == sector)
        & (companies["industry_group"] == industry_group)
        & (companies["industry"] == industry)
        & (companies["country"] == country)
        & (companies["market_cap"] == market_cap)
    ]

    # Drop rows with NaN values in the 'summary' column
    filtered_companies = filtered_companies.dropna(subset=["summary"])

    # Save the filtered DataFrame to a CSV file
    filtered_companies.to_csv("companies.csv", index=True)

    # Convert the filtered DataFrame to JSON and save to a file
    with open(path, "w") as file:
        json.dump(
            json.loads(filtered_companies.reset_index().to_json(orient="records")),
            file,
            indent=4,
        )

    return "Done"
    # return filtered_companies


def get_number_of_companies(path: Annotated[str, "Path to JSON file"]) -> int:
    """
    Get the number of companies in the JSON file.

    Parameters:
    path (str): The path to the JSON file.

    Returns:
    int: The number of companies in the JSON file.
    """
    companies = read_json_from_disk(path)
    return len(companies)


def get_names_and_summaries(path: Annotated[str, "Path to JSON file"]) -> str:
    """
    Get the symbols, names and summaries of companies from the JSON file.

    Parameters:
    path (str): The path to the JSON file.

    Returns:
    str: A JSON string containing the symbols, names and summaries of companies.
    """
    companies = read_json_from_disk(path)
    df = pd.DataFrame(companies, columns=["symbol", "name", "summary"])
    df = df.reset_index(drop=True)
    return df.to_json(orient="records", indent=4)


def collect_and_save_fmp_data(
    symbol: Annotated[str, "Symbol for which data needs to be collected"],
    path: Annotated[str, "Path to save collected data"],
) -> str:
    """Collect FMP data and save it, returning only a status message"""
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        return (
            "FMP API key not found. Please set the 'FMP_API_KEY' environment variable."
        )
    base_url = "https://financialmodelingprep.com/api/v3"

    endpoints = {
        "financials": f"/financials/income-statement/{symbol}",
        "balance_sheet": f"/financials/balance-sheet-statement/{symbol}",
        "cash_flow": f"/financials/cash-flow-statement/{symbol}",
        "ratios": f"/key-ratios/{symbol}",
        "quote": f"/quote/{symbol}",
        "sector_performance": "/sector-performance",
        "macro_data": "/economic-indicator",
    }

    data = {}
    try:
        for key, endpoint in endpoints.items():
            url = f"{base_url}{endpoint}?apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data[key] = response.json()

        base_path = str(Path(path))
        os.makedirs(base_path, exist_ok=True)
        filepath = Path(base_path) / f"{symbol}_fmp.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return f"Successfully collected and saved FMP data for {symbol}"
    except Exception as e:
        return f"Error processing {symbol}: {str(e)}"


def tavily_search(query: Annotated[str, "Query to search for"]) -> str:
    """
    Search for a company using Tavily API.

    Parameters:
    query (str): The query to search for.

    Returns:
    str: A JSON string containing the search results.
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    search_results = client.qna_search(query)
    print(search_results)


if __name__ == "__main__":
    query = input("Enter a query to search for: ")
    tavily_search(query=query)
    # Find all the publicaly listed companies working in Electronics manufacturing
