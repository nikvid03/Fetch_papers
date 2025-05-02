"""Command-line interface for the papers_fetcher module."""

import argparse
import sys
import logging
import traceback
from typing import List, Optional

from papers_fetcher.api import search_pubmed, fetch_paper_details, set_entrez_email
from papers_fetcher.parser import parse_article
from papers_fetcher.output import format_results_for_csv, write_csv

def configure_logging(debug: bool) -> None:
    """
    Configure logging based on debug flag.
    
    Args:
        debug: Whether to enable debug logging
    """
    log_level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Fetch research papers with authors from pharmaceutical or biotech companies.'
    )
    
    parser.add_argument(
        'query',
        help='PubMed query string (supports full PubMed query syntax)'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print debug information during execution'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Specify the filename to save the results (if not provided, print to console)'
    )
    
    parser.add_argument(
        '-m', '--max-results',
        type=int,
        default=100,
        help='Maximum number of results to fetch (default: 100)'
    )
    
    parser.add_argument(
        '-e', '--email',
        default="user@example.com",
        help='Email address for PubMed API (default: user@example.com)'
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point for the command-line interface."""
    args = parse_arguments()
    
    # Configure logging
    configure_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    # Set email for PubMed API
    set_entrez_email(args.email)
    
    try:
        # Search PubMed
        if args.debug:
            print(f"Searching PubMed for: {args.query}")
        
        pmids = search_pubmed(args.query, max_results=args.max_results, debug=args.debug)
        
        if not pmids:
            print("No papers found matching the query.")
            sys.exit(0)
        
        # Fetch paper details
        articles = fetch_paper_details(pmids, debug=args.debug)
        
        if args.debug:
            print(f"Fetched details for {len(articles)} papers")
        
        # Parse articles
        parsed_articles = []
        for article in articles:
            parsed = parse_article(article)
            if parsed:
                parsed_articles.append(parsed)
        
        if args.debug:
            print(f"Successfully parsed {len(parsed_articles)} papers")
        
        # Format results for CSV
        csv_data = format_results_for_csv(parsed_articles)
        
        if not csv_data:
            print("No papers found with authors from pharmaceutical or biotech companies.")
            sys.exit(0)
        
        if args.debug:
            print(f"Found {len(csv_data)} papers with non-academic authors")
        
        # Write CSV output
        write_csv(csv_data, args.file)
        
        if args.file:
            print(f"Results saved to {args.file}")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")
        if args.debug:
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()