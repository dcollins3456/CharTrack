from contextlib import nullcontext
import nextcord
import pickle
from nextcord import Interaction
from nextcord.ext import commands
import discord
import os
from os import path
from dotenv import load_dotenv
load_dotenv()
botkey = os.getenv("DISCORD_TOKEN")
intents = nextcord.Intents.default()

testServerID:int = 1019312655384727657

client = commands.Bot(command_prefix = "!", intents=intents)

characterlist = list()

class pchar:
    def __init__(self, charname, playbook):
        self.charname = charname
        self.safename = scrub(charname)
        self.playbook = playbook
        self.stress = 0
        self.harm1 = list()
        self.harm2 = list()
        self.harm3 = list()
        self.xpmain = 0
        self.xp1 = 0
        self.xp2 = 0
        self.xp3 = 0

def scrub(namepass:str):
    result = namepass.split()
    res=[]
    for i in result:
        if(i.startswith('"') and i.endswith('"')):
            i=i.replace('"',"")
            res.append(i)
            
    if res == []:
        print("NO NICKNAME DETECTED, using first name")
        res = result
    cleanname = res
    cleanname = cleanname[0].lower()
    print(f"SCRUB: cleanname = '{cleanname}'")
    return cleanname

def opencharlist():
    with open ('characterlist.pkl', 'rb') as file:
        characterlist = pickle.load(file)
        listlen = len(characterlist)
        print (f"OPENCHARLIST: characterlist loaded from file, length: {listlen}")
    return characterlist

def savecharlist(characterlist, filename):

    with open(filename, "wb") as file:
        pickle.dump(characterlist, file)
        listlen = len(characterlist)
        print(f"SAVECHARLIST: characterlist updated. Total characters in list = {listlen}")

def savechar(charfile, thischar):
    with open(charfile, 'wb') as file:
        pickle.dump(thischar, file)
        print(f"SAVECHAR: {thischar.charname} saved to {charfile}.")

def openchar(character:str):
    charfile = character
    with open (charfile, 'rb') as file:
        thischar = pickle.load(file)
        print (f"OPENCHAR: {thischar.charname} loaded from {charfile}.")
    return thischar

def buildstatusembed(thischar):
    embed=discord.Embed(title=(f"**{thischar.charname}** ( '{thischar.safename}' ) : {thischar.playbook}"), description=(f"Stress: {thischar.stress}"), color=0x720e4d)
    if len(thischar.harm1) >= 1:
        embed.add_field(name="Harm Lvl.1: [Less Effect]", value=thischar.harm1[0], inline=False)
    if len(thischar.harm1) > 1:
        embed.add_field(name="Harm Lvl.1: [Less Effect] ", value=thischar.harm1[1], inline=True)
    if len(thischar.harm2) >= 1:
        embed.add_field(name="Harm Lvl.2: [ -1d ]", value=thischar.harm2[0], inline=False)
    if len(thischar.harm2) > 1:
        embed.add_field(name="Harm Lvl.2: [ -1d ]", value=thischar.harm2[1], inline=True)
    if len(thischar.harm3) >= 1:
        embed.add_field(name="Harm Lvl.3: [ Requires Help ]", value=thischar.harm3[0], inline=False)
    return embed

@client.slash_command(name="new", description="Make a new Player Character, linked to you")
async def newchar(interaction: Interaction, name:str, playbook:str):
    name = name.title()
    playbook = playbook.title()
    thischar = pchar(name, playbook)
    characterlist = opencharlist()
    nickname = thischar.safename
    charfile = nickname+".pkl"
    print(f"\n- - - - - - -\nNew character created: {name} ( '{thischar.safename}' ), the {playbook}\nby {interaction.user.name}\n- - - - - - -\n")
    characterlist.append(charfile)
    savechar(charfile, thischar)
    savecharlist(characterlist, 'characterlist.pkl')
    await interaction.response.send_message((f"Character Created: **{thischar.charname}** ( '{thischar.safename}' ), the {playbook}"))
    
@client.slash_command(name="listall", description="Displays a list of all registered Player Characters and nicknames.")
async def listall(interaction: Interaction):
    embed=discord.Embed(title="PLAYER CHARACTERS | Nicknames", color=0x720e4d)
    characterlist = opencharlist()
    i=0
    length = len(characterlist)
    print(f"LISTALL: loaded characterlist length: {length}")

    if length == 0:
        embed.add_field(name="ERROR: no Player Characters were found", value=None, inline=False)
    else:
        while i < length:
            filename = characterlist[i]
            thischar = openchar(filename)
            print(f"added filename: {filename}")
            embed.add_field(name=thischar.charname, value=thischar.safename, inline=False)
            i=i+1
    await interaction.response.send_message(embed=embed)

@client.slash_command(name="addharm", description="Add harm to a Player Character")
async def addharm(interaction: Interaction, nickname:str, level:int, description:str):    #open file
    filename = nickname+".pkl"
    thischar = openchar(filename)
    message = "Harm processed"
    embed=discord.Embed(title=message, color=0xAA2255)
    invalid = False
    
    def addharm1(description):
        thischar.harm1.insert(0, description)        
        if len(thischar.harm1) > 2:
            addharm2(thischar.harm1.pop())

    def addharm2(description):
        thischar.harm2.insert(0, description)        
        if len(thischar.harm2) > 2:
            addharm3(thischar.harm2.pop())

    def addharm3(description):
        thischar.harm3.insert(0, description)        
            
    if level == 1:
        addharm1(description)
    elif level == 2:
        addharm2(description)
    elif level == 3:
        addharm3(description)
    else:
        message = "**INVALID HARM LEVEL**, please use 1, 2, or 3."
        invalid = True
        embed=discord.Embed(title=message, color=0xDD0000)
        
    #dump file
    charfile = nickname+".pkl"
    savechar(charfile, thischar)
    statusembed = buildstatusembed(thischar)
    await interaction.response.send_message(embed=statusembed)
    if len(thischar.harm3) > 1:
        grab = thischar.harm3[0]
        thischar.harm3.clear()
        thischar.harm3.append(grab)
        print(f"ADDHARM3: shortened thischar.harm3 to: {thischar.harm3}")
        message = "**LEVEL 4 HARM!!**"
        desc = "Incur permanent, catastrophic, or fatal harm"
        embed=discord.Embed(title=message, description=desc, color=0xAA2255)
        await interaction.followup.send(embed=embed)
    if invalid == True:
        await interaction.followup.send(embed=embed)
    

@client.slash_command(name="status", description="Presents a PC's status")
async def displaystatus(interaction: Interaction, nickname:str):
    filename = nickname+".pkl"
    thischar = openchar(filename)
    statusembed = buildstatusembed(thischar)
    await interaction.response.send_message(embed=statusembed)
    
@client.slash_command(name="nickname", description="Allows renaming of a Character's input name")
async def nickname(interaction: Interaction, nickname:str, newnick:str):
    #open file
    filename = nickname+".pkl"
    thischar = openchar(filename)
    #change nickname
    thischar.nickname = newnick.lower()
    #dump file
    charfile = newnick+".pkl"
    savechar(charfile, thischar)
    await interaction.response.send_message(f"{thischar.charname} nickname updated to {newnick}")

@client.event
async def on_ready():
    print("--------------------------")
    print("CharTrack bot is on track.")
    print("--------------------------")
    print(f"Test Sever ID = {testServerID}")

# Creates 'characterlist.pkl' file if it does not exist, or loads it, if it does exist.   

def checkcharlist():
    if path.exists('characterlist.pkl') == True:
        print("\nfound characterlist.pkl...")
    
    else: 
        characterlist = list()
        with open ('characterlist.pkl', 'wb') as file:
            print ("dumping characterlist object to file...")
            pickle.dump(characterlist, file)

checkcharlist()
opencharlist()
    
client.run(botkey)

