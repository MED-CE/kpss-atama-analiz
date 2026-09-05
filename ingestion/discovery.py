import httpx
from bs4 import BeautifulSoup
import logging
import re
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OSYM_ARCHIVE_URL = "https://www.osym.gov.tr/SinavGrubu/Menu/338"
OSYM_BASE_URL = "https://www.osym.gov.tr"

async def discover_placement_periods() -> List[Dict]:
    """
    Scrapes OSYM KPSS archive page to find placement periods.
    Returns a list of dictionaries with year, period, title, and url.
    """
    # OSYM sometimes has SSL issues or requires specific headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(OSYM_ARCHIVE_URL, timeout=10.0)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch OSYM archive: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    periods = []
    
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        
        # Regex to find something like "2024/1", "2023/2", etc.
        match = re.search(r'(20\d{2})/(\d+)', text)
        if match and "KPSS" in text:
            year = int(match.group(1))
            period = match.group(2)
            
            full_url = href if href.startswith('http') else f"{OSYM_BASE_URL}{href}"
            
            periods.append({
                "year": year,
                "period": period,
                "title": text,
                "url": full_url
            })
            
    return periods

if __name__ == "__main__":
    import asyncio
    
    async def main():
        periods = await discover_placement_periods()
        for p in periods:
            print(p)
            
    asyncio.run(main())
