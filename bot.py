# bot.py
import feedparser
import os
from telegram import Bot, ParseMode

# Configurazioni dalle variabili d'ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")
RSS_URL = os.getenv("RSS_URL")

# Memoria delle offerte già inviate (in RAM per ora)
sent_links = set()

def aggiungi_tag_affiliato(link):
    if "tag=" in link:
        return link
    separatore = "&" if "?" in link else "?"
    return f"{link}{separatore}tag={AFFILIATE_TAG}"

def invia_offerte():
    bot = Bot(token=BOT_TOKEN)
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries[:5]:
        titolo = entry.title
        link = aggiungi_tag_affiliato(entry.link)

        if link in sent_links:
            continue

        messaggio = f"📦 *{titolo}*\n🔗 [Acquista ora]({link})"
        try:
            bot.send_message(chat_id=CHAT_ID, text=messaggio, parse_mode=ParseMode.MARKDOWN)
            print(f"Inviato: {titolo}")
            sent_links.add(link)
        except Exception as e:
            print(f"Errore: {e}")

if __name__ == "__main__":
    invia_offerte()
