import datetime
import json
import os
from urllib.parse import parse_qs
import requests,random

class PkuAccount:
    # 这个类是一个完整类的精简版，要不没必要单独写
    def __init__(self, username: str, passwd: str):
        self._username = username
        self._passwd = passwd
        self._session = requests.Session()
        fake_ua = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'])
        self._session.headers.update({
            'User-agent': fake_ua})
        self.alias_dict = {'portal': 'portal2017'}
        self.app_dict = {
            'portal2017': ['https://portal.pku.edu.cn/portal2017/ssoLogin.do', 'https://portal.pku.edu.cn/portal2017/'],
        }

    @property
    def session(self):
        return self._session

    def _get_token(self, appid, otp_code=''):
        if appid in self.alias_dict:
            appid = self.alias_dict[appid]
        auth_url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
        auth_dict = {'appid': appid, 'userName': self._username, 'password': self._passwd,
                     'redirUrl': self.app_dict[appid][0], 'otpCode': otp_code}
        return_text = self._session.post(auth_url, data=auth_dict, timeout=7).text

        try:
            return json.loads(return_text)['token']
        except KeyError:
            raise Exception(f'{return_text}')

    def login(self, appid, otp_code=''):
        if appid in self.alias_dict:
            appid = self.alias_dict[appid]

        token = self._get_token(appid, otp_code=otp_code)
        error = 0
        while error < 4:
            try:
                process_callback = self._session.get(self.app_dict[appid][0], params={
                    'rand': random.random(), 'token': token}, timeout=7)
                return {'success': True, 'token': f'{token}', 'land_url': f'{process_callback.url}',
                        'land_text': f'{process_callback.text}'}
            except:
                error += 1

username=os.environ["USERNAME"]
passwd=os.environ["PASSWORD"]

pku = PkuAccount(username, passwd)

pku.login('portal')
t_1 = pku.session.get('https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=stuCampusExEn')
token = parse_qs(t_1.url)['token'][0]
land = pku.session.get(f'https://simso.pku.edu.cn/ssapi/simsoLogin?token={token}')

sid = json.loads(land.text)['sid']
xh=json.loads(land.text)['xh']

r1 = pku.session.get(f'https://simso.pku.edu.cn/pages/sadEpidemicAccess.html?_sk={xh}#/epiAccessHome')
dt=str(datetime.datetime.now().strftime('%Y%m%d'))

for type in ['出校','入校']:
    last_info=pku.session.get(f'https://simso.pku.edu.cn/ssapi/stuaffair/epiAccess/getLastSqxx?sid={sid}&_sk={xh}&sqlb={type}')
    last_info=json.loads(last_info.text)["row"]
    # Overwrite date
    last_info["cxrq"]=dt
    last_info["rxrq"]=dt
    r0 = pku.session.post(f'https://simso.pku.edu.cn/ssapi/stuaffair/epiAccess/saveSqxx?sid={sid}&_sk={xh}', json=last_info)
    res_0 = json.loads(r0.text)
    submit=pku.session.get(f'https://simso.pku.edu.cn/ssapi/stuaffair/epiAccess/submitSqxx?sid={sid}&_sk={xh}&sqbh={res_0["row"]}')
    submit_response=json.loads(submit.text)
    if submit_response['code'] in [1, '1'] and submit_response["msg"] == '成功':
        print(f'Success: {submit_response}') # Success
    else:
        print(f'Failed: {submit_response}') # Failed
        exit(1)
