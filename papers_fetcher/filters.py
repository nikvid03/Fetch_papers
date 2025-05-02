"""Module for filtering authors based on their affiliations."""

import re
import logging
from typing import Dict, List, Set, Optional

logger = logging.getLogger(__name__)

# Keywords that indicate academic affiliations
ACADEMIC_KEYWORDS: Set[str] = {
    "university", "college", "school", "institute", "academia", "laboratory", 
    "lab ", "department of", "dept of", "school of", "faculty of", 
    "research center", "research centre", "national", "medical center",
    "hospital", "clinic", "medical school", ".edu", ".ac.", "foundation"
}

# Keywords that indicate pharmaceutical or biotech company affiliations
COMPANY_KEYWORDS: Set[str] = {
    "pharma", "biotech", "therapeutics", "inc", "inc.", "llc", "llc.", 
    "ltd", "ltd.", "limited", "company", "corp", "corp.", "corporation", 
    "bioscience", "biosciences", "biopharma", "health", "sciences", 
    "pharmaceutical", "pharmaceuticals", "gmbh", "ag", "sa", "technology",
    "group", "systems", "solutions", "laboratories", "industries", "products"
}

# Email domains that usually indicate company affiliations
COMPANY_EMAIL_DOMAINS: Set[str] = {
    ".com", ".co", ".io", ".bio", ".ai", ".pharma", ".health", ".tech", ".net"
}

# Email domains that usually indicate academic affiliations
ACADEMIC_EMAIL_DOMAINS: Set[str] = {
    ".edu", ".ac.uk", ".ac.jp", ".ac.", ".gov", ".org", ".nih.gov"
}

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Determine if an affiliation is non-academic (likely a company).
    
    Args:
        affiliation: The affiliation string to check
        
    Returns:
        True if the affiliation appears to be non-academic, False otherwise
    """
    # Convert to lowercase for case-insensitive matching
    affiliation_lower = affiliation.lower()
    
    # Check for academic keywords
    for keyword in ACADEMIC_KEYWORDS:
        if keyword in affiliation_lower:
            return False
    
    # Check for company keywords
    for keyword in COMPANY_KEYWORDS:
        if keyword in affiliation_lower:
            return True
    
    # If no clear indicators, default to False
    return False

def is_company_email(email: Optional[str]) -> bool:
    """
    Determine if an email address is likely from a company.
    
    Args:
        email: The email address to check, or None
        
    Returns:
        True if the email appears to be from a company, False otherwise
    """
    if not email:
        return False
    
    email_lower = email.lower()
    
    # Check for academic email domains
    for domain in ACADEMIC_EMAIL_DOMAINS:
        if domain in email_lower:
            return False
    
    # Check for company email domains
    for domain in COMPANY_EMAIL_DOMAINS:
        if email_lower.endswith(domain):
            return True
    
    return False

def filter_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    """
    Filter authors to include only those with non-academic affiliations.
    
    Args:
        authors: List of author dictionaries
        
    Returns:
        List of non-academic authors
    """
    non_academic_authors = []
    
    for author in authors:
        # Check if any affiliation is non-academic
        non_academic = False
        company_affiliation = None
        
        for affiliation in author.get("affiliations", []):
            if is_non_academic_affiliation(affiliation):
                non_academic = True
                company_affiliation = affiliation
                break
        
        # Check email as a fallback
        if not non_academic and is_company_email(author.get("email")):
            non_academic = True
        
        if non_academic:
            author_copy = author.copy()
            author_copy["company_affiliation"] = company_affiliation
            non_academic_authors.append(author_copy)
    
    return non_academic_authors

def extract_company_names(authors: List[Dict]) -> List[str]:
    """
    Extract company names from author affiliations.
    
    Args:
        authors: List of non-academic author dictionaries
        
    Returns:
        List of company names
    """
    companies = []
    
    for author in authors:
        if "company_affiliation" in author and author["company_affiliation"]:
            # Try to extract the company name from the affiliation
            affiliation = author["company_affiliation"]
            
            # Common patterns: "Company Name, Location" or "Department, Company Name"
            company_match = re.search(r'([A-Z][A-Za-z0-9\s\.&]+(?:Inc\.?|LLC\.?|Ltd\.?|GmbH|AG|SA|Corporation|Corp\.?|Therapeutics|Pharma|Biotech|Biosciences))', affiliation)
            
            if company_match:
                companies.append(company_match.group(1).strip())
            else:
                # Fallback: use the whole affiliation
                companies.append(affiliation)
    
    # Remove duplicates while preserving order
    unique_companies = []
    for company in companies:
        if company not in unique_companies:
            unique_companies.append(company)
    
    return unique_companies