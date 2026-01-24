"""
Paper Finder Script for PhD Topic:
"Development of an AI-Based Model to Predict Depression in Women"

Sources:
1) Semantic Scholar API (no key required for basic usage)
2) Crossref API
3) PubMed (NCBI E-utilities)

Outputs:
- results_<timestamp>.csv
- results_<timestamp>.json
"""

import csv
import json
import time
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlencode
import requests


# ----------------------------
# Config
# ----------------------------

DEFAULT_QUERIES = [
    # core query - AI/ML based depression prediction in women
    '("depression" OR "major depressive disorder") AND (women OR female) AND (prediction OR predictive) AND ("machine learning" OR "deep learning" OR "artificial intelligence")',
    # specific ML approaches
    '(women OR female) depression prediction "machine learning" model',
    'postpartum depression prediction "machine learning" women',
    'perinatal depression prediction model "artificial intelligence"',
    'depression screening women "deep learning"',
    'depression risk prediction women "electronic health records" AI',
    # additional relevant queries
    'women depression "neural network" prediction',
    'female depression "random forest" OR "support vector machine" prediction',
    'maternal depression AI prediction model',
]

# Year filter: 2010-2025
YEAR_START = 2010
YEAR_END = 2025

HEADERS = {
    "User-Agent": "PhD-Paper-Finder/1.0 (contact: youremail@example.com)"
}

TIMEOUT = 30


@dataclass
class Paper:
    source: str
    title: str
    year: str
    authors: str
    publication_venue: str
    abstract_findings: str
    doi: str
    url: str
    citations: str
    keywords: str
    study_type: str


def safe_get(d, path, default=""):
    """Get nested dict keys with a list path."""
    cur = d
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return default
    return cur if cur is not None else default


def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ----------------------------
# Semantic Scholar Search
# ----------------------------

def search_semanticscholar(query: str, limit: int = 25, offset: int = 0) -> list[Paper]:
    """
    Semantic Scholar: https://api.semanticscholar.org/
    Endpoint: /graph/v1/paper/search
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "fields": "title,year,authors,venue,abstract,externalIds,url,citationCount,publicationTypes",
        "year": f"{YEAR_START}-{YEAR_END}"  # Filter by year range
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    out = []

    for item in data.get("data", []):
        year = item.get("year", "")
        # Double-check year filter
        if year and (int(year) < YEAR_START or int(year) > YEAR_END):
            continue
            
        authors = ", ".join([a.get("name", "") for a in item.get("authors", []) if a.get("name")])
        doi = safe_get(item, ["externalIds", "DOI"], "")
        pub_types = ", ".join(item.get("publicationTypes", []) or [])
        
        out.append(Paper(
            source="SemanticScholar",
            title=clean_text(item.get("title", "")),
            year=str(year),
            authors=clean_text(authors),
            publication_venue=clean_text(item.get("venue", "")),
            abstract_findings=clean_text(item.get("abstract", "")),
            doi=clean_text(doi),
            url=clean_text(item.get("url", "")),
            citations=str(item.get("citationCount", "")),
            keywords="",
            study_type=clean_text(pub_types),
        ))

    return out


# ----------------------------
# Crossref Search
# ----------------------------

def search_crossref(query: str, rows: int = 25, offset: int = 0) -> list[Paper]:
    """
    Crossref: https://api.crossref.org/works
    Good for DOI + journal metadata.
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": rows,
        "offset": offset,
        "filter": f"from-pub-date:{YEAR_START},until-pub-date:{YEAR_END}",
        "select": "title,author,issued,container-title,DOI,URL,is-referenced-by-count,abstract,type,subject"
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    items = safe_get(data, ["message", "items"], [])

    out = []
    for it in items:
        title_list = it.get("title", [])
        title = title_list[0] if title_list else ""
        year = ""
        issued = safe_get(it, ["issued", "date-parts"], [])
        if issued and isinstance(issued, list) and issued[0]:
            year = str(issued[0][0])
        
        # Filter by year
        if year and (int(year) < YEAR_START or int(year) > YEAR_END):
            continue

        authors = []
        for a in it.get("author", []) or []:
            given = a.get("given", "")
            family = a.get("family", "")
            name = (given + " " + family).strip()
            if name:
                authors.append(name)

        venue_list = it.get("container-title", [])
        venue = venue_list[0] if venue_list else ""
        
        abstract = it.get("abstract", "")
        subjects = ", ".join(it.get("subject", []) or [])
        study_type = it.get("type", "")

        out.append(Paper(
            source="Crossref",
            title=clean_text(title),
            year=clean_text(year),
            authors=clean_text(", ".join(authors)),
            publication_venue=clean_text(venue),
            abstract_findings=clean_text(abstract),
            doi=clean_text(it.get("DOI", "")),
            url=clean_text(it.get("URL", "")),
            citations=str(it.get("is-referenced-by-count", "")),
            keywords=clean_text(subjects),
            study_type=clean_text(study_type),
        ))

    return out


# ----------------------------
# PubMed Search (NCBI)
# ----------------------------

def pubmed_esearch(query: str, retmax: int = 25, retstart: int = 0) -> list[str]:
    """
    Step 1: get PubMed IDs using esearch with year filter
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    # Add year filter to query
    query_with_year = f"{query} AND {YEAR_START}:{YEAR_END}[pdat]"
    params = {
        "db": "pubmed",
        "term": query_with_year,
        "retmode": "json",
        "retmax": retmax,
        "retstart": retstart,
        "sort": "relevance",
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return safe_get(data, ["esearchresult", "idlist"], [])


def pubmed_esummary(pmids: list[str]) -> list[Paper]:
    """
    Step 2: fetch summaries using esummary
    """
    if not pmids:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()

    out = []
    result = data.get("result", {})
    for pmid in pmids:
        it = result.get(pmid, {})
        if not it:
            continue

        title = it.get("title", "")
        year = ""
        pubdate = it.get("pubdate", "")
        if pubdate:
            year = pubdate.split(" ")[0]
        
        # Filter by year
        try:
            if year and (int(year) < YEAR_START or int(year) > YEAR_END):
                continue
        except:
            pass

        authors = ", ".join([a.get("name", "") for a in it.get("authors", []) if a.get("name")])
        venue = it.get("fulljournalname", "")
        pub_type = ", ".join(it.get("pubtype", []) or [])

        # PubMed URL
        url_p = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        out.append(Paper(
            source="PubMed",
            title=clean_text(title),
            year=clean_text(year),
            authors=clean_text(authors),
            publication_venue=clean_text(venue),
            abstract_findings="",   # esummary doesn't include abstract
            doi="",        # not always in esummary
            url=url_p,
            citations="",  # not in PubMed summary
            keywords="",
            study_type=clean_text(pub_type),
        ))
    return out


# ----------------------------
# Helpers: Dedup + Save
# ----------------------------

def deduplicate(papers: list[Paper]) -> list[Paper]:
    """
    Deduplicate by DOI if available else by (title+year).
    """
    seen = set()
    out = []
    for p in papers:
        key = ""
        if p.doi:
            key = "doi:" + p.doi.lower().strip()
        else:
            key = "ty:" + (p.title.lower().strip() + "|" + p.year.strip())
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def save_outputs(papers: list[Paper], prefix: str = "results") -> tuple[str, str]:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"{prefix}_{ts}.csv"
    json_path = f"{prefix}_{ts}.json"

    # CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(papers[0]).keys()) if papers else [
            "source","title","year","authors","publication_venue","abstract_findings","doi","url","citations","keywords","study_type"
        ])
        w.writeheader()
        for p in papers:
            w.writerow(asdict(p))

    # JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in papers], f, ensure_ascii=False, indent=2)

    return csv_path, json_path


# ----------------------------
# Main Runner
# ----------------------------

def run_search(
    queries: list[str] = None,
    per_query: int = 25,
    semantic_pages: int = 1,
    crossref_pages: int = 1,
    pubmed_pages: int = 1,
    sleep_sec: float = 0.8
):
    queries = queries or DEFAULT_QUERIES
    all_papers: list[Paper] = []

    for q in queries:
        print(f"\n=== Query: {q} ===")

        # Semantic Scholar
        for page in range(semantic_pages):
            offset = page * per_query
            try:
                papers = search_semanticscholar(q, limit=per_query, offset=offset)
                print(f"SemanticScholar page {page+1}: {len(papers)}")
                all_papers.extend(papers)
            except Exception as e:
                print(f"SemanticScholar error: {e}")
            time.sleep(sleep_sec)

        # Crossref
        for page in range(crossref_pages):
            offset = page * per_query
            try:
                papers = search_crossref(q, rows=per_query, offset=offset)
                print(f"Crossref page {page+1}: {len(papers)}")
                all_papers.extend(papers)
            except Exception as e:
                print(f"Crossref error: {e}")
            time.sleep(sleep_sec)

        # PubMed
        for page in range(pubmed_pages):
            retstart = page * per_query
            try:
                pmids = pubmed_esearch(q, retmax=per_query, retstart=retstart)
                papers = pubmed_esummary(pmids)
                print(f"PubMed page {page+1}: {len(papers)}")
                all_papers.extend(papers)
            except Exception as e:
                print(f"PubMed error: {e}")
            time.sleep(sleep_sec)

    all_papers = [p for p in all_papers if p.title]  # remove empty
    deduped = deduplicate(all_papers)
    print(f"\nTotal collected: {len(all_papers)} | After dedup: {len(deduped)}")

    if deduped:
        csv_path, json_path = save_outputs(deduped, prefix="phd_depression_women")
        print(f"Saved CSV : {csv_path}")
        print(f"Saved JSON: {json_path}")
    else:
        print("No papers found. Try changing queries.")


if __name__ == "__main__":
    print(f"Searching for papers from {YEAR_START} to {YEAR_END}")
    print("Fields collected: Year, Authors, Title, Publication Venue, Findings/Abstract, DOI, URL, Citations, Keywords, Study Type")
    print("\n" + "="*80 + "\n")
    
    # Change pages to get more results per query
    run_search(
        per_query=30,
        semantic_pages=3,   # 3 pages => 90 results per query from Semantic Scholar
        crossref_pages=2,   # 2 pages => 60 results per query from Crossref
        pubmed_pages=2,     # 2 pages => 60 results per query from PubMed
        sleep_sec=1.0       # Be respectful to APIs
    )
