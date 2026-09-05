import pandas as pd
import pdfplumber
import logging
import io

logger = logging.getLogger(__name__)

def parse_excel_placements(file_bytes: bytes) -> list:
    """
    Parses OSYM Excel files for Placement Quotas and Scores.
    Returns a list of dictionaries.
    """
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))
        
        # Find the header row (OSYM usually puts headers after some title rows)
        header_row_idx = None
        for i, row in df.iterrows():
            row_str = str(row.values).upper()
            if 'KONTENJAN' in row_str and ('KURUM' in row_str or 'KADRO' in row_str):
                header_row_idx = i
                break
                
        if header_row_idx is not None:
            df.columns = df.iloc[header_row_idx]
            df = df.iloc[header_row_idx+1:].dropna(how='all')
        
        # Clean column names
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        results = []
        for _, row in df.iterrows():
            # Convert row to dictionary, dropping NaN values
            row_dict = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
            if row_dict:
                results.append(row_dict)
            
        return results
    except Exception as e:
        logger.error(f"Excel parsing failed: {e}")
        return []

def parse_pdf_qualifications(file_bytes: bytes) -> dict:
    """
    Parses OSYM PDF files for Qualification Codes (Nitelik Kodları).
    Returns a dictionary mapping code -> description.
    """
    qualifications = {}
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                    
                lines = text.split('\n')
                for line in lines:
                    parts = line.strip().split(' ', 1)
                    if len(parts) == 2 and parts[0].isdigit() and len(parts[0]) == 4:
                        code = parts[0]
                        desc = parts[1].strip()
                        qualifications[code] = desc
        return qualifications
    except Exception as e:
        logger.error(f"PDF parsing failed: {e}")
        return {}
