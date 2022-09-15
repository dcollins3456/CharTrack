from contextlib import nullcontext
import nextcord
import pickle
from nextcord import Interaction
from nextcord.ext import commands
import os
from os import path
from dotenv import load_dotenv
load_dotenv()
botkey = os.getenv("DISCORD_TOKEN")
intents = nextcord.Intents.default()

testServerID:int = 1019312655384727657

client = commands.Bot(command_prefix = "!", intents=intents)

def scrub(namepass:str):
    cleanname = namepass.replace('"','')
    print(f"Scrubbed a name: {cleanname}")
    #MAKE THIS USE NICKNAME IN QUOTES AS OUTPUT, OR FIRST NAME IF NO QUOTES
    return cleanname.split()[0]

async def savecharlist(listfile):
    with open(listfile, "wb") as file:
        pickle.dump(characterlist, file)
        listlen = len(characterlist)
        print(f"characterlist updated. Total characters in list = {listlen}")

async def savechar(charfile):
    with open(charfile, 'wb') as file:
        pickle.dump(thischar, file)
        print(f"Character file, {file}, has been created.")

class pchar:
    def __init__(self, charname, playbook):
        self.charname = charname
        self.safename = scrub(charname)
        self.playbook = playbook
        self.stress = 0
        self.harm1_1 = None
        self.harm1_2 = None
        self.harm2_2 = None
        self.harm3 = None
        self.xpmain = 0
        self.xp1 = 0
        self.xp2 = 0
        self.xp3 = 0


# Creates 'characterlist.pkl' file if it does not exist, or loads it, if it does exist.   
if path.exists('characterlist.pkl') == True:
    print("\nfound characterlist.pkl...")
    with open ('characterlist.pkl', 'rb') as file:
        characterlist = pickle.load(file)
        listlen = len(characterlist)
        print (f"characterlist loaded from file, length: {listlen}")
        print (f"characterlist = {characterlist}")
else:
    characterlist = []
    with open ('characterlist.pkl', 'wb') as file:
        print ("dumping characterlist object to file...")
        pickle.dump(characterlist, file)



@client.slash_command(name="new", description="Make a new Player Character, linked to you")
async def generatechar(interaction: Interaction, name:str, playbook:str):
    thischar = pchar(name, playbook)
    nickname = scrub(name)
    charfile = nickname+".pkl"
    listfile = 'characterlist.pkl'
    print(f"\n- - - - - - -\nNew character created: {name}\n- - - - - - -\nby {interaction.user.name}")
    characterlist.append(charfile)
    savechar(charfile)
    savecharlist(listfile)

    

    with open(charfile, 'wb') as file:
        pickle.dump(thischar, file)
        print(f"Character file, {file}, has been created.")
    
    await interaction.channel.send(f'Character Created:\n{thischar.charname}\nstress: {thischar.stress}')


@client.slash_command(name="status", description="Presents a PC's status")
async def displaystatus(interaction: Interaction, name:str):
    
    await interaction.response.send_message(f"status report request for {name}.pkl")

@client.slash_command(name="adopt", description="Takes ownership of a Player Character")
async def adoptchar(interaction: Interaction, name:str):

    await interaction.response.send_message("User ____ now has control of _____ ")

@client.event
async def on_ready():
    print("--------------------------")
    print("CharTrack bot is on track.")
    print("--------------------------")
    print(f"Test Sever ID = {testServerID}")

client.run(botkey)

