# main.py
import tweepy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

class LightStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        url = f"https://twitter.com/i/status/{tweet.id}"
        requests.post(DISCORD_WEBHOOK, json={"content": url})
        print(f"Enviado: {url}")

    def on_error(self, error):
        print(f"Erro: {error}")

print("Bot iniciado | ≥50 likes | Apenas link")

stream = LightStream(BEARER_TOKEN)

if stream.get_rules().data:
    stream.delete_rules([r.id for r in stream.get_rules().data])

rule = ('("crypto ambassador" OR "web3 ambassador" OR "blockchain ambassador" OR '
        '"ambassador program" crypto OR web3 OR "looking for ambassadors" crypto OR web3 OR '
        '"join as ambassador" crypto OR web3) lang:en -is:retweet min_faves:50')

stream.add_rules(tweepy.StreamRule(value=rule, tag="crypto-ambassador"))

stream.filter()
