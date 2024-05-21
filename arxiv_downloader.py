import os
import re
import requests
from bs4 import BeautifulSoup

def extract_title_from_arxiv(arxiv_id):
  arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
  response = requests.get(arxiv_url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', class_='title')
    if title_element:
      return title_element.text.strip()
  return None

def download_arxiv_pdf(arxiv_id, title):
  base_url = "https://arxiv.org/pdf/"
  pdf_url = base_url + arxiv_id + ".pdf"
  
  response = requests.get(pdf_url)
  if response.status_code == 200:
    pdf_filename = re.sub(r'[^\w\-_\. ]', '_', title)
    pdf_filename = re.sub(r'_ ', ' ', pdf_filename)
    pdf_filename = re.sub(r'Title_', '', pdf_filename)
    pdf_filename += f" ({arxiv_id}).pdf"
    
    with open(pdf_filename, "wb") as file:
      file.write(response.content)
    print(f"Downloaded: {pdf_filename}")
    return True
  else:
    print(f"Error downloading: {arxiv_id}")
    return False

def process_arxiv_ids_file(file_path, completed_file_path):
  with open(file_path, 'r') as file:
    arxiv_ids = file.read().split()
      
  completed_ids = []
  
  for arxiv_id in arxiv_ids:
    title = extract_title_from_arxiv(arxiv_id)
    if title:
      if(download_arxiv_pdf(arxiv_id, title)):
        completed_ids.append(arxiv_id)
    else:
      print(f"Error retrieving title for: {arxiv_id}")
      
  with open(completed_file_path, 'a') as file:
    file.write('\n'.join(completed_ids) + '\n')

  remaining_ids = [arxiv_id for arxiv_id in arxiv_ids if arxiv_id not in completed_ids]
  with open(file_path, 'w') as file:
    file.write(' '.join(remaining_ids))

arxiv_ids_file = 'arxiv_ids.txt'
completed_ids_file = 'completed_ids.txt'
process_arxiv_ids_file(arxiv_ids_file, completed_ids_file)