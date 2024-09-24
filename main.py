import discord
import os 
import requests
import json
import random
from replit import db
from keepalive import keep_alive

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)
sad_words=["sad","depressed","unhappy","angry","miserable","depressing","bad"]

starter_encouragements = ["Cheer up!","Hang in there.","You are a great person!"]

if "responding" not in db:
  db["responding"] = True

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + " -" +json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db:
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(db["encouragements"])>index:
    del db["encouragements"][index]
    db["encoragements"]=encouragements 



@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
    
  if message.content.startswith("$hello"):
    await message.channel.send("Hello!")
    
  if message.content.startswith("$inspire"):
    quote=get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      encouragements_list = db["encouragements"]
      encouragements = list(encouragements_list)
      options = options + encouragements
      
    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

  if message.content.startswith("$new"):
    encouraging_message=message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(message.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements=[item for item in db["encouragements"]]
    await message.channel.send(encouragements)
    
  if message.content.startswith("$list"):
    encouragements=[]
    if bytes("encouragements", 'utf-8') in db.keys():
      encouragements = [item for item in db["encouragements"]]
    await message.channel.send(encouragements)

  if message.content.startswith("$responding"):
    value=message.content.split("$responding ",1)[1]

    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")

keep_alive()
if os.getenv('TOKEN') is None:
  print("Please set the TOKEN environment variable.")
  exit(1)
token=os.getenv('TOKEN')
client.run(token)