"""Module for interacting with the PubMed API."""

import time
from typing import Dict, List, Optional
import logging
from Bio import Entrez

logger = logging.getLogger(__name__)

# Default email for Entrez (will be configured by CLI or code using the module)
DEFAULT_EMAIL = "vidyarthinikhil630@gmail.com"

def set_entrez_email(email: str) -> None:
    """
    Set the email address for Entrez to contact if there are issues.
    
    Args:
        email: Email address to use
    """
    Entrez.email = email

# Initialize with default email
set_entrez_email(DEFAULT_EMAIL)

def search_pubmed(query: str, max_results: int = 100, debug: bool = False) -> List[str]:
    """
    Search PubMed for the given query and return a list of PMIDs.
    
    Args:
        query: The PubMed query string
        max_results: Maximum number of results to return
        debug: Whether to print debug information
        
    Returns:
        List of PubMed IDs (PMIDs)
    """
    if debug:
        logger.debug(f"Searching PubMed for: {query}")
        logger.debug(f"Max results: {max_results}")
    
    try:
        # Search PubMed
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        pmids = record["IdList"]
        
        if debug:
            logger.debug(f"Found {len(pmids)} results")
        
        return pmids
    
    except Exception as e:
        if debug:
            logger.error(f"Error searching PubMed: {e}")
        raise RuntimeError(f"Error searching PubMed: {e}")

def fetch_paper_details(pmid_list: List[str], debug: bool = False) -> List[Dict]:
    """
    Fetch detailed information for a list of PubMed IDs.
    
    Args:
        pmid_list: List of PubMed IDs
        debug: Whether to print debug information
        
    Returns:
        List of dictionaries containing paper details
    """
    if not pmid_list:
        return []
    
    if debug:
        logger.debug(f"Fetching details for {len(pmid_list)} papers")
    
    results = []
    
    try:
        # To avoid rate limiting, fetch in batches
        batch_size = 50
        for i in range(0, len(pmid_list), batch_size):
            batch = pmid_list[i:i+batch_size]
            
            if debug:
                logger.debug(f"Fetching batch {i//batch_size + 1} ({len(batch)} papers)")
            
            handle = Entrez.efetch(db="pubmed", id=",".join(batch), retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            for article in records["PubmedArticle"]:
                results.append(article)
            
            # Be nice to the API - pause between batches
            if i + batch_size < len(pmid_list):
                time.sleep(1)
    
    except Exception as e:
        if debug:
            logger.error(f"Error fetching paper details: {e}")
        raise RuntimeError(f"Error fetching paper details: {e}")
    
    return results