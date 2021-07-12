import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

questions_words = ["questions", "question", "why", "Why", "How", "how"]

starter_questions = [
    "If you have any question please check out our Frequently Asked Questions: https://www.assistant-courrier.laposte.fr/faq"
]

hello_words = [
    "Hello", "Hi", "Goodmorning", "Good afternoon", "What's up", "hi", "hello"
]

starter_hello = [
    "It's a beautiful day, isn't it?\nWhat can I do for you?\n\nTap 'colis' with your Parcel or Mail number to have the following.",
    "How are you doing today?\nWhat can I do for you?\n\nTap 'colis' with your Parcel or Mail number to have the following.all",
    "Hello! \nHow can I help you?\n\nTap 'colis' with your Parcel or Mail number to have the following.",
    "Little hey little ho!\nWhat can I do for you?\n\nTap 'colis' with your Parcel or Mail number to have the following."
    "Welcome in ElizaBot!\nWhat can I do for you?\n\nTap 'colis' with your Parcel or Mail number to have the following."
]

recla_words = ["reclamation","reclamations","Reclamation","Reclamations","recla"]

starter_recla = ["If you want to do a reclamation check the following link : https://aide.laposte.fr/professionnel/contenu/comment-contacter-ou-reclamer-aupres-du-service-clients-de-laposte-fr?t=cc"]

starter_encouragement = ["ok"]

thanks_words = ["thanks", "thank you", "Thanks", "Thank", "Thank you", "thank"]

starter_thanks = ["Your welcome. \nPlease checkout our newsletter to still be informed: https://elisabot.com/newsletter\n\nYou have time ? \nTap '$new' to grade us from 1 to 10 and enter how was your experience with Eliza"]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        msg = message.content

        if any(word in msg for word in hello_words):
            await message.channel.send(random.choice(starter_hello))

        if msg.startswith('$inspire'):
            quote = get_quote()
            await message.channel.send(quote)

        if any(word in msg for word in questions_words):
            await message.channel.send(random.choice(starter_questions))

        if db["responding"]:
            options = starter_encouragement
            if "encouragements" in db.keys():
                options.extend(db["encouragements"])

            if any(word in msg for word in thanks_words):
                await message.channel.send(random.choice(starter_thanks))


        if msg.startswith("$new"):
            encouraging_message = msg.split("$new ", 1)[1]
            update_encouragements(encouraging_message)
            await message.channel.send("Your score has been send.\nThank you!\nFeel free to ask me whenever you need! \n\n A robot never sleep!")

        if msg.startswith("$del"):
            encouragements = []
            if "encouragements" in db.keys():
                index = int(msg.split("$del", 1)[1])
                delete_encouragement(index)
                encouragements = db["encouragements"]
            await message.channel.send(encouragements)

        if msg.startswith("$list"):
            encouragements = []
            if "encouragements" in db.keys():
                encouragements = db["encouragements"]
            await message.channel.send(encouragements)

        if msg.startswith("$responding"):
            value = msg.split("$responding ", 1)[1]

            if value.lower() == "true":
                db["responding"] = True
                await message.channel.send("Responding is on.")
            else:
                db["responding"] = False
                await message.channel.send("Responding is off.")


        if any(word in msg for word in recla_words):
                await message.channel.send(random.choice(starter_recla))

        if msg.startswith("colis"):
            param = msg.split("colis ", 1)[1]

            headers_dict = {
                "Accept":
                "application/json",
                "X-Okapi-Key":
                "3z3Pusvey/bbEZpKwfCeeeXqF6g/l7m3GEF5VVYlxkHIYy2VZKsjIokzopM91B/o"
            }
            response = requests.get(
                "https://api.laposte.fr/suivi/v2/idships/"+param,
                headers=headers_dict)
            json_data = json.loads(response.text)
            print(json_data['returnMessage']+'\n'+json_data['idShip'])

            await message.channel.send(json_data['returnMessage']+'\n'+json_data['idShip']+"\n\nTap 'question' and enter if you have one.\nTap 'reclamation' if you want to make a request.\nTap 'thanks' if you have finished.")
#1A00915820380

keep_alive()
client.run('ODQzODMyMzk4NjM4MjE5Mjg1.YKJmKQ.kDomZlho-rzHLlhNM8RBCkJUKsg')
