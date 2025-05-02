"""Module for handling output of results to CSV."""

import csv
import sys
import logging
from typing import Dict, List, Optional

from papers_fetcher.filters import filter_non_academic_authors, extract_company_names

logger = logging.getLogger(__name__)

def format_results_for_csv(parsed_articles: List[Dict]) -> List[Dict]:
    """
    Format parsed article data for CSV output.
    
    Args:
        parsed_articles: List of parsed articles
        
    Returns:
        List of dictionaries with fields for CSV output
    """
    csv_rows = []
    
    for article in parsed_articles:
        if not article:
            continue
        
        # Filter non-academic authors
        non_academic_authors = filter_non_academic_authors(article["authors"])
        
        # Skip articles with no non-academic authors
        if not non_academic_authors:
            continue
        
        # Extract company names
        company_names = extract_company_names(non_academic_authors)
        
        # Format the row for CSV
        row = {
            "PubmedID": article["pmid"],
            "Title": article["title"],
            "Publication Date": article["publication_date"],
            "Non-academic Author(s)": "; ".join(author["name"] for author in non_academic_authors),
            "Company Affiliation(s)": "; ".join(company_names),
            "Corresponding Author Email": article["corresponding_email"] or ""
        }
        
        csv_rows.append(row)
    
    return csv_rows

def write_csv(data: List[Dict], filename: Optional[str] = None) -> None:
    """
    Write data to a CSV file or print to console.
    
    Args:
        data: List of dictionaries with data to write
        filename: CSV filename, or None to print to console
    """
    if not data:
        logger.warning("No data to output.")
        print("No data to output.")
        return
    
    fieldnames = [
        "PubmedID", 
        "Title", 
        "Publication Date", 
        "Non-academic Author(s)", 
        "Company Affiliation(s)", 
        "Corresponding Author Email"
    ]
    
    try:
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Results saved to {filename}")
        else:
            # Print to console
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        logger.error(f"Error writing CSV: {e}")
        raise RuntimeError(f"Error writing CSV: {e}")