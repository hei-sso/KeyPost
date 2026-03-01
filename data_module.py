import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords(num_keywords=10):
    keywords = []
    try:
        url = 'https://news.naver.com/main/ranking/popularDay.naver'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select('.list_title')
        
        for el in elements:
            title = el.text.strip()
            if title and title not in keywords:
                keywords.append(title)
            
            if len(keywords) >= num_keywords:
                break
                
    except Exception as e:
        print(f"크롤링 에러 발생: {e}")

    # 수집을 못 했으면 빈 리스트([]) 그대로 반환
    return keywords

def save_to_excel(data_list, filename="블로그_트렌드_수집결과.xlsx"):
    df = pd.DataFrame(data_list)
    df.to_excel(filename, index=False)

def save_blog_text(idx, safe_title, title, content):
    os.makedirs("블로그_결과물", exist_ok=True)
    file_name = f"블로그_결과물/{idx}번_{safe_title}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"제목: {title}\n")
        f.write(f"관련 이미지 파일: {idx}번_이미지_{safe_title}.png\n")
        f.write("-" * 30 + "\n\n")
        f.write(content)
    return file_name

def save_image(idx, safe_title, image_bytes):
    os.makedirs("블로그_결과물", exist_ok=True)
    image_filename = f"블로그_결과물/{idx}번_이미지_{safe_title}.png"
    with open(image_filename, "wb") as f:
        f.write(image_bytes)
    return image_filename
