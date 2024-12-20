
import requests
import os
from urllib.parse import urlparse, unquote
from pathlib import Path
import time

def download_pdf(url, output_dir='downloaded_pdfs', filename=None):
    """
    Download a PDF from a given URL and save it to the specified directory.
    
    Args:
        url (str): The URL of the PDF to download
        output_dir (str): Directory to save the PDFs (default: 'downloaded_pdfs')
        filename (str): Optional custom filename for the PDF
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Make the request with a timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check if the content is actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'application/pdf' not in content_type:
            print(f"Warning: URL {url} might not be a PDF (Content-Type: {content_type})")
        
        # Generate filename if not provided
        if not filename:
            # Try to get filename from Content-Disposition header
            if 'Content-Disposition' in response.headers:
                content_disp = response.headers['Content-Disposition']
                if 'filename=' in content_disp:
                    filename = content_disp.split('filename=')[1].strip('"')
            
            # If still no filename, extract it from URL
            if not filename:
                parsed_url = urlparse(url)
                filename = unquote(os.path.basename(parsed_url.path))
                
            # If filename is still empty or doesn't end with .pdf
            if not filename or not filename.endswith('.pdf'):
                filename = f"document_{int(time.time())}.pdf"
        
        # Ensure filename ends with .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Create full file path
        filepath = os.path.join(output_dir, filename)
        
        # Download and save the file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Successfully downloaded: {filename}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error downloading {url}: {str(e)}")
        return False

def download_pdfs_from_list(urls, output_dir='downloaded_pdfs', delay=1):
    """
    Download PDFs from a list of URLs with a delay between downloads.
    
    Args:
        urls (list): List of URLs to download PDFs from
        output_dir (str): Directory to save the PDFs
        delay (int): Delay in seconds between downloads
    
    Returns:
        tuple: (successful_downloads, failed_downloads)
    """
    successful = []
    failed = []
    
    for url in urls:
        success = download_pdf(url.strip(), output_dir)
        if success:
            successful.append(url)
        else:
            failed.append(url)
        
        # Wait before next download to be polite to servers
        if delay > 0:
            time.sleep(delay)
    
    return successful, failed

# Example usage:
if __name__ == "__main__":
    # List of URLs to download PDFs from
    pdf_urls = [ "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2011.pdf",
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2012.pdf",  
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2013.pdf",  
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2014.pdf",  
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2015.pdf",  
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2016.pdf", 
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_annuel_sfbt_2017.pdf", 
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_sfbt_2018.pdf", 
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_du_conseil_dadministration_sfbt_2018.pdf", 
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_sfbt_2019.pdf",   
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_sfbt_2020.pdf",   
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_sfbt_2021.pdf",   
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/sfbt_rapport_annuel_de_gestion31-12-2022.pdf",   
  "https://www.cmf.tn/sites/default/files/pdfs/emetteurs/informations/rapports-societes/rapport_sfbt_2023.pdf"]
    
    # Download the PDFs
    successful, failed = download_pdfs_from_list(pdf_urls)
    
    # Print summary
    print("\nDownload Summary:")
    print(f"Successfully downloaded: {len(successful)} PDFs")
    print(f"Failed downloads: {len(failed)} PDFs")
    
    while len(failed) != 0:
        print("\nFailed URLs:")
        for url in failed:
            print(f"- {url}")
        successful, failed = download_pdfs_from_list(failed)



 
