import argparse
import bisect
import os
import re
import requests
from bs4 import BeautifulSoup

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

def process_arxiv_id(arxiv_id, completed_ids):
  if arxiv_id in completed_ids:
    print(f"Already downloaded: {arxiv_id}")
  else:
    title = extract_title_from_arxiv(arxiv_id)
    if title:
      if(download_arxiv_pdf(arxiv_id, title)):
        bisect.insort(completed_ids, arxiv_id)
        return True
    else:
      print(f"Error retrieving title for: {arxiv_id}")
  return False

arxiv_ids_file_path = 'arxiv_ids.txt'
completed_ids_file_path = 'completed_ids.txt'

parser = argparse.ArgumentParser(description='Download papers from arXiv.')
parser.add_argument('-f', '--file', metavar='file', type=str, default=arxiv_ids_file_path, help='path to a file containing arXiv IDs.')
parser.add_argument('-i', '--ids', metavar='ids', nargs='+', type=str, help='list of arXiv IDs')

args = parser.parse_args()

with open(completed_ids_file_path, 'r') as file:
  completed_ids = file.read().split()

arxiv_ids = []

if args.ids:
  arxiv_ids = args.ids
elif args.file:
  with open(args.file, 'r') as file:
    arxiv_ids = file.read().split()

ids_added = 0
for arxiv_id in arxiv_ids:
  if process_arxiv_id(arxiv_id, completed_ids):
    ids_added += 1

if ids_added > 0:
  with open(completed_ids_file_path, 'w') as file:
    for arxiv_id in completed_ids:
      file.write(arxiv_id + '\n')
