import os
from datetime import datetime

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json

creds_json = os.environ.get("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope

)

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Pengeluaran")

def start(update, context):
    update.message.reply_text(
        "👋 Selamat datang!\n\n"
        "Gunakan format:\n"
        "Kategori | Nominal | Deskripsi\n\n"
        "Contoh:\n"
        "Makan & Minum | 35000 | Warteg Bu Sari"
    )
def handle_message(update, context):
    text = update.message.text

    if "|" not in text:
        update.message.reply_text(
            "❌ Format salah\n\n"
            "Gunakan:\n"
            "Kategori | Nominal | Deskripsi"
        )
        return

    try:
        kategori, nominal, deskripsi = [x.strip() for x in text.split("|", 2)]
        nominal = int(nominal)

        now = datetime.now()

        row = [
            now.strftime("%Y%m%d%H%M%S"),     # ID
            now.strftime("%Y-%m-%d"),         # Tanggal
            now.strftime("%H:%M:%S"),         # Waktu
            update.message.from_user.id,      # User_ID
            update.message.from_user.full_name,  # User_Nama
            kategori,                         # Kategori
            nominal,                          # Nominal
            deskripsi,                        # Deskripsi
            "Chat",                           # Sumber
            "Valid",                          # Status
            ""                                # Bukti
        ]

        sheet.append_row(row)

        update.message.reply_text(
            f"✅ Tersimpan\n\n"
            f"Kategori : {kategori}\n"
            f"Nominal  : Rp{nominal:,}\n"
            f"Catatan  : {deskripsi}"
        )

    except Exception:
        update.message.reply_text("❌ Gagal menyimpan data")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()






