import os
import re
import json
import time
import datetime
import execjs
import pymysql
import requests
import random
import easyocr
import schedule
from XhSReply import get_review

XHS_JSPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'CrawlerJs','xs.js')
XHS_JSCODE = open(XHS_JSPATH,'r',encoding='utf-8').read()
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
def load_config():
    with open(CURRENT_PATH+'/config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
#-----------------------------------ChinaProxies--------------------------------
config = load_config()
proxy_config = config['proxy']
TUNNEL = proxy_config['china']['host']+":"+str(proxy_config['china']['port'])
USERNAME = proxy_config['china']['username']
PASSWORD = proxy_config['china']['password']
ChinaProxies = {
    'http': 'http://%(user)s:%(pwd)s@%(proxy)s/' % {"user": USERNAME, "pwd": PASSWORD, "proxy": TUNNEL},
    'https': 'http://%(user)s:%(pwd)s@%(proxy)s/' % {"user": USERNAME, "pwd": PASSWORD, "proxy": TUNNEL},
}
#-----------------------------------Database--------------------------------
db_config = config['database']['mysql']
pool = pymysql.connect(
host=db_config['host'],
port=db_config['port'],
user=db_config['user'],
password=db_config['password'],
db=db_config['db_name'],
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor
)
#-----------------------------------Params--------------------------------
params_config = config['params']
cookie = params_config['cookie']
xtoken = params_config['xtoken']
push_comment_cookie = "loadts=1746876271992;xsecappid=xhs-pc-web;x-user-id-creator.xiaohongshu.com=5decbaf600000000010076c2;websectiga=9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8;galaxy_creator_session_id=hFEAs7rVmv6wWwlNmYbv8MkcsM1dUBuRiLse;webBuild=4.62.3;galaxy.creator.beaker.session.id=1745225365165038850925;sec_poison_id=639c9ba6-eaae-444c-ba7b-1cdb02c2ab32;web_session=0400698c98f9be562694dfe4c9354bff682c35;gid=yj2W48iJy4fdyj2W48iyK0E88qqY9k8I3Yq838DMjFiWjU28x006MJ888qj44YW88f2KijdY;a1=195740f160338tg0ni830s9rf79haamsdaip2w00b50000394487;abRequestId=2d32661b-6aa9-5e48-bf44-66ab6e143d7a;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517495685867242309415g2rneojb9bmxhfxd;customerClientId=127441548027406;unread={%22ub%22:%2267fbb59b0000000009015ccc%22%2C%22ue%22:%22681dc8d2000000002102c52d%22%2C%22uc%22:46};webId=36127434f2306c19db7a20f19c7f2f4f"
#-----------------------------------GlobalProxies--------------------------------
global_proxy_config = config['proxy']['global']
GLOBAL_PROXY = {
    'http': 'http://'+global_proxy_config['host']+":"+str(global_proxy_config['port']),
    'https': 'http://'+global_proxy_config['host']+":"+str(global_proxy_config['port']),
}
def XhsA1():
    data = execjs.compile(XHS_JSCODE).call('a1')
    return data
class XhsWebApi:
    def __init__(self) -> None:
        self.comment_list = []
        self.collect_dict = {
            '6756325e0000000031002468':'Top',
            '67563254000000003100ada4':'BBW',
            '6756323e0000000030010fbe':'紫色异味',
            '67562c2c000000003100c124':'纯',
            '67562c5400000000300074e1':'愈',
            '67562c48000000003003cf09':'欲',
            '67562b9a00000000300374c8':'knowledge',
        }
        self.subcommnet_list = []
        self.cookie = cookie
    def requests_rewrite(self,method,**kwargs):
        all = 0
        errinfo = ''
        while all <= 3:
            try:
                print(all)
                all += 1
                response = requests.get(**kwargs)
                if str(method).upper() == 'POST':
                    response = requests.post(**kwargs)
                return response
            except Exception as e:
                print('requests_rewritez--error',all,e)
        return {'error':errinfo}
    def response_parse(self,response, *args):
      try:
        error_key = ''
        for i in args:
          error_key = i
          response = response[i]
        return response
      except KeyError as e:
        print('{}中没有键{}'.format(response,error_key))
        return None
    def generate_param(self,cookie,*params):
        data = execjs.compile(XHS_JSCODE.replace('mycookie',cookie)).call('x_s',*params)
        return (data['x-s'],data['x-t'],data['x-common'])
    def blog_detail(self,noteid,xtoken=''): 
        noteid = str(noteid).strip()
        try:
            info_data = {
                'source_note_id': noteid,
                'image_formats': [
                    'jpg',
                    'webp',
                    'avif',
                ],
                'extra': {
                    'need_body_topic': '1',
                },
                'xsec_source': 'pc_cfeed',
                'xsec_token': xtoken,
            }
            xs,xt,xc = self.generate_param(self.cookie,'/api/sns/web/v1/feed', info_data)
            info_url = 'https://edith.xiaohongshu.com/api/sns/web/v1/feed'
            headers = {
                'cookie': self.cookie,
                "content-type": "application/json;charset=UTF-8",
                "referer": "https://www.xiaohongshu.com/",
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                "X-S": xs,
                'X-s-COMMON':xc,
                'X-T':str(xt)}

            response = self.requests_rewrite(method='post',url=info_url,headers=headers,
                                         data=json.dumps(info_data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
          
            if response.status_code != 200:
                print('初始小红书cookie状态监测', noteid, response,response.text)
                print('x-s长度为:',len(xs),'x-common长度为:',len(xc))
                return self.blog_detail(noteid,xtoken)

            print('最终小红书cookie状态监测', noteid, response)
            if "笔记不存在" == response.json()['msg']:
                return {'image_url': None,
                    'liked_count': 0,
                    'comment_count': 0,
                    'collected_count': 0,
                    'username': None,
                    'userid': None,
                    'share_count': 0,
                    'last_update_time': None,
                    'push_time': None}
            response = response.json()['data']['items'][0]['note_card']
            title = self.response_parse(response,'title')
            description = self.response_parse(response,'desc')
            image_url = self.response_parse(response,'image_list',0,'url_default')
            liked_count = self.response_parse(response,'interact_info','liked_count')
            if liked_count is not None:
                if "万" in liked_count:
                    liked_count = int(float(str(liked_count).replace("万",""))*10000)
                elif "千" in liked_count:
                    liked_count = int(float(str(liked_count).replace("千",""))*1000)
            
            comment_count = self.response_parse(response,'interact_info','comment_count')
            if comment_count is not None:
                if "万" in comment_count:
                    comment_count = int(float(str(comment_count).replace("万",""))*10000)
                elif "千" in comment_count:
                    comment_count = int(float(str(comment_count).replace("千",""))*1000)
            
            collected_count = self.response_parse(response,'interact_info','collected_count')
            if collected_count is not None:
                if "万" in collected_count:
                    collected_count = int(float(str(collected_count).replace("万",""))*10000)
                elif "千" in collected_count:
                    collected_count = int(float(str(collected_count).replace("千",""))*1000)
           
            share_count = self.response_parse(response,'interact_info','share_count')
            if share_count is not None:
                if "万" in share_count:
                    share_count = int(float(str(share_count).replace("万",""))*10000)
                elif "千" in share_count:
                    share_count = int(float(str(share_count).replace("千",""))*1000)
            
            last_update_time = self.response_parse(response,'last_update_time')
            if last_update_time is not None:
                last_update_time = datetime.datetime.fromtimestamp(int(last_update_time) / 1000)
            push_time = self.response_parse(response,'time')
            if push_time is not None:
                push_time = datetime.datetime.fromtimestamp(int(push_time) / 1000)
            username = self.response_parse(response,'user','nickname')
            userid = self.response_parse(response,'user','user_id')
            print({'image_url': image_url,
                    'liked_count': liked_count,
                    'comment_count': comment_count,
                    'collected_count': collected_count,
                    'share_count': share_count,
                    'username': username,
                    'userid': userid,
                    'last_update_time': last_update_time,
                    'push_time': push_time,
                    'title': title,
                    'description': description})
            return {'image_url': image_url,
                    'liked_count': liked_count,
                    'comment_count': comment_count,
                    'collected_count': collected_count,
                    'share_count': share_count,
                    'last_update_time': last_update_time,
                    'push_time': push_time,
                    'username': username,
                    'userid': userid,
                    'title': title,
                    'description': description}
        
        except Exception as e:
            print(f'查询小红书帖子数据{noteid}报错', e)
            if 'item' in str(e):
                return self.blog_detail(noteid,xtoken)
            return {'image_url': None,
                    'liked_count': None,
                    'comment_count': None,
                    'collected_count': None,
                    'username': None,
                    'userid': None,
                    'share_count': None,
                    'last_update_time': None,
                    'push_time': None}
    def parseComment(self,comment, Onesorts, Secsorts):
        CommentDict = {}
        CommentDict['NoteId'] = comment["note_id"]
        CommentDict['ColTime'] = str(datetime.datetime.now())
        CommentDict['CommentText'] = comment["content"]
        CommentDict['CommentLike'] = comment["like_count"]
        if '万' in str(CommentDict['CommentLike']):
            CommentDict['CommentLike'] = str(CommentDict['CommentLike'])
        CommentDict['CommentId'] = comment['id']
        CommentDict['CommentSort'] = Secsorts
        CommentDict['CommentTime'] = str(datetime.datetime.fromtimestamp(int(comment['create_time']) / 1000))
        CommentDict['CommentUserId'] = comment['user_info']['user_id']
        CommentDict['CommentUserName'] = comment['user_info']['nickname']
        try:
            CommentDict['CommentTarget'] = comment['target_comment']['id']
        except Exception as e:
            CommentDict['CommentTarget'] = None
        CommentDict['CommentImg'] = comment.get('pictures')
        CommentDict['Commenttag'] = str(Onesorts) + '-' + str(Secsorts)
        if CommentDict['CommentImg']:
            CommentDict['CommentImg'] = CommentDict['CommentImg'][0]['url_default']
        else:
            CommentDict['CommentImg'] = None
        try:
            CommentDict['CommentIp'] = comment['ip_location']
        except Exception as e:
            CommentDict['CommentIp'] = ''

        with open('comment', 'a', encoding='utf-8') as f:
            f.write(json.dumps(CommentDict,ensure_ascii=False))
            f.write('\n')

        return CommentDict
 
    def blog_comment(self,noteid,xsec_token, cursor='', Onesorts=0,cookie1=''):
        # a1 = XhsA1()
        # cookie = c.unlogin_cookie(a1)
        # if Onesorts:
        cookie =cookie1
        result = []
        xs, xt, xc = self.generate_param(cookie, f'/api/sns/web/v2/comment/page?note_id={noteid}&cursor={cursor}&top_comment_id=&image_formats=jpg,webp,avi&xsec_token={xsec_token}', None)
        url = f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={noteid}&cursor={cursor}&top_comment_id=&image_formats=jpg,webp,avi&xsec_token={xsec_token}'
        headers = {
        'cookie': cookie,
        "content-type": "application/json;charset=UTF-8",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "X-S": xs,
        'X-s-COMMON': xc
        }
        response = self.requests_rewrite('GET',url=url, headers=headers, proxies=GLOBAL_PROXY)
        time.sleep(8)
        try:
            response = response.json()  # 指定编码为 UTF-8
            response = response['data']
            print(id,response,Onesorts)
        except UnicodeDecodeError as e:
            print(f"解码失败: {e}")
            return
        if 'comments' in response:
            comments = response['comments']
        else:
            return
        Secsorts = 0
        for comment in comments:
            Secsorts += 1
            sub_comment_cursor = comment['sub_comment_cursor']
            CommentId = comment['id']
            result.append(self.parseComment(comment, Onesorts + Secsorts, 0))
            comment = comment['sub_comments']
            if comment:
                result.append(self.parseComment(comment[0], Onesorts + Secsorts, 1))
        has_more = response['has_more']
        cursor = response['cursor']
        if has_more and Onesorts<30:
            Onesorts += 10
        
            return self.blog_comment(noteid,xsec_token, cursor, Onesorts, cookie1)
    def author(self):
        pass
    def search(self,keywords,page):
        result = []
        keyword = keywords
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        
        data = {"keyword": keyword, "page": page, "page_size": 20, "search_id": "2dxn7d4e4grk2mjlnkzsh", "sort": "time_descending", "note_type": 0, "ext_flags": [], "image_formats": ["jpg", "webp", "avif"]}
        xs,xt,xc = self.generate_param(self.cookie,'/api/sns/web/v1/search/notes', data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.cookie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode('utf-8'), proxies=GLOBAL_PROXY)
        response = response.json()
        page = data['page']
        keyword = data['keyword']
        if response.get('data', {}).get('items'):
            items = response['data']['items']
            _sort_ = 0
            for item in items:
                _sort_ += 1
                SearchDicts = {}
                SearchDicts['NoteId'] = item['id']
                # if '#' not in SearchDicts['NoteId']:
                #     self.blog_comment(item['xsec_token'],item['id'], pool)
                SearchDicts['Format'] = item['model_type']
                SearchDicts['Sort'] = (page - 1) * 20 + _sort_
                SearchDicts['Keyword'] = keyword
                SearchDicts['Xtoken'] = item['xsec_token']
                SearchDicts['Coltime'] = datetime.datetime.now()
                result.append(SearchDicts)
        return result

    def blog_sub_comment(self):
        pass
    def blog_like(self,noteid):
        data ={"note_oid":noteid}
        xs, xt, xc = self.generate_param(self.cookie, f'/api/sns/web/v1/note/like',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.cookie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/like"
       
       
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
    def comment_like(self,noteid,commentid):
        data ={"note_id":noteid,"comment_id":commentid}
        coo = 'loadts=1745487369095;xsecappid=xhs-pc-web;acw_tc=0a00d39c17454863781634146e77d0e1b8bd5ba44762cbdd5700fda35edd40;x-user-id-creator.xiaohongshu.com=5decbaf600000000010076c2;websectiga=f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0;galaxy_creator_session_id=hFEAs7rVmv6wWwlNmYbv8MkcsM1dUBuRiLse;webBuild=4.62.3;galaxy.creator.beaker.session.id=1745225365165038850925;sec_poison_id=bf6efecb-d4ce-4840-a89f-df9c66e4a583;web_session=0400698c98f9be562694dfe4c9354bff682c35;gid=yj2W48iJy4fdyj2W48iyK0E88qqY9k8I3Yq838DMjFiWjU28x006MJ888qj44YW88f2KijdY;a1=195740f160338tg0ni830s9rf79haamsdaip2w00b50000394487;abRequestId=2d32661b-6aa9-5e48-bf44-66ab6e143d7a;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517495685867242309415g2rneojb9bmxhfxd;customer-sso-sid=68c517495685867242309412soxj8b6qjyocju4a;customerClientId=127441548027406;unread={%22ub%22:%2268011c05000000001c02dbff%22%2C%22ue%22:%226809db2c000000001c0036d7%22%2C%22uc%22:22};webId=36127434f2306c19db7a20f19c7f2f4f'

        xs, xt, xc = self.generate_param(coo, f'/api/sns/web/v1/comment/like',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": coo,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/like"
       
       
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
    def move_collect(self,boardid,noteid):
        data ={"target_board_id":boardid,"notes_id":noteid}
        xs, xt, xc = self.generate_param(self.cookie, f'/api/sns/web/v1/note/move',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.cookie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/move"
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
    def blog_collect(self,noteid):
        data ={"note_id":noteid}
        xs, xt, xc = self.generate_param(self.cookie, f'/api/sns/web/v1/note/collect',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.cookie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/collect"
       
    
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                        data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                        .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
    def author_follow(self,userid):
        data = {"target_user_id":userid}
        xs, xt, xc = self.generate_param(self.cookie, f'/api/sns/web/v1/user/follow',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.cookie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/user/follow"
       
       
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
    def push_newblog(self):
        pass
    def message_list(self):
        pass
    def detele_comment(self,noteid,comment_id,cookiie):
        
        data = {"note_id":noteid,"comment_id":comment_id}
        xs, xt, xc = self.generate_param(cookiie, f'/api/sns/web/v1/comment/delete',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": cookiie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/delete"
       
       
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
        time.sleep(5)
    def push_comment(self,noteid,content,cookiie):
        
        data = {"note_id":noteid,"content":content,"at_users":[],"target_comment_id": "682aaf590000000009014b9f"}
        xs, xt, xc = self.generate_param(cookiie, f'/api/sns/web/v1/comment/post',data)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "cookie": cookiie,
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "x-s": xs,
            "x-s-common": xc,}
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/post"
       
       
        response = self.requests_rewrite(method='post',url=url,headers=headers,
                                         data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'),proxies = GLOBAL_PROXY)
        print(response)
        print(response.text)
        time.sleep(5)
        # return response.json()['data']["comment"]['id']
    def unlogin_cookie(self,a1):
        cookie = f'webBuild=4.43.0;a1={a1};webId=1fb17a90d762193f8d2140ad3c31a1{str(random.randint(1,9))}{str(random.randint(1,9))};xsecappid=xhs-pc-web'
        xs,xt,xc = self.generate_param(cookie,"/api/sns/web/v1/login/activate",{})
        headers = {
        'cookie':cookie,
        "content-type": "application/json;charset=UTF-8",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        "X-S": xs,
        'X-s-COMMON':xc,

    }   
        data = {}
        res = requests.post('https://edith.xiaohongshu.com/api/sns/web/v1/login/activate',headers=headers,proxies=GLOBAL_PROXY,data=json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                                         .encode('utf-8'))
        session =  res.json()['data']['session']
        return f'a1={a1};web_session={session}' 
c = XhsWebApi()
def insert_data( table_name, data_dict):
    """插入数据"""
    with pool.cursor() as cursor:
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['%s'] * len(data_dict))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data_dict.values()))
    pool.commit()

def select_data(table_name, conditions=None, fields="*", params=None):
    """查询数据，使用参数化查询"""
    with pool.cursor() as cursor:
        sql = f"SELECT {fields} FROM {table_name}"
        if conditions:
            sql += f" WHERE {conditions}"
        cursor.execute(sql, params or ())
        return cursor.fetchall()


def search_comment(keywords, max_days_old=1, min_comments=0, max_comments=8):
    """
    智能搜索并评论小红书帖子
    参数:
    - keywords: 搜索关键词列表
    - max_days_old: 最大发帖天数
    - min_comments: 最少评论数
    - max_comments: 最大评论数
    """
    # 评论模板库
    comment_templates = config['params']['comment_templates']['search']

    def get_comment_type(title, desc):
        """根据标题和描述判断评论类型"""
        text = (title + desc).lower()
        if any(word in text for word in ['程序','代码','python','java','开发']):
            return 'programming'
        elif any(word in text for word in ['数据','爬虫','采集']):
            return 'data'
        return 'general'
        
    def should_comment(item_detail):
        """判断是否应该评论"""
        # 检查发布时间
        if item_detail['push_time'] < datetime.datetime.now() - datetime.timedelta(days=max_days_old):
            return 0
            
        comment_count = int(item_detail['comment_count'])
        # 评论数要在合理范围
        if comment_count < min_comments or comment_count > max_comments:
            return 1
            
        # 检查标题和描述是否包含关键词
        text = item_detail['title'] + item_detail['description']
        if  len([w for w in ['求助','帮忙','求解','请教','有偿'] if w in text]) == 0:
            return 2
            
        # 检查互动数据
        if int(item_detail['liked_count']) > 10:
            return 3
            
        return 4

    def generate_comment(title, desc):
        """根据内容生成合适的评论"""
        comment_type = get_comment_type(title, desc)
        return random.choice(comment_templates[comment_type])

    # 主搜索逻辑
    for keyword in keywords:
        for page in range(1, 3):
            time.sleep(random.randint(2, 5))  # 随机延迟
            
            try:
                result = c.search(keyword, page)
                if not result:
                    continue
                for item in result  :
                    if '-' in item['NoteId']:
                        continue
                    select_data_result = select_data('xhs_action', 'action_aid = %s', 'action_aid', (item['NoteId'],))
                    if select_data_result:
                        continue
                        
                    # 获取详情
                    detail = c.blog_detail(item['NoteId'], item['Xtoken'])
                    should_comment_result = should_comment(detail)
                    print("keyword",keyword,"page",page,"select_data_result",select_data_result,"should_comment_result",should_comment_result)
                    if should_comment_result == 0:
                        break
                    # 判断是否需要评论
                    if  should_comment_result != 4:
                        continue
                        
                    # 检查是否已评论过
           
                        
                    # 生成评论
                    comment = generate_comment(detail['title'], detail['description'])
                    
                    # 发送评论
                    c.push_comment(item['NoteId'], comment)
                    
                    # 记录操作
                    url = f'https://www.xiaohongshu.com/explore/{item["NoteId"]}?xsec_token={item["Xtoken"]}&xsec_source=pc_feed'
                    action_dict = {
                                                'action_type': '搜索后评论',          # varchar(10)
                                                'action_time': datetime.datetime.now(),        # datetime
                                                'noteid': item['NoteId'],              # varchar(80)
                                                'action_aid': item['NoteId'],          # varchar(100), 主键
                                                'title': detail['title']    ,               # varchar(255)
                                                'url':url, # varchar(255)
                                                'description': detail['description'],                # text
                                                'push_time': detail['push_time'],         # datetime
                                                'like_count':int(detail['liked_count']) ,           # int
                                                'comment_count': int(detail['comment_count']),        # int
                                                'share_count': int(detail['share_count']),          # int
                                                'collect_count': int(detail['collected_count']),        # int
                                                'action_status': 'success',       # varchar(10)
                                                'action_info': str(comment)[:40],         # varchar(50)
                                                'username': detail['username'],         # datetime
                                                'userid':detail['userid'] ,           # int
                                                'action_userid': None,        # int
                                                'action_username': None,          # int
                                                'action_detail': f'搜索"{keyword}"找到符合条件的帖子并评论:{comment}'         # varchar(255)

                                            }
                    
                    print(f"评论成功: {action_dict['title']}")
                    insert_data('xhs_action', action_dict)
                    
                    time.sleep(random.randint(10, 20))  # 评论后随机等待
                    
            except Exception as e:
                print(f"处理出错: {str(e)}")
                continue

                            
def download_image(link):
    try:
        response = requests.get(link)
        if response.content:
            with open(f'only.jpg','wb') as f:
                f.write(response.content)
            return True
        else:
            return False
    except:
        return False
def recommand_like(keywords):
    c.recommand_like(keywords)
def hot_comment(keywords):
    keyword_run = True
    if keywords:
        
         for keyword in keywords:
            try:
                keyword_run = True
                for i in range(1,11):
                    if keyword_run == False:
                        break
                    result = c.search(keyword,i)
                    if result:
                        for item in result:
                            action_aid = item['NoteId']
                            if '-' in item['NoteId'] or  select_data('xhs_action', 'action_aid = %s', 'action_aid', (action_aid,)):
                                continue 
                            detail = c.blog_detail(item['NoteId'],item['Xtoken'])
                            push_time = detail['push_time']
                            link = detail['image_url']
                            download_image(link)
                            comment_count = int(detail['comment_count'])
                            title = detail['title']
                            if '头像' in title or '壁纸' in title  or '情侣' in title or '图' in title or '穿搭' in title or '衣' in title:
                                continue
                            description = detail['description']
                            like_count = int(detail['liked_count'])
                            collect_count = int(detail['collected_count'])
                            share_count = int(detail['share_count'])
                            username = detail['username']
                            userid = detail['userid']
                            action_userid = None
                            action_username = None
                            
                            condition = (comment_count > 5 or like_count > 10 ) and collect_count > 2 and comment_count > 3
                            if push_time < datetime.datetime.now() - datetime.timedelta(days=1):
                                condition = (comment_count > 10 or like_count > 20 ) and collect_count > 2 and comment_count > 3
                            if   condition:
                                info  = ''
                                action_aid = item['NoteId']
                                is_ocr = orc_word('only.jpg')
                                if  is_ocr:
                                    c.blog_collect(item['NoteId'])
                                    if '紫' in keyword  :
                                        c.move_collect('6756323e0000000030010fbe',item['NoteId'])
                                    if '纯' in keyword  :
                                        c.move_collect('67562c2c000000003100c124',item['NoteId'])
                                    if 'BBW' in keyword:
                                        c.move_collect('67563254000000003100ada4',item['NoteId'])
                                    if '艳' in keyword:
                                        c.move_collect('67562c48000000003003cf09',item['NoteId'])
                                    if '腹肌' in keyword:
                                        c.move_collect('67562c5400000000300074e1',item['NoteId'])
                                    if collect_count + comment_count + share_count > like_count:
                                        c.move_collect('6756325e0000000031002468',item['NoteId'])
                                    url = f'https://www.xiaohongshu.com/explore/{item["NoteId"]}?xsec_token={item["Xtoken"]}&xsec_source=pc_feed'
                                    action_dict = {
                                                'action_type': '收录美好',          # varchar(10)
                                                'action_time': datetime.datetime.now(),        # datetime
                                                'noteid': item['NoteId'],              # varchar(80)
                                                'action_aid': item['NoteId'],          # varchar(100), 主键
                                                'title': title,               # varchar(255)
                                                'url':url, # varchar(255)
                                                'description': description,                # text
                                                'push_time': push_time,         # datetime
                                                'like_count':like_count ,           # int
                                                'comment_count': comment_count,        # int
                                                'share_count': share_count,          # int
                                                'collect_count': collect_count,        # int
                                                'action_status': 'success',       # varchar(10)
                                                'action_info': info,         # varchar(50)
                                                'username': username,         # datetime
                                                'userid':userid ,           # int
                                                'action_userid': action_userid,        # int
                                                'action_username': action_username,          # int
                                                'action_detail': f'请欣赏{url}'        # varchar(255)

                                            }
                                    print(action_dict)
                                    insert_data('xhs_action',action_dict)
            except Exception as e:
                print(e)
def hot_comments(keywords):

    keyword_run = True
    if keywords:
        
         for keyword in keywords:
            try:
                keyword_run = True
                for i in range(1,11):
                    if keyword_run == False:
                        break
                    result = c.search(keyword,i)
                    if result: 
                        for item in result:
                            if '-' in item['NoteId'] :
                                continue 
                            exists = select_data(
                                    'xhs_action',
                                    'action_aid = %s AND action_type = %s',
                                    'action_aid',
                                    (item['NoteId'], '热帖评论')
                                )
                            if not exists:
                                detail = c.blog_detail(item['NoteId'],item['Xtoken'])
                                content = get_review(detail['description'])
                                comment_id = c.push_comment(item['NoteId'],content)
                                push_time = detail['push_time']
                                link = detail['image_url']
                                comment_count = int(detail['comment_count'])
                                title = detail['title']
                                description = detail['description']
                                like_count = int(detail['liked_count'])
                                collect_count = int(detail['collected_count'])
                                share_count = int(detail['share_count'])
                                username = detail['username']
                                userid = detail['userid']
                                action_userid = None
                                action_username = None
                                url = f'https://www.xiaohongshu.com/explore/{item["NoteId"]}?xsec_token={item["Xtoken"]}&xsec_source=pc_feed'
                                action_dict = {
                                                    'action_type': '热帖评论',          # varchar(10)
                                                    'action_time': datetime.datetime.now(),        # datetime
                                                    'noteid': item['NoteId'],              # varchar(80)
                                                    'action_aid': item['NoteId'],          # varchar(100), 主键
                                                    'title': title,               # varchar(255)
                                                    'url':url, # varchar(255)
                                                    'description': description,                # text
                                                    'push_time': push_time,         # datetime
                                                    'like_count':like_count ,           # int
                                                    'comment_count': comment_count,        # int
                                                    'share_count': share_count,          # int
                                                    'collect_count': collect_count,        # int
                                                    'action_status': 'success',       # varchar(10)
                                                    'action_info': comment_id,         # varchar(50)
                                                    'username': username,         # datetime
                                                    'userid':userid ,           # int
                                                    'action_userid': action_userid,        # int
                                                    'action_username': action_username,          # int
                                                    'action_detail': f'在{url}发布{content}id={comment_id}'        # varchar(255)

                                                }
                                print(action_dict)
                                insert_data('xhs_action',action_dict)
                                comment_list = c.blog_comment(item['NoteId'],item['Xtoken'])
                                print('comment_list',comment_list)
                                if comment_list:
                                    for comment in comment_list:
                                        time.sleep(1)
                                        comment_id = comment['CommentId']
                                        CommentText = comment['CommentText']
                                        c.comment_like(item['NoteId'],comment_id)
                                        url = f'https://www.xiaohongshu.com/explore/{item["NoteId"]}?xsec_token={item["Xtoken"]}&xsec_source=pc_feed'
                                        action_dict = {
                                                    'action_type': '评论点赞',          # varchar(10)
                                                    'action_time': datetime.datetime.now(),        # datetime
                                                    'noteid': item['NoteId'],              # varchar(80)
                                                    'action_aid': comment_id,          # varchar(100), 主键
                                                    'title': title,               # varchar(255)
                                                    'url':url, # varchar(255)
                                                    'description': description,                # text
                                                    'push_time': push_time,         # datetime
                                                    'like_count':like_count ,           # int
                                                    'comment_count': comment_count,        # int
                                                    'share_count': share_count,          # int
                                                    'collect_count': collect_count,        # int
                                                    'action_status': 'success',       # varchar(10)
                                                    'action_info': CommentText,         # varchar(50)
                                                    'username': username,         # datetime
                                                    'userid':userid ,           # int
                                                    'action_userid': action_userid,        # int
                                                    'action_username': action_username,          # int
                                                    'action_detail': f'在{url}点赞{CommentText}'        # varchar(255)

                                                }
                                        print(action_dict)
                                        insert_data('xhs_action',action_dict)
            except Exception as e:
                print(e)
# search_comment(['数据采集求助','爬虫求助', '数据分析求助', '数据处理帮忙', '数据统计求助', '数据可视化求助','论文数据求助','大学生作业求助','数据求助','作业求助','JS逆向求助'])
def orc_word(image_path):
    reader = easyocr.Reader(['ch_sim'], gpu=True)

    # 指定要识别的图片路径

    # 使用Reader对象读取图片并识别文字
    result = reader.readtext(image_path)
    run = True
    QUALITY = 0
    # 打印识别结果
    # 每个识别结果是一个元组，包含边界框坐标、识别的文本和置信度
    if result:
        for (bbox, text, prob) in result:
            QUALITY += len(re.sub(r'[^\u4e00-\u9fff]', '', text.strip())) / 10
            print('---------------')
            print('text',text)
            print('prob',prob)
            if (text and prob > 0.5) or QUALITY >= 0.3:
                run = False
                break
    
    return run
def search_comment_job():
    # 这里可以调用你的搜索和评论函数
    search_comment(['数据采集求助','爬虫求助', '数据分析求助', '数据处理帮忙', '数据统计求助', '数据可视化求助','论文数据求助','大学生作业求助','数据求助','作业求助','JS逆向求助'])
def hot_comment_jobs():
    # 这里可以调用你的搜索和评论函数
    hot_comments([
    # 恋爱相关
    "恋爱日常", "恋爱分享", "恋爱经历", "恋爱技巧", "脱单",
    "恋爱心理", "恋爱故事", "异地恋", "初恋", "暗恋",
    "恋爱观", "恋爱总结", "恋爱相处", "恋爱必修课", "情侣日常",
    
    # 情感状态
    "心动瞬间", "暧昧期", "单身", "失恋", "暗恋",
    "心动", "心碎", "心酸", "遗憾", "遇见",
    "错过", "放下", "成长", "治愈", "温暖",
    
    # 感情表达
    "甜甜的恋爱", "甜宠", "浪漫", "温柔", "感动",
    "真诚", "细节控", "仪式感", "告白", "表白",
    "心动信号", "心动时刻", "心动回忆", "心动瞬间", "心动故事",
    
    # 情感话题
    "情感故事", "情感分享", "情感记录", "情感经历", "情感观点",
    "情感困惑", "情感建议", "情感答疑", "情感共鸣", "情感成长",
    
    # 恋爱阶段
    "暗恋期", "追求期", "热恋期", "磨合期", "稳定期",
    "倦怠期", "分手期", "复合期", "修复期", "重逢",  "大模型", "AGI", "智能驾驶", "数字人", "元宇宙", "光子计算", "量子通信", "芯片国产化", "算力网络", "类脑计算",
    "躺平", "内卷", "打工人", "摆烂", "绝绝子", "破防", "社恐", "润学", "双减", "养老焦虑",
    "新消费", "数字经济", "共同富裕", "直播带货", "零工经济", "种草", "小红书", "抖音电商", "消费降级", "银发经济",
    "佛系", "断舍离", "极简主义", "慢生活", "小确幸", "居家办公", "养生", "断糖", "轻奢", "微度假",
    "破防", "绝绝子", "无语子", "啥都不懂", "整活", "破防了", "太真实了", "笑死", "润了", "太上头了",
    "35岁焦虑", "职场PUA", "副业", "斜杠青年", "职场社恐", "职业倦怠", "裁员潮", "跳槽", "降薪", "考公",
    "二次元", "国潮", "汉服", "剧本杀", "密室逃脱", "脱口秀", "说唱", "国风", "沉浸式体验", "虚拟偶像",
    "碳中和", "可持续", "垃圾分类", "新能源", "心理健康", "亚健康", "免疫力", "环保主义", "素食主义", "低碳生活",
    "考研", "留学", "职业教育", "终身学习", "在线教育", "素质教育", "学历焦虑", "考证", "技能培训", "教育内卷",
    "数字游民", "智慧城市", "乡村振兴", "城市更新", "数字化转型", "智能家居", "远程医疗", "区块链", "人工智能", "元宇宙"
])
def hot_comment_job():
    # 这里可以调用你的搜索和评论函数
    hot_comment(['情感','快乐','艳比基尼','艳御姐黑丝','艳大雷美女','纯欲高冷美女','紫色异味大胸美女','艳黑丝','紫色异味美女','纯欲大雷美女','BBW大胸美女'])
def setup_schedule():
    """设置调度任务"""
    # 每天早上8:30执行任务
    schedule.every().day.at("08:30").do(search_comment_job)
    # 每天下午2:00执行任务
    schedule.every().day.at("14:00").do(search_comment_job)
    # 每天晚上7:00执行任务
    schedule.every().day.at("19:00").do(search_comment_job)
    schedule.every(2).hours.do(search_comment_job)
def run_scheduler():
    """运行调度器"""
    setup_schedule()
    print("调度器已启动")
    while True:
        schedule.run_pending()
        time.sleep(1)  # 每秒检查一次

if __name__ == "__main__":
        c = XhsWebApi()
        # search_comment_job()
        ex_id = []
        cookie = "loadts=1752799212347;xsecappid=xhs-pc-web;acw_tc=0a00d7a117527992033555961e35722b983193e5fecbaa8d529dcf58e37919;x-user-id-creator.xiaohongshu.com=662cd92b00000000030311c2;websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d;webBuild=4.72.0;sec_poison_id=4ef38f1f-4848-486f-b1fd-3d033e8f36b1;web_session=0400698c98f9be56269494df4c3a4bc6ecc7cf;gid=yjKK0dWYD2CjyjKK0dWW8fK94yxfTJ3C1TVMAF4UCdAxjf28jfDIKk888J82jqJ8fqSqqd0J;a1=1966ae77041hdk2ixlkjspxeqh99dbn6xdqdg6tr450000205932;abRequestId=bf7b04f8-11dd-5b28-950e-f3243c3414a8;customerClientId=950294290162470;unread={%22ub%22:%22687081e800000000120339f4%22%2C%22ue%22:%2268591c290000000012033993%22%2C%22uc%22:28};webId=036ea57b16d5490eea0239156d23e25a"
        import  pandas as pd

        with open('comment','r',encoding='utf-8') as f:
            for line in f.readlines():
                line = json.loads(line)
                url_id = line['NoteId']
                ex_id.append(url_id)

        df = pd.read_excel('search_result.xlsx')
        for index, row in df.iterrows():
            xsec_token = row['xsec_token']
            id = row['id']

            comment_count = row['comment_count']
            if id not in ex_id:
                ex_id.append(id)
                if comment_count >= 5:
                    try:
                         print(id)
                         c.blog_comment(id,xsec_token,'',0,cookie)
                         time.sleep(2)
                    except Exception as e:
                        print(e)


