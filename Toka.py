import discord
from discord.ext import commands

#intents

intents = discord.Intents().all()
bot = description= "description du bot" 
bot = commands.Bot(command_prefix="!", intents=intents)

# profil du bot 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Je fonctionne correctement !")


@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()



@bot.event
async def on_ready():
	print("Ready !")

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")




@bot.command()
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
	#await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", url = "https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber", color=0xfa8072)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber")
	embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
	embed.add_field(name = "Membre banni", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	embed.set_footer(text = random.choice(funFact))

	await ctx.send(embed = embed)



@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"`{serverName}` contient {numberOfPerson} membres. \n La description du serveur est {serverDescription}. \n {serverName} contient {numberOfTextChannels} salon textuel et {numberOfVoiceChannels} salon vocaux"
    await ctx.send(message)
    
bot.run("Put your Token here")
