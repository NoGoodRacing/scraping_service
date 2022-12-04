import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = "scraping_service.settings"

django.setup()
from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Рассылка вакансий на {today}'
text_content = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению новых вакансий нет</h2>'

User = get_user_model()
qs = User.objects.filter(send_mail=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'], i['language_id'])].append(i)
    # for keys, emails in users_dict.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
    #         html += f'<p>{row["description"]}</p>'
    #         html += f'<p>{row["company"]}</p><br><hr>'
    #     _html = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, "text/html")
    #         msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''

if qs.exists():
    error = qs.first()
    data = error.data
    for i in data:
        _html += f'<p><a href="{i["url"]}">Error:{i["title"]}</a></p>'
        subject = f'Ошибки скрапинга {today}'
        text_content = 'Ошибки скрапинга'

qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_err = ''
qs = User.objects.filter(send_mail=True).values('city', 'language')
users_dict = {(i['city'], i['language']): (i['city'], i['language']) for i in qs}
for i in users_dict:
    if i not in urls_dict.keys():
        urls_err += f'<p>Для {i[0]} и языка программирования {i[1]} отсутвуют url</p><br>'
if urls_err:
    subject += 'Отсутвующие url'
    _html += urls_err
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
