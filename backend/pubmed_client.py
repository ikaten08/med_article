# backend/pubmed_client.py
"""Simple wrapper for PubMed / Europe PMC API (MVP stub).
In production you would use the Entrez E-utilities or EuropePMC REST API.
Here we provide a very small placeholder that returns a list of dicts with the
required fields so the rest of the app can run without external network access.
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict

import httpx

# PubMed API key can be set via environment variable; not required for the stub.
API_KEY = os.getenv("PUBMED_API_KEY")
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def _build_query(days_back: int = 180) -> str:
    """Build a query that restricts to English papers published in the last `days_back` days."""
    today = datetime.utcnow().date()
    start_date = (today - timedelta(days=days_back)).strftime("%Y/%m/%d")
    end_date = today.strftime("%Y/%m/%d")
    # Example query: ("english[lang]") AND ("2024/01/01"[PDAT] : "2024/06/30"[PDAT])
    return f"english[lang] AND ({start_date}[PDAT] : {end_date}[PDAT])"

async def fetch_recent_papers(max_results: int = 20) -> List[Dict]:
    """Fetch recent English papers from PubMed.
    Returns a list of dictionaries containing at least:
        pmid, title, authors, journal, pub_date, abstract, url, study_type
    For the MVP we return a static example list if the network call fails.
    """
    params = {
        "db": "pubmed",
        "term": _build_query(),
        "retmax": max_results,
        "retmode": "json",
        "sort": "pub+date",
    }
    if API_KEY:
        params["api_key"] = API_KEY
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            # The real response parsing would be more complex; here we just mock.
            # In a full implementation you would use the `esummary` or `efetch`
            # endpoint to get details for each PMID.
        except Exception:
            # Network error or API limit – return dummy data
            return [
                {
                    "pmid": "12345678",
                    "title": "Example Randomized Controlled Trial of Home‑Based Care for Elderly Patients",
                    "authors": "Doe J, Smith A",
                    "journal": "J Clin Med",
                    "pub_date": "2026-09-15",
                    "abstract": "This study evaluates...",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
                    "study_type": "Randomized Controlled Trial",
                }
            ]
    # If we got a proper response we would parse IDs and fetch details.
    # For brevity we return an empty list here.
    return []
