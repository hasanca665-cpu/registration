#!/usr/bin/env python3
# FINAL_COMPLETE_BOT.py - 100% Working | 1 Message per Account (Live Edit) 🔥

import asyncio
import aiohttp
import aiofiles
import json
import os
import random
import string
import hashlib
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
import threading

# ==================== Flask for Render.com ====================
app = Flask(__name__)
@app.route('/')
def home():
    return "🤖 Final Complete Bot Running | 1 Account = 1 Live Message 🔥"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)

# ==================== Logging ====================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# ==================== Constants ====================
BOT_TOKEN = "6329569356:AAEfPA03ZjZAByKhGhNUc8n_x5EATZpHDGw"
KEY = b'djchdnfkxnjhgvuy'
IV = b'ayghjuiklobghfrt'

BASE_WEBSITE_CONFIGS = {
   "1": {
    "name": "Job989",
    "api_domain": "https://job989.club/",
    "origin": "https://job989.com",
    "referer": "https://job989.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://job989.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "2": {
    "name": "TG299",
    "api_domain": "https://tg299.online/",
    "origin": "https://tg299.club",
    "referer": "https://tg299.club/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://tg299.online/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "3": {
    "name": "TG377",
    "api_domain": "https://tg377.club/",
    "origin": "https://tg377.vip",
    "referer": "https://tg377.vip/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://tg377.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "4": {
    "name": "DIY22",
    "api_domain": "https://diy22.club/",
    "origin": "https://diy22.net",
    "referer": "https://diy22.net/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://diy22.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "5": {
    "name": "22Job",
    "api_domain": "https://web.112233job.com/",
    "origin": "https://22job.me",
    "referer": "https://22job.me/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://web.112233job.com/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "6": {
    "name": "Port07",
    "api_domain": "https://port07.cc/",
    "origin": "https://port07.bet",
    "referer": "https://port07.bet/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://port07.cc/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "7": {
    "name": "Wapp2",
    "api_domain": "https://rcs22.club/",
    "origin": "https://wapp2.com",
    "referer": "https://wapp2.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://rcs22.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "8": {
    "name": "Dep6",
    "api_domain": "https://dep6.club/",
    "origin": "https://dep6.com",
    "referer": "https://dep6.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://dep6.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "9": {
    "name": "333Work",
    "api_domain": "https://web.111333work.com/",
    "origin": "https://333work.com",
    "referer": "https://333work.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://web.111333work.com/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "10": {
    "name": "Task32",
    "api_domain": "https://task32.club/",
    "origin": "https://task32.com",
    "referer": "https://task32.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://task32.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "11": {
    "name": "WsGo",
    "api_domain": "https://wsgo22.com/",
    "origin": "https://wsgo55.com",
    "referer": "https://wsgo55.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://wsgo22.com/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "12": {
    "name": "Ok6Job",
    "api_domain": "https://ok6job.cc/",
    "origin": "https://ok6job.com",
    "referer": "https://ok6job.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://ok6job.cc/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "13": {
    "name": "Ok7Job",
    "api_domain": "https://ok7job.vip/",
    "origin": "https://ok7job.net",
    "referer": "https://ok7job.net/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://ok7job.vip/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "14": {
    "name": "Ok8Job",
    "api_domain": "https://ok8job.cc/",
    "origin": "https://ok8job.net",
    "referer": "https://ok8job.net/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://ok8job.cc/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "15": {
    "name": "Ok9Job",
    "api_domain": "https://ok9job.vip/",
    "origin": "http://ok9job.net",
    "referer": "http://ok9job.net/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://ok9job.vip/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "16": {
    "name": "WsPart",
    "api_domain": "https://wspart.top/",
    "origin": "https://wspart.com",
    "referer": "https://wspart.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://wspart.top/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "17": {
    "name": "WsFull3",
    "api_domain": "https://wsfull3.top/",
    "origin": "https://wsfull3.com",
    "referer": "https://wsfull3.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://wsfull3.top/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "18": {
    "name": "PartTime2",
    "api_domain": "https://part-time2.club/",
    "origin": "https://part-time2.com",
    "referer": "https://part-time2.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://part-time2.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "19": {
    "name": "Mess6",
    "api_domain": "https://mess6.club/",
    "origin": "https://news669.com",
    "referer": "https://news669.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://mess6.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "20": {
    "name": "Task33",
    "api_domain": "https://task33.club/",
    "origin": "http://task33.vip",
    "referer": "http://task33.vip/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://task33.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "21": {
    "name": "Sms93",
    "api_domain": "https://sms93.club/",
    "origin": "https://sms93.com",
    "referer": "https://sms93.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://sms93.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "22": {
    "name": "Job777",
    "api_domain": "https://job777.club/",
    "origin": "https://job777.me",
    "referer": "https://job777.me/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://job777.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "23": {
    "name": "FullTime2",
    "api_domain": "https://full-time2.club/",
    "origin": "https://full-time2.com",
    "referer": "https://full-time2.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://full-time2.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "24": {
    "name": "Sms323",
    "api_domain": "https://sms323.club/",
    "origin": "https://sms323.com",
    "referer": "https://sms323.com/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://sms323.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "25": {
    "name": "Atm001",
    "api_domain": "https://atm001.com/",
    "origin": "http://atm8.me",
    "referer": "http://atm8.me/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://atm001.com/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "26": {
    "name": "Mk8",
    "api_domain": "https://mk8ht.com/",
    "origin": "https://mmmmm.cyou",
    "referer": "https://mmmmm.cyou/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://mk8ht.com/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  },
  "27": {
    "name": "Wa2",
    "api_domain": "https://web.wa2.club/",
    "origin": "https://wa2.club",
    "referer": "https://wa2.club/",
    "login_path": "api/user/signIn",
    "send_code_path": "api/ws_phone/sendCode",
    "get_code_path": "api/ws_phone/getCode",
    "phone_list_url": "https://web.wa2.club/api/ws_phone/phoneList",
    "signup_path": "api/user/signUp",
    "referral_field": "invite_code"
  }
}

ANDROID_UAS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi 14 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
]

# ==================== User Session Management ====================
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.is_running = False
        self.rotation_task = None
        self.proxy = None
        self.website_tasks = []
        self.cycle_count = 0

    def config_file(self): return f"user_config_{self.user_id}.json"
    def data_file(self): return f"user_data_{self.user_id}.txt"

    def load(self):
        if os.path.exists(self.config_file()):
            try:
                with open(self.config_file(), 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    self.proxy = d.get('proxy')
                    self.website_tasks = d.get('website_tasks', [])
                    self.cycle_count = d.get('cycle_count', 0)
            except: pass

    def save(self):
        data = {'proxy': self.proxy, 'website_tasks': self.website_tasks, 'cycle_count': self.cycle_count}
        with open(self.config_file(), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def stats(self):
        success = sum(t.get('total_success', 0) for t in self.website_tasks)
        attempts = sum(t.get('total_attempts', 0) for t in self.website_tasks)
        rate = round(success / attempts * 100, 1) if attempts > 0 else 0
        return {'success': success, 'attempts': attempts, 'rate': rate}

def get_session(uid):
    if uid not in user_sessions:
        user_sessions[uid] = UserSession(uid)
        user_sessions[uid].load()
    return user_sessions[uid]

# ==================== Helper Functions ====================
def gen_bd_phone():
    return "+880" + random.choice(["13","14","15","16","17","18","19"]) + "".join(random.choices(string.digits, k=8))

def encrypt_username(phone):
    p = phone.replace("+", "").encode()
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return base64.b64encode(cipher.encrypt(pad(p, 16))).decode()

def build_device(phone):
    seed = hashlib.sha256(phone.encode()).hexdigest()
    ua = random.choice(ANDROID_UAS)
    return {
        "ua": ua,
        "device_id": hashlib.sha256((seed+"dev").encode()).hexdigest(),
        "android_id": hashlib.sha256((seed+"aid").encode()).hexdigest()[:16],
        "imei": "35" + "".join(random.choices(string.digits, k=13)),
        "mac_wifi": ":".join(f"{random.randint(0,255):02X}" for _ in range(6)),
        "canvas_fp": hashlib.sha256((seed+"canvas").encode()).hexdigest()[:40],
        "audio_fp": hashlib.sha256((seed+"audio").encode()).hexdigest()[:40]
    }

def parse_proxy(p):
    if not p: return None
    parts = p.split(':')
    if len(parts) == 4: return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
    if len(parts) == 2: return f"http://{parts[0]}:{parts[1]}"
    return None

async def perform_registration(session, cfg, phone, pwd, ref, dev, proxy):
    encrypted = encrypt_username(phone)
    url = cfg['api_domain'] + cfg['signup_path']
    data = {"username": encrypted, "password": pwd, "confirm_password": pwd, cfg.get("referral_field", "invite_code"): ref}
    headers = {
        "User-Agent": dev["ua"], "Origin": cfg["origin"], "Referer": cfg["referer"],
        "X-Device-ID": dev["device_id"], "X-Android-ID": dev["android_id"],
        "X-IMEI": dev["imei"], "X-Mac-Wifi": dev["mac_wifi"],
        "X-Canvas-FP": dev["canvas_fp"], "X-Audio-FP": dev["audio_fp"]
    }
    try:
        async with session.post(url, data=data, headers=headers, proxy=proxy, timeout=15) as r:
            try: j = await r.json()
            except: j = {"raw": await r.text()}
            return r.status, j
    except Exception as e:
        return None, {"error": str(e)}

async def save_result(uid, phone, site, status, resp):
    file = f"user_data_{uid}.txt"
    async with aiofiles.open(file, "a", encoding="utf-8") as f:
        await f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {site} | {phone} | {status} | {resp}\n")

# ==================== Main Rotation (1 Message per Account) ====================
async def run_rotation(user_id, chat_id, bot):
    ses = get_session(user_id)
    try:
        while ses.is_running:
            ses.cycle_count += 1
            total = len(ses.website_tasks)

            await bot.send_message(chat_id, f"🚀 <b>Cycle #{ses.cycle_count} Started!</b>\n🌐 Total Sites: {total}\n⚡ Live updates below ↓", parse_mode='HTML')

            async with aiohttp.ClientSession() as session:
                for idx, task in enumerate(ses.website_tasks, 1):
                    if not ses.is_running: break
                    cfg = BASE_WEBSITE_CONFIGS[task['website_key']]
                    site = task['website_name']
                    ref = task['refer_code']

                    phone = gen_bd_phone()
                    pwd = phone.replace("+", "")
                    dev = build_device(phone)

                    # 1 Message Only
                    msg = await bot.send_message(chat_id,
                        f"⏳ <b>[{idx}/{total}] {site}</b>\n\n"
                        f"📱 Phone: <code>{phone}</code>\n"
                        f"🔑 Pass : <code>{pwd}</code>\n"
                        f"⏳ Registering...", parse_mode='HTML')

                    status_code, resp = await perform_registration(session, cfg, phone, pwd, ref, dev, ses.proxy)

                    task['total_attempts'] = task.get('total_attempts', 0) + 1
                    success = status_code == 200 and resp.get("code") == 1
                    if success:
                        task['total_success'] = task.get('total_success', 0) + 1

                    emoji = "✅ SUCCESS" if success else "❌ FAILED"
                    reason = f"\n❌ {resp.get('msg') or resp.get('error', 'Unknown')}" if not success else ""

                    await msg.edit_text(
                        f"{emoji} <b>[{idx}/{total}] {site}</b>\n\n"
                        f"📱 Phone    : <code>{phone}</code>\n"
                        f"👤 Username : <code>{phone}</code>\n"
                        f"🔑 Password : <code>{pwd}</code>{reason}",
                        parse_mode='HTML')

                    await save_result(user_id, phone, site, "SUCCESS" if success else "FAILED", resp)
                    await asyncio.sleep(0.8)

            stats = ses.stats()
            await bot.send_message(chat_id,
                f"✅ <b>Cycle #{ses.cycle_count} Complete!</b>\n"
                f"✅ Success: {stats['success']}\n"
                f"🔄 Attempts: {stats['attempts']}\n"
                f"📊 Rate: {stats['rate']}%\n\n"
                f"🔥 Next cycle in 3s...", parse_mode='HTML')
            ses.save()
            await asyncio.sleep(3)

    except asyncio.CancelledError: pass
    except Exception as e:
        await bot.send_message(chat_id, f"💥 Error: {e}")
    finally:
        ses.is_running = False
        stats = ses.stats()
        await bot.send_message(chat_id,
            f"🛑 <b>Rotation Stopped!</b>\n\n"
            f"✅ Total Success : {stats['success']}\n"
            f"🔄 Total Attempts: {stats['attempts']}\n"
            f"📊 Rate: {stats['rate']}%\n"
            f"🔥 Cycles: {ses.cycle_count}\n\n"
            f"💾 Use /download_data", parse_mode='HTML')

# ==================== Commands ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start Rotation", callback_data="start_rot"), InlineKeyboardButton("🛑 Stop Rotation", callback_data="stop_rot")],
        [InlineKeyboardButton("🌐 My Sites", callback_data="my_sites"), InlineKeyboardButton("📊 Stats", callback_data="stats")]
    ])
    await update.message.reply_html("🤖 <b>Final Complete Bot</b> 🔥\n\n✅ 1 Account = 1 Live Message\n✨ Super Clean Chat\n\n/start_rotation - Begin", reply_markup=keyboard)

async def add_website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /add_website 1 ABC123")
        return
    wid, ref = context.args[0], " ".join(context.args[1:])
    if wid not in BASE_WEBSITE_CONFIGS:
        await update.message.reply_text("❌ Invalid ID! Use /list_websites")
        return
    ses = get_session(update.effective_user.id)
    if any(t['website_key'] == wid for t in ses.website_tasks):
        await update.message.reply_text("⚠️ Already added!")
        return
    ses.website_tasks.append({"website_key": wid, "website_name": BASE_WEBSITE_CONFIGS[wid]["name"], "refer_code": ref, "total_success": 0, "total_attempts": 0})
    ses.save()
    await update.message.reply_text(f"✅ <b>{BASE_WEBSITE_CONFIGS[wid]['name']}</b> Added!\nReferral: <code>{ref}</code>", parse_mode='HTML')

async def list_websites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ses = get_session(update.effective_user.id)
    text = "🌐 <b>Available Sites</b>\n\n"
    for k, v in BASE_WEBSITE_CONFIGS.items():
        status = "✅" if any(t['website_key']==k for t in ses.website_tasks) else "➖"
        text += f"{status} <code>{k}</code> → {v['name']}\n"
    text += f"\n✅ Your sites: {len(ses.website_tasks)}"
    await update.message.reply_html(text)

async def set_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /set_proxy ip:port:user:pass\nOr /set_proxy ip:port")
        return
    proxy = parse_proxy(context.args[0])
    if not proxy:
        await update.message.reply_text("❌ Invalid proxy format!")
        return
    ses = get_session(update.effective_user.id)
    ses.proxy = proxy
    ses.save()
    await update.message.reply_text(f"✅ Proxy Set!\n<code>{proxy}</code>", parse_mode='HTML')

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ses = get_session(update.effective_user.id)
    s = ses.stats()
    text = f"📊 <b>Your Stats</b>\n\n" \
           f"✅ Success : {s['success']}\n" \
           f"🔄 Attempts: {s['attempts']}\n" \
           f"📈 Rate    : {s['rate']}%\n" \
           f"🔥 Cycles  : {ses.cycle_count}\n" \
           f"🌐 Sites   : {len(ses.website_tasks)}"
    await update.message.reply_html(text)

async def download_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = f"user_data_{update.effective_user.id}.txt"
    if not os.path.exists(file):
        await update.message.reply_text("❌ No data yet!")
        return
    with open(file, 'rb') as f:
        await update.message.reply_document(InputFile(f, filename=f"My_Accounts_{update.effective_user.id}.txt"))

async def clear_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = f"user_data_{update.effective_user.id}.txt"
    if os.path.exists(file):
        os.remove(file)
        await update.message.reply_text("✅ Data cleared!")
    else:
        await update.message.reply_text("ℹ️ No data to clear")

async def start_rotation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ses = get_session(update.effective_user.id)
    if ses.is_running:
        await update.message.reply_text("⚠️ Already running!")
        return
    if not ses.website_tasks:
        await update.message.reply_text("❌ Add sites first! /add_website 1 ABC123")
        return
    ses.is_running = True
    ses.rotation_task = asyncio.create_task(run_rotation(update.effective_user.id, update.effective_chat.id, context.bot))
    await update.message.reply_text("🚀 <b>Rotation Started!</b>\n⚡ 1 message per account (live update)", parse_mode='HTML')

async def stop_rotation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ses = get_session(update.effective_user.id)
    if not ses.is_running:
        await update.message.reply_text("❌ Not running!")
        return
    ses.is_running = False
    if ses.rotation_task: ses.rotation_task.cancel()
    await update.message.reply_text("🛑 Stopping...")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "start_rot": await start_rotation(update, context)
    elif data == "stop_rot": await stop_rotation(update, context)
    elif data == "stats": await stats_cmd(update, context)
    elif data == "my_sites": await list_websites(update, context)

# ==================== Bot Start ====================
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_website", add_website))
    application.add_handler(CommandHandler("list_websites", list_websites))
    application.add_handler(CommandHandler("set_proxy", set_proxy))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("download_data", download_data))
    application.add_handler(CommandHandler("clear_data", clear_data))
    application.add_handler(CommandHandler("start_rotation", start_rotation))
    application.add_handler(CommandHandler("stop_rotation", stop_rotation))
    application.add_handler(CallbackQueryHandler(button))

    print("🤖 Final Complete Bot Started!")
    application.run_polling()

if __name__ == "__main__":
    main()
