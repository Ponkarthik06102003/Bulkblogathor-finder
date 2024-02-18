import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_author_details(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    author_name_elem = soup.find('span', class_='author-name')
    author_email_elem = soup.find('span', class_='author-email')
    author_profile_elem = soup.find('a', href=True, string='author Profile')
    author_image_elem = soup.find('img', class_='author-image')
    blog_logo_elem = soup.find('img', class_='blog-logo')
    blog_name_elem = soup.find('h1', class_='blog-name')

    author_name = author_name_elem.text.strip() if author_name_elem else ''
    author_email = author_email_elem.text.strip() if author_email_elem else ''
    author_profile = author_profile_elem['href'] if author_profile_elem else ''
    author_image = author_image_elem['src'] if author_image_elem else ''
    blog_logo = blog_logo_elem['src'] if blog_logo_elem else ''
    blog_name = blog_name_elem.text.strip() if blog_name_elem else ''

    return author_name, author_email, author_profile, author_image, blog_logo, blog_name


def get_author_details_from_search(query):
    search_url = f'https://www.google.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    search_results = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(search_results.text, 'html.parser')
    search_results = soup.find_all('div', class_='g')
    author_details = []

    for result in search_results:
        link_elem = result.find('a')
        if not link_elem:
            continue
        link = link_elem['href']
        if 'http' not in link:
            continue
        try:
            author_name, author_email, author_profile, author_image, blog_logo, blog_name = get_author_details(link)
            author_details.append({
                'Blog URL': link,
                'Author Name': author_name,
                'Author Email': author_email,
                'Author Profile Link': author_profile,
                'Author Image': author_image,
                'Blog Logo': blog_logo,
                'Blog Name': blog_name
            })
        except:
            pass
    return author_details


def main():
    def get_urls():
        urls = []
        while True:
            url = input("Enter a URL (or 'done' to finish): ")
            if url == 'done':
                break
            urls.append(url)
        return urls
    # example usage
    urls = get_urls()
    author_details = []
    for url in urls:
        query = f'site:{url}'
        author_details += get_author_details_from_search(query)
    df = pd.DataFrame(author_details)
    df.to_excel('author_details.xlsx', index=False)
    print(f"Data saved in 'author_details1.xlsx' file.")


if __name__ == '__main__':
    main()


