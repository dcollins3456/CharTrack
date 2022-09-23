#from contextlib import nullcontext
import nextcord
import pickle
from nextcord import Interaction
from nextcord.ext import commands
import discord
import imgkit
#from html2image import Html2Image
#hti = Html2Image()
import dotenv
#from discord import File
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
        self.xppb = 0
        self.xp1 = 0
        self.xp2 = 0
        self.xp3 = 0
        self.items = ["", "", "", "", ""]
        self.hunt = 0
        self.study = 0
        self.survey = 0
        self.tinker = 0
        self.finesse = 0
        self.prowl = 0
        self.skirmish = 0
        self.wreck = 0
        self.attune = 0
        self.command = 0
        self.consort = 0
        self.sway = 0
        self.profilepic = "testport01.png"
        self.playbookxp = "0"
        self.insightxp = "0"
        self.prowessxp = "0"
        self.resolvexp = "0"

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

def checkcharlist():
    if path.exists('characterlist.pkl') == True:
        print("\nfound characterlist.pkl...")
    
    else: 
        characterlist = list()
        with open ('characterlist.pkl', 'wb') as file:
            characterlist = list()
            print ("dumping characterlist object to file...")
            pickle.dump(characterlist, file)

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
        print(f"SAVECHARLIST: characterlist updated. characterlist = {characterlist}")

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

def displaystatus(nickname:str):
    filename = nickname+".pkl"
    thischar = openchar(filename)
        
    itemline1 = thischar.items[0]
    itemline2 = thischar.items[1]
    itemline3 = thischar.items[2]
    itemline4 = thischar.items[3]
    itemline5 = thischar.items[4]

    atribs = [
    "<img src=\"a0.png\" /> <img src=\"a0.png\" /><img src=\"a0.png\" /><img src=\"a0.png\" />", 
    "<img src=\"a1.png\" /> <img src=\"a0.png\" /><img src=\"a0.png\" /><img src=\"a0.png\" />", 
    "<img src=\"a1.png\" /> <img src=\"a1.png\" /><img src=\"a0.png\" /><img src=\"a0.png\" />", 
    "<img src=\"a1.png\" /> <img src=\"a1.png\" /><img src=\"a1.png\" /><img src=\"a0.png\" />",
    "<img src=\"a1.png\" /> <img src=\"a1.png\" /><img src=\"a1.png\" /><img src=\"a1.png\" />"]
    
    hunt_atrib = atribs[thischar.hunt]
    study_atrib = atribs[thischar.study]
    survey_atrib = atribs[thischar.survey]
    tinker_atrib = atribs[thischar.tinker]
    finesse_atrib = atribs[thischar.finesse]
    prowl_atrib = atribs[thischar.prowl]
    skirmish_atrib = atribs[thischar.skirmish]
    wreck_atrib = atribs[thischar.wreck]
    attune_atrib = atribs[thischar.attune]
    command_atrib = atribs[thischar.command]
    consort_atrib = atribs[thischar.consort]
    sway_atrib = atribs[thischar.sway]
    
    harm3_1=""
    harm2_2=""
    harm2_1=""
    harm1_2=""
    harm1_1=""

    if len(thischar.harm1) > 0:
        harm1_1 = thischar.harm1[0]
    if len(thischar.harm1) > 1:
        harm1_2 = thischar.harm1[1]
    if len(thischar.harm2) > 0:
        harm2_1=thischar.harm2[0]
    if len(thischar.harm2) > 1:
        harm2_2=thischar.harm2[1]
    if len(thischar.harm3) > 0:
        harm3_1=thischar.harm3[0]
        
    if thischar.stress > 5:
        stresscracks = 1;
        if thischar.stress > 7:
            stresscracks = 2;
    else:
        stresscracks = 0;

    htmlbody=f"""
        <!DOCTYPE html>
            <html>
                <head>
                     <link rel="stylesheet" href="styles.css">
                </head>
            <body>
                <div class="maindiv">
                    <div class="title">{thischar.charname}</div>\n
                    <div class="portraitbg">\n
                        <div class="footer">Use <span class="crimson">'{thischar.safename}'</span> to interact</div>\n
                        <div class="sub">\n
                            <div class="playbookbig"><div class="the">the </div>{thischar.playbook}</div>\n
                        </div>\n
                    </div>\n
                    <div class="stress"><img src="stress{thischar.stress}.png" /></div>\n
                    <div class="tracker">\n
                        <div class="harm3_1">{harm3_1}</div>\n
                        <div class="harm2_2">{harm2_2}</div>\n
                        <div class="harm2_1">{harm2_1}</div>\n
                        <div class="harm1_2">{harm1_2}</div>\n
                        <div class="harm1_1">{harm1_1}</div>\n
                    </div>\n
                    <div class="tracker item">\n
                        <div class="harm3_1">{itemline1}</div>\n
                        <div class="harm2_2">{itemline2}</div>\n
                        <div class="harm2_1">{itemline3}</div>\n
                        <div class="harm1_2">{itemline4}</div>\n
                        <div class="harm1_1">{itemline5}</div>\n
                    </div>\n
                    <div class="attributes">\n
                        <div class="attribs one">{hunt_atrib}</div>\n
                        <div class="attribs one">{study_atrib}</div>\n
                        <div class="attribs one">{survey_atrib}</div>\n
                        <div class="attribs one">{tinker_atrib}</div>\n
                        <div class="attribs two">{finesse_atrib}</div>\n
                        <div class="attribs two">{prowl_atrib}</div>\n
                        <div class="attribs two">{skirmish_atrib}</div>\n
                        <div class="attribs two">{wreck_atrib}</div>\n
                        <div class="attribs three">{attune_atrib}</div>\n
                        <div class="attribs three">{command_atrib}</div>\n
                        <div class="attribs three">{consort_atrib}</div>\n
                        <div class="attribs three">{sway_atrib}</div>\n
                    </div>
                    <div class="portrait">\n
                        <img src="{thischar.profilepic}" />\n
                        <img class="stresscracks" src="cracks{stresscracks}.png" />\n
                    </div>\n
                    <div class="playbook"><img src="pb{thischar.playbookxp}.png" /></div>\n
                    <div class="pbtitle">playbook</div>\n
                    <div class="xp xp1"><img src="xp{thischar.insightxp}.png" /></div>\n
                    <div class="xp xp2"><img src="xp{thischar.prowessxp}.png" /></div>\n
                    <div class="xp xp3"><img src="xp{thischar.resolvexp}.png" /></div>\n
                </div>\n                 
            </body>\n
        </html>\n
    """
    #async def charcardcreate()
    charhtml = open("GRAPHICS/charcard.html","w")
    charhtml.write(htmlbody)
    charhtml.close()

    options = {'format': 'png', 'width': 800, 'height': 350, 'enable-local-file-access': "",'allow': os.path.join(os.path.dirname(__file__), 'templates') }
    imgkit.from_file("GRAPHICS/charcard.html", 'GRAPHICS/charcard.jpg', options=options)
    
    imgfile = nextcord.File('GRAPHICS/charcard.jpg')
    return imgfile

@client.slash_command(name="new", description="Make a new Player Character, linked to you")
async def newchar(interaction: Interaction, name:str, playbook:str):
    name = name.title()
    playbook = playbook.title()
    thischar = pchar(name, playbook)
    characterlist = opencharlist()
    nickname = thischar.safename
    
    if path.exists(f"GRAPHICS/{thischar.safename}.png"):
        thischar.profilepic = f"{thischar.safename}.png"
    elif path.exists(f"GRAPHICS/{thischar.safename}.jpg"):
        thischar.profilepic = f"{thischar.safename}.jpg"
    else:
        #profile pic not found, assigning default
        thischar.profilepic = "testport01.png"

    charfile = nickname+".pkl"
    print(f"\n- - - - - - -\nNew character created: {name} ( '{thischar.safename}' ), the {playbook}\nby {interaction.user.name}\n- - - - - - -\n")
    characterlist.append(charfile)
    savechar(charfile, thischar)
    savecharlist(characterlist, 'characterlist.pkl')
    await interaction.response.send_message((f"Character Created: **{thischar.charname}** ( '{thischar.safename}' ), the {playbook}"))


@client.slash_command(name="setnick", description="Allows renaming of a Character's input name")
async def setnick(interaction: Interaction, nickname:str, newnick:str):
    characterlist = opencharlist()
    print(f"SETNICK: characterlist at beginning of op: {characterlist}")
    filename = nickname+".pkl"
    thischar = openchar(filename)
    thischar.safename = newnick.lower()
    if path.exists(f"GRAPHICS/{thischar.safename}.png"):
        thischar.profilepic = f"{thischar.safename}.png"
        print(f"NICKNAME: profile pic exists as PNG")
    elif path.exists(f"GRAPHICS/{thischar.safename}.jpg"):
        thischar.profilepic = f"{thischar.safename}.jpg"
        print(f"NICKNAME: profile pic exists as JPG")
    else:
        #profile pic not found, assigning default
        thischar.profilepic = "testport01.png"
        print(f"NICKNAME: No Portrait file, \"{thischar.safename}\", detected, using default")
    #dump file
    charfile = newnick+".pkl"
    oldfile = nickname+".pkl"
    os.remove(oldfile)
    savechar(charfile, thischar)
    print(f"SETNICK: characterlist before append = {characterlist}")
    characterlist.append(charfile)
    characterlist.remove(oldfile)
    print(f"SETNICK: characterlist after append/delete = {characterlist}")
    await interaction.response.send_message(f"{thischar.charname} nickname updated to {newnick}")



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
    charfile = nickname+".pkl"
    thischar = openchar(charfile)
    message = "Harm processed"
    embed=discord.Embed(title=message, color=0xAA2255)
    invalid = False
    
    def addharm1(description):
        thischar.harm1.insert(0, description)
        if len(thischar.harm1) > 1:
            pass    
        if len(thischar.harm1) > 2:
            addharm2(thischar.harm1.pop())
           
    def addharm2(description):
        thischar.harm2.insert(0, description) 
        if len(thischar.harm2) > 1:
            pass          
        if len(thischar.harm2) > 2:
            addharm3(thischar.harm2.pop())
            ("ADDHARM: Former level 2_2 harm bumped up to level 3_1 harm.")
              
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
    
    savechar(charfile, thischar)    
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)
    if len(thischar.harm3) > 1:
        grab = thischar.harm3[1]
        thischar.harm3.clear()
        thischar.harm3.append(grab)
        #dump file
        charfile = nickname+".pkl"
        savechar(charfile, thischar)
        message = "**LEVEL 4 HARM!!**"
        desc = "Incur permanent, catastrophic, or fatal harm"
        embed=discord.Embed(title=message, description=desc, color=0xAA2255)
        await interaction.followup.send(embed=embed)
    if invalid == True:
        await interaction.followup.send(message)
    
@client.slash_command(name="setxp", description="Set Player Character experience track to desired value")
async def setxp(interaction: Interaction, nickname:str, track:str, value:int):
    filename = nickname+".pkl"
    thischar = openchar(filename)
    invalid = False
    track = track.lower()
    if 0 <= value <= 6 and (track == "1" or track == "insight"):
        thischar.insightxp = value
    elif 0 <= value <= 6 and (track == "2" or track == "prowess"):
        thischar.prowessxp = value
    elif 0 <= value <= 6 and (track == "3" or track == "resolve"):
        thischar.resolvexp = value
    elif 0<= value <= 8 and (track == "4" or track == "playbook"):
        thischar.playbookxp = value
    else:
        message = "**INVALID ENTRY | NO CHANGES MADE**, please use \"Insight\", \"Prowess\", \"Resolve\", or \"Playbook\", and an appropriate number value."
        invalid = True

    #dump file
    charfile = nickname+".pkl"
    savechar(charfile, thischar)
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)
    if invalid == True:
        await interaction.followup.send(message)

@client.slash_command(name="setload", description="Edit individual line items in Load Tracker (\"na\" or \"none\" for blank line")
async def setload(interaction: Interaction, nickname:str, line:int, desc:str):
    filename = nickname+".pkl"
    thischar = openchar(filename)
    invalid = False

    if (1 <= line <= 5) and len(desc) <= 40:
        num = line - 1
        thischar.items[num] = desc
        if desc.lower() == "na" or desc == "none":
            thischar.items[num] = ""
    else:
        message = "**INVALID ENTRY | NO CHANGES MADE**, please use line_number 1-5, and keep entries under 40 characters per line."
        invalid = True

    #dump file
    charfile = nickname+".pkl"
    savechar(charfile, thischar)
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)
    if invalid == True:
        await interaction.followup.send(message)

@client.slash_command(name="setaction", description="Define an action with a new value")
async def setaction(interaction: Interaction, nickname:str, action:str, value:int):
    filename = nickname+".pkl"
    thischar = openchar(filename)
    invalid = False
    action = action.lower()

    if 0 <= value <= 4:
        if action.lower() == "hunt":
            thischar.hunt = value
        elif action.lower() == "study":
            thischar.study = value
        elif action.lower() == "survey":
            thischar.survey = value
        elif action.lower() == "tinker":
            thischar.tinker = value  
        elif action.lower() == "finesse":
            thischar.finesse = value
        elif action.lower() == "prowl":
            thischar.prowl = value
        elif action.lower() == "skirmish":
            thischar.skirmish = value
        elif action.lower() == "wreck":
            thischar.wreck = value  
        elif action.lower() == "attune":
            thischar.attune = value
        elif action.lower() == "command":
            thischar.command = value
        elif action.lower() == "consort":
            thischar.consort = value
        elif action.lower() == "sway":
            thischar.sway = value
        else: 
            message = "**INVALID ENTRY | NO CHANGES MADE**, please use proper action name, and a value from 0-4."
            invalid = True
    else:
        message = "**INVALID ENTRY | NO CHANGES MADE**, please use proper action name, and a value from 0-4."
        invalid = True

    #dump file
    charfile = nickname+".pkl"
    savechar(charfile, thischar)
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)
    if invalid == True:
        await interaction.followup.send(message)

@client.slash_command(name="setstress", description="Define stress level for Player Character")
async def setstress(interaction: Interaction, nickname:str, stress:int):
    filename = nickname+".pkl"
    thischar = openchar(filename)
    invalid = False
    if 0 <= stress <= 8:
        thischar.stress = stress
    else: 
        message = "**INVALID ENTRY | NO CHANGES MADE**, please enter stress value 0-8."
        invalid = True

    #dump file
    charfile = nickname+".pkl"
    savechar(charfile, thischar)
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)
    if invalid == True:
        await interaction.followup.send(message)

@client.slash_command(name="status", description="Presents a PC's status")
async def getstatus(interaction: Interaction, nickname:str):
    
    imgfile = displaystatus(nickname)
    await interaction.response.send_message(file=imgfile)


@client.event
async def on_ready():
    print("--------------------------")
    print("CharTrack bot is on track.")
    print("--------------------------")
    print(f"Test Sever ID = {testServerID}")

# Creates 'characterlist.pkl' file if it does not exist, or loads it, if it does exist.   



checkcharlist()
opencharlist()
    
client.run(botkey)

