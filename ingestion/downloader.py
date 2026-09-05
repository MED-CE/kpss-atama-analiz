import httpx
from bs4 import BeautifulSoup
import logging
import urllib.parse
from typing import List, Dict

logger = logging.getLogger(__name__)

async def fetch_document_links(period_url: str) -> List[Dict]:
    """
    Fetches the specific placement period page and extracts links to PDFs and Excel files.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(period_url, timeout=15.0)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch period details from {period_url}: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = "https://www.osym.gov.tr"
    
    documents = []
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()
        
        # Look for PDF or Excel files
        if href.lower().endswith('.pdf') or href.lower().endswith('.xls') or href.lower().endswith('.xlsx'):
            full_url = href if href.startswith('http') else urllib.parse.urljoin(base_url, href)
            
            doc_type = "UNKNOWN"
            if "nitelik" in text or "kosul" in text or "koşul" in text:
                doc_type = "QUALIFICATIONS"
            elif "kadro" in text or "pozisyon" in text or "yerleştirme" in text or "sonuç" in text or "max" in text or "min" in text:
                doc_type = "PLACEMENTS"
                
            documents.append({
                "url": full_url,
                "title": a.get_text(strip=True),
                "type": doc_type
            })
            
    return documents

async def download_file(url: str) -> bytes | None:
    """
    Downloads the file from the given URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Failed to download file from {url}: {e}")
            return None
