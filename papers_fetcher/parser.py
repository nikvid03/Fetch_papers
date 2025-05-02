"""Module for parsing and processing PubMed article data."""

import re
import logging
from typing import Dict, List, Optional

from datetime import datetime

logger = logging.getLogger(__name__)

def extract_publication_date(article: Dict) -> str:
    """
    Extract the publication date from a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        Publication date in YYYY-MM-DD format
    """
    try:
        pub_date = article["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
        
        # Different date formats in PubMed
        if "Year" in pub_date and "Month" in pub_date and "Day" in pub_date:
            return f"{pub_date['Year']}-{pub_date['Month'].zfill(2)}-{pub_date['Day'].zfill(2)}"
        elif "Year" in pub_date and "Month" in pub_date:
            return f"{pub_date['Year']}-{pub_date['Month'].zfill(2)}-01"
        elif "Year" in pub_date:
            return f"{pub_date['Year']}-01-01"
        elif "MedlineDate" in pub_date:
            # Try to extract year from MedlineDate (format varies)
            year_match = re.search(r'(\d{4})', pub_date["MedlineDate"])
            if year_match:
                return f"{year_match.group(1)}-01-01"
            
        # Default if we can't parse the date
        return "Unknown"
    
    except KeyError:
        logger.warning("Could not extract publication date")
        return "Unknown"

def extract_title(article: Dict) -> str:
    """
    Extract the title from a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        Article title
    """
    try:
        title = article["MedlineCitation"]["Article"]["ArticleTitle"]
        return title
    except KeyError:
        logger.warning("Could not extract title")
        return "Unknown"

def extract_authors_and_affiliations(article: Dict) -> List[Dict]:
    """
    Extract authors and their affiliations from a PubMed article.
    
    Args:
        article: PubMed article data
        
    Returns:
        List of dictionaries with author name, affiliations, and email
    """
    authors = []
    
    try:
        author_list = article["MedlineCitation"]["Article"]["AuthorList"]
        
        for author in author_list:
            # Skip authors without complete name information
            if "LastName" not in author or "ForeName" not in author:
                continue
            
            name = f"{author['LastName']} {author['ForeName']}"
            affiliations = []
            email = None
            
            # Extract affiliations
            if "AffiliationInfo" in author:
                for affiliation in author["AffiliationInfo"]:
                    if "Affiliation" in affiliation:
                        affiliations.append(affiliation["Affiliation"])
            
            # Extract email from affiliations
            for affiliation in affiliations:
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', affiliation)
                if email_match:
                    email = email_match.group(0)
                    break
            
            authors.append({
                "name": name,
                "affiliations": affiliations,
                "email": email
            })
        
        return authors
    
    except KeyError as e:
        logger.warning(f"Could not extract authors: {e}")
        return []

def extract_corresponding_author_email(authors: List[Dict]) -> Optional[str]:
    """
    Extract the email of the corresponding author.
    
    Args:
        authors: List of author dictionaries
        
    Returns:
        Email address of the corresponding author, if available
    """
    # If any author has an email, return the first one found
    for author in authors:
        if author.get("email"):
            return author["email"]
    
    return None

def parse_article(article: Dict) -> Optional[Dict]:
    """
    Parse a PubMed article to extract relevant information.
    
    Args:
        article: PubMed article data
        
    Returns:
        Dictionary with parsed article data or None if parsing fails
    """
    try:
        pmid = article["MedlineCitation"]["PMID"]
        title = extract_title(article)
        pub_date = extract_publication_date(article)
        authors = extract_authors_and_affiliations(article)
        corresponding_email = extract_corresponding_author_email(authors)
        
        return {
            "pmid": pmid,
            "title": title,
            "publication_date": pub_date,
            "authors": authors,
            "corresponding_email": corresponding_email
        }
    
    except KeyError as e:
        logger.warning(f"Error parsing article: {e}")
        return None