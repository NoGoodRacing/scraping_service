import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import choice

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Safari/537.36 (Macintosh; Intel Mac OS X 10_15_5)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]

__all__ = ('work', 'dou', 'djinni')


def work(url, city=None, language=None):
    domain = 'https://www.work.ua'
    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            if main_div:
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append(
                        {'title': title.text, 'url': domain + href, 'description': description, 'company': company,
                         'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def dou(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id="vacancyListId")
            if main_div:
                div_list = main_div.find_all('div', attrs={'_id': True})
                for div in div_list:
                    title = div.find('a', attrs={'class': 'vt'})
                    href = div.a['href']
                    description = div.find('div', attrs={'sh-info'}).text
                    company = div.find('div', attrs={'class': 'title'}).find('a', attrs={'class': 'company'}).text
                    jobs.append({'title': title.text, 'url': href, 'description': description, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def djinni(url, city=None, language=None):
    domain = 'https://djinni.co'
    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url, headers=choice(headers))
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-unstyled list-jobs'})
            if main_ul:
                div_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item list__item'})
                for div in div_list:
                    title = div.find('div', attrs={'class': 'list-jobs__title list__title order-1'}).a.text
                    href = div.find('div', attrs={'class': 'list-jobs__title list__title order-1'}).a['href']
                    description = div.find('div', attrs={'class': 'list-jobs__description'}).p.text
                    company = div.find('div', attrs={'class': 'list-jobs__details__info'}).a.text
                    jobs.append(
                        {'title': title, 'url': domain + href, 'description': description, 'company': company.lstrip(),
                         'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == "__main__":
    url = 'https://djinni.co/jobs/?region=UKR&primary_keyword=Python&location=kyiv'
    jobs, errors = djinni(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
