import os
import re
import requests
from bs4 import BeautifulSoup
import bisect

papers_dir = 'arxiv_papers/'

if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)

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
    
    with open(f'{papers_dir}{pdf_filename}', "wb") as file:
      file.write(response.content)
    print(f"Downloaded: {pdf_filename}")
    return True
  else:
    print(f"Error downloading: {arxiv_id}")
    return False

def process_arxiv_ids_file(file_path, completed_file_path):
  with open(file_path, 'r') as file:
    arxiv_ids = file.read().split()
    
  with open(completed_file_path, 'r') as file:
    completed_ids = file.read().split()

  to_process_ids = []
  for arxiv_id in arxiv_ids:
    if arxiv_id in completed_ids:
      print(f"Already downloaded: {arxiv_id}")
    else:
      to_process_ids.append(arxiv_id)

  for arxiv_id in to_process_ids:

    title = extract_title_from_arxiv(arxiv_id)
    if title:
      if(download_arxiv_pdf(arxiv_id, title)):
        bisect.insort(completed_ids, arxiv_id)
    else:
      print(f"Error retrieving title for: {arxiv_id}")
      
  with open(completed_file_path, 'w') as file:
    for id in completed_ids:
      file.write(id + '\n')

  with open(file_path, 'w') as file:
    for id in to_process_ids:
      file.write(id + '\n')

arxiv_ids_file = 'arxiv_ids.txt'
completed_ids_file = 'completed_ids.txt'
process_arxiv_ids_file(arxiv_ids_file, completed_ids_file)