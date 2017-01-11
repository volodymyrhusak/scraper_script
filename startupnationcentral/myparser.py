# from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import json
import csv

class Parser:

    def __init__(self, url):
        self.url = 'http://' + url
        request = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        html = request.text
        self.soup = BeautifulSoup(html, 'html.parser')

        # helper variables
        self.team = self._get_team()
        self.similar_companies = self._get_similar_company(self.url)

    def get_company_name(self):
        return self.soup.find('h1', class_="company__title page-title").text

    def get_company_short_description(self):
        result = self.soup.find('div', class_='company__short-description')
        return self._get_pure_text(result.text)

    def get_company_description(self):
        result = self.soup.find('div', class_="company__description")
        return self._get_pure_text(result.text)

    def get_homepage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Homepage') != -1:
                return li.find('a').get('href')
        return ''

    def get_sector(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Sector') != -1:
                return li.find('a').text
        return ''

    def get_founded(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Founded') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_business_model(self):
        bm = list()
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Business Model') != -1:
                for a in li.find_all('a'):
                    bm.append(a.text)
                return ', '.join(bm)
        return ''

    def get_funding_stage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Funding Stage') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_amount_raised(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Amount Raised') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_employees(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Employees') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_products(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Products') != -1:
                result = li.find('div', class_="company-parameters__value")
                return self._get_pure_text(result.text, ',')
        return ''

    def get_product_stage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Product Stage') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_patent(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Patent') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_geographical_markets(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Geographical Markets') != -1:
                result = li.find('div', class_="company-parameters__value")
                return self._get_pure_text(result.text, ',')
        return ''

    def get_tags(self):
        tags = list()
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Tags') != -1:
                for tag in li.find_all('a', class_="tags__tag "):
                    tags.append(tag.text)
                return ', '.join(tags)
        return ''

    def get_target_markets(self):
        tags = list()
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Target Markets') != -1:
                for tag in li.find_all('a', class_="tags__tag "):
                    tags.append(tag.text)
                return ', '.join(tags)
        return ''

    def get_address(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Address') != -1:
                result = li.find('div', class_="company-parameters__value")
                return self._get_pure_text(result.text)
        return ''

    def get_offices_abroad(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Offices abroad') != -1:
                return li.find('div', class_="company-parameters__value").text
        return ''

    def get_tim_member_1(self):
        return self._get_team()[0]

    def get_tim_member_2(self):
        return self._get_team()[1]

    def get_tim_member_3(self):
        return self._get_team()[2]

    def get_funding_rounds(self):
        rounds = ''
        for i in self.soup.find_all('div', class_='company-fundings__one'):
            try:
                result = ''
                funding_type = i.find('h3', class_='company-fundings__round round__data').text
                funding_sum = i.find('span', class_='company-fundings__sum-currency round__data').text
                funding_date = i.find('p', class_="company-fundings__date round__data").text
                funding_investors = list()
                for investor in i.find_all('li', class_='company-fundings__investor round__data'):
                    funding_investors.append(self._get_pure_text(investor.text))

                # print(self._get_pure_text(funding_investors))

                if self._get_pure_text(funding_type):
                    result = self._get_pure_text(funding_type) + ', '
                if self._get_pure_text(funding_sum):
                    result = result + self._get_pure_text(funding_sum) + ', '
                if self._get_pure_text(', '.join(funding_investors)):
                    result = result + ', '.join(funding_investors) + ', '
                if self._get_pure_text(funding_date):
                    result += funding_date
                rounds = rounds + result.strip(', ') + '\n'
            except:
                pass

        return rounds

    def get_facebook(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('facebook.com') != -1:
                return l.get('href')
        return ''

    def get_twitter(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('twitter.com') != -1:
                return l.get('href')
        return ''

    def get_linkedin(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('linkedin.com') != -1:
                return l.get('href')
        return ''

    def get_similar_company_1(self):
        return self.similar_companies[0]

    def get_similar_company_2(self):
        return self.similar_companies[1]

    def get_similar_company_3(self):
        return self.similar_companies[2]

    def get_url_source(self):
        return self._get_pure_text(self.url)

    ### helper methods ###
    def _get_team(self):
        team = ['', '', '']
        try:
            company_team = self.soup.find('div', class_='company-team')
            for i, person in enumerate(company_team.find_all('div', class_='company-team__info')):
                name = person.find('div', class_='company-team__name').get_text()
                position = person.find('div', class_='company-team__position').get_text()
                team[i] = name + ', ' + position
        finally:
            return team

    def _get_similar_company(self, link):
        similar_urls = ['', '', '']
        try:
            company = link.split('/')[-1]
            link = 'http://finder.startupnationcentral.org/similar/' + company
            request = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            json_data = request.text
            data = json.loads(json_data)
            for j, i in enumerate(data):
                similar_urls[j] = ('finder.startupnationcentral.org/c/' + i['url'])
        finally:
            return similar_urls

    def _get_pure_text(self, text, separator=None):
        text = str(text)
        if separator:
            text = text.split(separator)
            text = map(lambda x: x.replace('\n', ''), text)
            text = map(lambda x: x.strip(), text)
            separator += ' '
            return separator.join(text)
        else:
            text = text.replace('\n', '').strip()
            return text


if __name__ == '__main__':

    with open('startupnationcentralv.csv', 'r') as outcsv:
        new_rows_list = []
        new_col = []
        reader = csv.reader(outcsv)
        for i, row1 in enumerate(reader):
                if not row1[-2] and not row1[-3] and not row1[-4] :
                    link = row1[-1]

        new_rows_list = []
        for row in reader:
            if row[-1] == link:
                parser = Parser(link)
                row[-2] == parser.get_similar_company_1()
                row[-3] == parser.get_similar_company_2()
                row[-4] == parser.get_similar_company_3()
            for col in row:
                col.strip()
                new_col.append(col.strip())
            new_rows_list.append(new_col)


    with open('startupnationcentralv_1.csv', 'w') as outcsv_1:
          csv_writer =  csv.writer(outcsv_1)
          csv_writer.writerows([x for x in new_rows_list])











