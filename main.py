import asyncio
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot


Bot = commands.Bot(command_prefix = ";")


Warns = []
Citations = []


def GetRole(Guild, Name):
    Role = discord.utils.get(Guild.roles, name=Name)
    return Role
def GetChannel(Guild, Name):
    Channel = discord.utils.get(Guild.channels, name=Name)
    return Channel
def IsModerator(Guild, Member):
    Role = GetRole(Guild, "Server Moderator")
    for HasRoles in Member.roles:
        if Role == HasRoles:
            return True

def IsAdmissions(Guild, Member):
    Role = GetRole(Guild, "Admissions Mod")
    for HasRoles in Member.roles:
        if Role == HasRoles:
            return True


async def DM(Member, Text, Embed):
    try:
        if Embed:
            await Bot.send_message(Member, embed=Text)
        else:
            await Bot.send_message(Member, Text)
    except:
        pass

          



def LogMessage(Moderator, Victim, Action, Reason):
    Title = Action + " by " + Moderator
    Description = Action + " for\n``` - " + Reason + "```"
    Embed = discord.Embed(title=Title, description=Description, type="rich", color = 0xFF0000)
    Embed.add_field(name="Mod", value = Moderator, inline=False)
    Embed.add_field(name="User", value = Victim, inline=False)
    Embed.add_field(name="Punishment", value = Action, inline=False)
    return Embed

def AdmissionsLog(Moderator, Victim, Action, Reason):
    Title = Action + " by " + Moderator
    Description = Action + " for\n``` - " + Reason + "```"
    Embed = discord.Embed(title=Title, description=Description, type="rich", color = 0xFF0000)
    Embed.add_field(name="Mod", value = Moderator, inline=False)
    Embed.add_field(name="User", value = Victim, inline=False)
    Embed.add_field(name="Punishment", value = Action, inline=False)
    return Embed

async def citate(From,Victim, Reason):
    Embeded = AdmissionsLog(From.name, "Citation", Reason)
    await DM(Victim, Embeded, True)
    await Bot.send_message(GetChannel(Victim.server,"citation_logs"), embed=Embeded)

async def suspend(From,Victim,Reason):
    Embeded = AdmissionsLog(From.name, "Suspsension", Reason)
    await DM(Victim,Embeded,True)
    await Bot.send_message(GetChannel(Victim.server,"suspend_logs"), embed=Embeded)

async def Mute(From, Victim, Reason):
    for VictimRoles in Victim.roles:
        await Bot.remove_roles(Victim, VictimRoles)
    MutedRole = GetRole(Victim.server, "Muted")
    await Bot.add_roles(Victim, MutedRole)

    Embeded = LogMessage(From.name, Victim.name, "Mute", Reason)    
    await DM(Victim, Embeded, True)
    await Bot.send_message(GetChannel(Victim.server, "joint_logs"), embed=Embeded)
    



async def Warn(From, Victim, Reason):
    Embeded = LogMessage(From.name, Victim.name, "Warn", Reason)
    await DM(Victim, Embeded, True)
    await Bot.send_message(GetChannel(Victim.server, "joint_logs"), embed=Embeded)
    print(Warns)

async def Kick(From, Victim, Reason):

    await Bot.kick(Victim)
    Embeded = LogMessage(From.name, Victim.name, "Kick", Reason)
    await DM(Victim, Embeded, True)
    await Bot.send_message(GetChannel(Victim.server, "joint_logs"), embed=Embeded)
    
async def Unmute(Member):
    for MemberRoles in Member.roles:
        await Bot.remove_roles(MemberRoles)




@Bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    Message = reaction.message
    Guild = Message.server
    Channel = Message.channel
    Victim = Guild.get_member(Message.author.id)
    Member = Guild.get_member(reaction)
    if reaction.emoji.name == "warn":
        print("xD")
        if "402221315693477888" in [y.id for y in user.roles]:
            await Warn(user, Victim, "Player said: " + Message.clean_content)
            await Bot.delete_message(Message)
            Warns.append (Victim.id)
    if reaction.emoji.name == "kick":
        if "402221315693477888" in [y.id for y in user.roles]:
            await Kick(user, Victim, "Player said: " + Message.clean_content)
            await Bot.delete_message(Message)
    else:
        print("no")
        
@Bot.command(pass_context=True)
async def warn(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild, Member):
            Victim = Message.mentions[0]
            Reason = Message.content[9+len(Message.raw_mentions[0]): len(Message.content)]
            await Warn(Member, Victim, Reason)
            await Bot.delete_message(Message)
            Warns.append (Victim.id)
            kick = Warns.count(Victim.id)
            if kick == 3:
                await Kick(Member, Victim, Reason)
            else:
                print("Good egg")
    except:
        pass


@Bot.command(pass_context=True)
async def citate(Context):
    Message = Context.message
    Guild = Message.server
    Member = Guild.get_member(Message.author.id)
    if Member and IsAdmissions(Guild, Member):
        Victim = Message.mentions[0]
        Reason = Message.content[9+len(Message.raw_mentions[0]): len(Message.content)]
        await citate(Member, Victim, Reason)
        await Bot.delete_message(Message)
        Citations.append (Victim.id)
        suspend = Citations.count(Victim.id)
        if suspend == 3:
            await suspend(Member, Victim, Reason)
        else:
            print("Good admissions bleh")


@Bot.command(pass_context=True)
async def suspend(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsAdmissions(Guild, Member):
            Victim = Message.mentions[0]
            Reason = Message.content[9+len(Message.raw_mentions[0]): len(Message.content)]
            await suspend(Member, Victim, Reason)
            await Bot.delete_message(Message)
    except:
        pass

        
@Bot.command(pass_context=True)
async def mute(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild, Member):
            Victim = Message.mentions[0]
            Reason = Message.content[9+len(Message.raw_mentions[0]): len(Message.content)]
            await Mute(Member, Victim, Reason)
            await Bot.delete_message(Message)
    except:
        pass


@Bot.command(pass_context=True)
async def kick(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild, Member):
            Victim = Message.mentions[0]
            Reason = Message.content[9+len(Message.raw_mentions[0]): len(Message.content)]
            await Kick(Member, Victim, Reason)
            await Bot.delete_message(Message)
    except:
        pass


@Bot.command(pass_context=True)
async def clearwarns(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild, Member):
            Victim = Message.mentions[0]
            for Occurence in Warns:
                if Occurence == Victim.id:
                    Warns.remove(Victim.id)
            await Bot.send_message(Message.channel, "Warnings cleared for " + Victim.name)
    except:
        pass

@Bot.command(pass_context=True)
async def chat(ctx, *, message : str):
    if ctx.message.author.id == "224533422654095360":
        await Bot.delete_message(ctx.message)
        await Bot.say(message)
    else:
        return  
        
@Bot.command(pass_context=True)
async def checkwarns(Context):
    Message = Context.message
    Guild = Message.server
    Victim = Message.mentions[0]
    Channel = Message.channel
    WarningsGiven = Warns.count(Victim.id)
    UserWarningGiven = Warns.count(Message.author.id)
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild,Member):
            await Bot.send_message(Channel, "<@" + Message.author.id + "> they have " + str(WarningsGiven) + " warning(s).")
        
        else:
            await Bot.send_message(Channel, "<@" + Message.author.id + "> you have " + str(UserWarningGiven) + " warning(s).")
    except:
        pass

@Bot.command(pass_context=True)
async def citationcount(Context):
    Message = Context.message
    Guild = Message.server
    Victim = Message.mentions[0]
    Channel = Message.channel
    CitationsGiven = Citations.count(Victim.id)
    UserCitationsGiven = Citations.count(Message.author.id)
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsAdmissions(Guild,Member):
            await Bot.send_message(Channel, "<@" + Message.author.id + "> they have " + str(CitationsGiven) + " citation(s).")
        
        else:
            await Bot.send_message(Channel, "<@" + Message.author.id + "> you have " + str(UserCitationsGiven) + " citation(s).")
    except:
        pass


@Bot.command(pass_context=True)
async def clear(Context):
    Message = Context.message
    Guild = Message.server
    try:
        Member = Guild.get_member(Message.author.id)
        if Member and IsModerator(Guild, Member):
            MessagesToDelete = int(Message.content[7:len(Message.content)])
            await Bot.delete_message(Message)
            await Bot.purge_from(Message.channel, limit=MessagesToDelete)
    except:
        pass


print("Running")
if not os.environ.get('TOKEN'):
    print("no token found!")
Bot.run(os.environ.get('TOKEN').strip('"'))
