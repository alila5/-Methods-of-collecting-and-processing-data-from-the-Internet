# -*- coding: utf-8 -*-
import re
import json
from scrapy.http import HtmlResponse
import scrapy
from urllib.parse import urlencode
from gbparse.items import  InstagramItem

HASHES = {
    'followers': 'c76146de99bb02f6415203be841dd25a',
    'following': 'd04b0a864b4b54837c0d870b0e77e076',
    'media': '58b6785bea111c67129decbe6a448951',
    'media_comments': '97b41c52301f77ce508f55e66d17620e',
    'likes': 'd5d763b1e2acf209d62d22d184488e57',
    'tags': '174a5243287c5f3a7de741089750ab3b',

}

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'adam666.1'
    insta_user_email = 'adamsemyanov1@yandex.ru'
    inst_passw = 'adamsemyanov'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'irenbyki'  #gefestart
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    user_data_hash = 'c9100bf9110dd6361671f113dd02e7d6'

    def parse(self, response: HtmlResponse):
        respons = response
        csrf_token = self.fetch_csrf_token(response.text)
        #csrf_token = csrf_token.replace(csrf_token[0],'W')
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_user_email, 'password': self.inst_passw},
            headers={'X-CSRFToken': csrf_token}
        )


    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_followers_parse,
                cb_kwargs={'username': self.parse_user}
            )



    #QVFCVjNkbU8tZDNMTWhsbTNmaW9XcjN6bkN1SEE2eXFTRjkzbkxmejFiblFYRWRYanNSekZ6eUk3Rmxfc3M0bVM3aUhOOVpBTFQzTk80a3dMRWIwT2d4Ug
    #QVFCTi00bWNjbkRZQkFZUi1KcFdVOG1MWUw1MmlsQk45V2hySDhfOXVIbDFmVDFaQU53Qi1YLUd1OXBmbjJ3NUI5TUhMb1BfZzlBNG1hY01YYWFubGx2Tw

    def user_followers_parse(self, response: HtmlResponse, username):
        self.user_id = self.fetch_user_id(response.text, username)
        query_followers_hash = HASHES['followers']
        #variables: {"id":"4713930173","include_reel":true,"fetch_mutual":true,"first":24}
        varibles = {
            'id': self.user_id,
            "include_reel": True,
            "fetch_mutual": True,
            "first": 24
        }

        url = f'{self.graphql_url}query_hash={query_followers_hash}&{urlencode(varibles)}'

        #data = response.xpath("//script[contains(., 'window._sharedData =')]/text()").extract_first()
        #j_data = json.loads(data[21:-1])
        #with open("1.json", "w", encoding="utf-8") as file:
          #  json.dump(j_data, file)
        yield response.follow(
            url,
            callback=self.followers_data_parse,
            cb_kwargs={'username': username}
        )



    def followers_data_parse(self, response: HtmlResponse, username):
        j_folower_data = json.loads(response.text)
        with open("2.json", "w", encoding="utf-8") as file:
            json.dump(j_folower_data, file)
        after_hash = j_folower_data['data']['user']['edge_followed_by']['page_info']['end_cursor']
        print(after_hash)
        for node in j_folower_data['data']['user']['edge_followed_by']['edges']:
            print(node)
            follower_info = node['node']
            _id = node['node']['username']
            yield InstagramItem(_id = _id, follower_info = follower_info)
        if j_folower_data['data']['user']['edge_followed_by']['page_info']['has_next_page'] == True:
            query_followers_hash = HASHES['followers']
            varibles = {
                'id': self.user_id,
                "include_reel": True,
                "fetch_mutual": True,
                "first": 24,
                "after": after_hash
            }

            url = f'{self.graphql_url}query_hash={query_followers_hash}&{urlencode(varibles)}'
            yield response.follow(
                url,
                callback=self.followers_data_parse,
                cb_kwargs={'username': username}
            )

    def userdata_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        varibles = {
            'user_id': user_id,
            "include_chaining": True,
            "include_reel": True,
            "include_logged_out_extras": False,
        }
        url = f'{self.graphql_url}query_hash={self.user_data_hash}&{urlencode(varibles)}'
        #data = response.xpath("//script[contains(., 'window._sharedData =')]/text()").extract_first()
        #j_data = json.loads(data[21:-1])
        #with open("1.json", "w", encoding="utf-8") as file:
          #  json.dump(j_data, file)
        yield response.follow(
            url,
            callback=self.user_data,
            cb_kwargs={'username': username}
        )

    def user_data(self, response: HtmlResponse, username):
        j_user_data = json.loads(response.text)
        with open("2.json", "w", encoding="utf-8") as file:
            json.dump(j_user_data, file)
        print(1)
        for node in j_user_data['data']['user']['edge_chaining']['edges']:
            userinfo = node['node']
            _id = node['node']['username']
            yield InstagramItem(_id = _id, userinfo=userinfo)




    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text)
        matched =matched.group()
        res = matched.split(':').pop()
        res = res.replace(r'"', '')
        return res


    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

