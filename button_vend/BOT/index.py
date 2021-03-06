from discord import user
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow
import discord, sqlite3, datetime, randomstring, os, setting, random
from discord_components.ext.filters import user_filter
import asyncio, requests, json
from setting import admin_id, webhook_profile_url, webhook_name, domain, bot_name
from datetime import timedelta
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType

client = discord.Client()

def get_roleid(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT roleid FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    if (str(data).isdigit()):
        return int(data)
    else:
        return data

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_buylogwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT buylogwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

@client.event
async def on_ready():
    DiscordComponents(client)

@client.event
async def on_message(message):
    if message.content.startswith('!?????? '):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            license_key = message.content.split(" ")[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
            search_result = cur.fetchone()
            con.close()
            if (search_result != None):
                if (search_result[2] == 0):
                    if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                        con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                        cur = con.cursor()
                        cur.execute("CREATE TABLE serverinfo (id TEXT, expiredate TEXT, cultureid TEXT, culturepw TEXT, pw TEXT, roleid TEXT, logwebhk TEXT, buylogwebhk TEXT, culture_fee TEXT, bank TEXT);")
                        con.commit()
                        first_pw = randomstring.pick(10)
                        cur.execute("INSERT INTO serverinfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (message.guild.id, make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])), "", "", first_pw, 0, "", "", 0, ""))
                        con.commit()
                        cur.execute("CREATE TABLE users (id INTEGER, money INTEGER, bought INTEGER);")
                        con.commit()
                        cur.execute("CREATE TABLE products (name INTEGER, money INTEGER, stock TEXT);")
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), message.guild.id, license_key))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        await message.author.send(embed=discord.Embed(title="?????? ?????? ??????", description="????????? ??????????????? ?????????????????????.\n???????????? ??????: `30`???\n?????????: `" + make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])) + f"`\n??? ??????: {domain}\n?????????: `" +str(message.guild.id) + "`\n????????????: `" + first_pw + "`", color=0x4461ff),
                        components = [
                            ActionRow(
                                Button(style=ButtonType().Link,label = "?????????",url=domain),
                            )
                        ]
                    )
                        await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description="????????? ??????????????? ?????????????????????.", color=0x4461ff))
                        con.close()
                    else:
                        await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ????????? ??????????????? ????????? ??? ????????????.\n?????? ????????? ??????????????? !???????????? ???????????? ??????????????????.", color=0x4461ff))
                else:
                    await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ????????? ?????????????????????.\n??????????????? ??????????????????.", color=0x4461ff))
            else:
                await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description="???????????? ?????? ?????????????????????.", color=0x4461ff))

    if message.content == '!??????':
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                await message.delete()
                embed = discord.Embed(title=bot_name, description='???????????? ????????? ??????????????????.', color=0x4461ff)
                await message.channel.send(
                    embed=embed,
                    components = [
                        ActionRow(
                            Button(style=ButtonStyle.blue,label = "??????",custom_id="??????"),
                            Button(style=ButtonStyle.blue,label = "??????",custom_id="??????"),
                            Button(style=ButtonStyle.blue,label = "??????",custom_id="??????"),
                            Button(style=ButtonStyle.blue,label = "??????",custom_id="??????"),
                        )
                    ]
                )

    if message.content == '!????????????':
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                embed = discord.Embed(title=bot_name, description='???????????? ????????? ??????????????????.', color=0x4461ff)
                await message.channel.send(
                    embed=embed,
                    components = [
                        ActionRow(
                            Button(style=ButtonStyle.blue,label = "??????",custom_id="??????"),
                            Button(style=ButtonStyle.blue,label = "?????????",custom_id="?????????"),
                        )
                    ]
                )

    if message.content.startswith("!???????????? "):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            try:
                userId = message.mentions[0].id
            except:
                userId = int(message.content.split(" ")[1])
            try:
                amount = message.content.split(" ")[2]
            except:
                return await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description="`!???????????? @???????????? ????????????` ?????? ??????????????????!", color=0x4461ff))
            con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (userId,))
            user_info = cur.fetchone()
            if not user_info:
                return await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description=f"???????????? ?????? ???????????????.", color=0x4461ff))
            current_money = int(user_info[1])
            now_money = current_money + int(amount)
            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, userId))
            con.commit()
            await message.channel.send(embed=discord.Embed(title="?????? ?????? ??????", description=f"?????????: {message.author}\n?????? ??????: `{current_money}`\n????????? ??????: `{amount}`\n?????? ??? ??????: `{now_money}`???", color=0x4461ff))

@client.event
async def on_button_click(interaction):
    if not isinstance(interaction.channel, discord.channel.DMChannel):
        if (os.path.isfile("../DB/" + str(interaction.guild.id) + ".db")):
            con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo;")
            cmdchs = cur.fetchone()
            con.close()
            try:
                tempvar = is_expired(cmdchs[1])
            except:
                os.rename("../DB/" + str(interaction.guild.id) + ".db", "../DB/" + str(interaction.guild.id) + f".db_old{datetime.datetime.now()}")
            if not(is_expired(cmdchs[1])):
                if interaction.responded:
                    return
                try:
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    if (user_info == None):
                        cur.execute("INSERT INTO users VALUES(?, ?, ?);", (interaction.user.id, 0, 0))
                        con.commit()
                        con.close()
                except:
                    pass
                if interaction.custom_id == "??????":
                    con = sqlite3.connect(f"../DB/{interaction.guild.id}.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM products;")
                    products = cur.fetchall()
                    con.close()
                    list_embed = discord.Embed(title="?????? ??????", color=0x4461ff)
                    for product in products:
                        list_embed.add_field(name=product[0], value="??????: `" + str(product[1]) + "`???\n??????: `" + str(len(product[2].split("\n"))) + "`???", inline=False)
                    await interaction.respond(embed=list_embed)
                if interaction.custom_id == "??????":
                    embed = discord.Embed(title='???????????? ??????', description='???????????? ??????????????? ??????????????????.', color=0x4461ff)
                    await interaction.respond(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.blue,label = "???????????????",custom_id="????????????"),
                                Button(style=ButtonStyle.blue,label = "????????????",custom_id="????????????"),
                            )
                        ]
                    )
                if interaction.custom_id == "????????????":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    cur.execute("SELECT * FROM serverinfo;")
                    server_info = cur.fetchone()
                    con.close()
                    if (server_info[2] != "" and server_info[3] != ""):
                            try:
                                await interaction.user.send(embed=discord.Embed(title="??????????????? ??????", description=f"??????????????? ???????????? -??? ???????????? ??????????????????.\n??????????????? ?????? ?????????: {server_info[8]}%", color=0x4461ff))
                                await interaction.respond(embed=discord.Embed(title="?????? ??????", description="DM??? ??????????????????.", color=0x4461ff))
                            except:
                                await interaction.respond(embed=discord.Embed(title="??????????????? ?????? ??????", description="DM??? ?????????????????? ????????? ?????? ????????? ????????????.", color=0x4461ff))
                                return None

                            def check(msg):
                                return (isinstance(msg.channel, discord.channel.DMChannel) and (len(msg.content) == 21 or len(msg.content) == 19) and (interaction.user.id == msg.author.id))
                            try:
                                msg = await client.wait_for("message", timeout=60, check=check)
                            except asyncio.TimeoutError:
                                try:
                                    await interaction.user.send(embed=discord.Embed(title="??????????????? ?????? ??????", description="?????? ?????????????????????.", color=0x4461ff))
                                except:
                                    pass
                                return None
                            
                            try:
                                jsondata = {"token" : setting.api_token, "id" : server_info[2], "pw" : server_info[3], "pin" : msg.content}
                                res = requests.post(setting.api, json=jsondata)
                                if (res.status_code != 200):
                                    raise TypeError
                                else:
                                    print(str(res))
                                    res = res.json()
                            except:
                                try:
                                    await interaction.user.send(embed=discord.Embed(title="??????????????? ?????? ??????", description="???????????? ?????? ???????????????.\n?????? ??? ?????? ??????????????????.", color=0x4461ff))
                                except:
                                    pass
                                return None

                            if (res["result"] == True):
                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM serverinfo WHERE id == ?;",(interaction.guild.id,))
                                guild_info = cur.fetchone()
                                culture_fee = int(guild_info[8])
                                culture_amount = int(res["amount"])
                                culture_amount_after_fee = culture_amount - int(culture_amount*(culture_fee/100))
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (msg.author.id,))
                                user_info = cur.fetchone()
                                current_money = int(user_info[1])
                                now_money = current_money + culture_amount_after_fee
                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, msg.author.id))
                                con.commit()
                                con.close()
                                try:
                                    await interaction.user.send(embed=discord.Embed(title="??????????????? ?????? ??????", description=f"?????????: `{msg.content}`\n??????: `{culture_amount}`???\n????????? ??????: `{culture_amount_after_fee}` (????????? {culture_fee}%)\n?????? ??? ??????: `{now_money}`???", color=0x3dce32).set_footer(text=interaction.guild.name))
                                    try:
                                        webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                        eb = DiscordEmbed(title='??????????????? ?????? ??????', description=f'[??? ????????? ????????????]({domain})', color=0x4461ff)
                                        eb.add_embed_field(name='???????????? ?????????', value=f"{msg.author}", inline=False)
                                        eb.add_embed_field(name='??? ??????', value=f"{msg.content}", inline=False)
                                        eb.add_embed_field(name='????????? ??????', value=f"`{culture_amount}`???", inline=False)
                                        eb.add_embed_field(name='????????? ??????', value=f"`{culture_amount_after_fee}`??? (????????? {culture_fee}%)", inline=False)
                                        webhook.add_embed(eb)
                                        webhook.execute()
                                    except:
                                        pass
                                except:
                                    pass
                            else:
                                try:
                                    await interaction.user.send(embed=discord.Embed(title="??????????????? ?????? ??????", description="[ " + res["reason"] + " ]", color=0x4461ff))
                                    try:
                                        webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                        eb = DiscordEmbed(title='??????????????? ?????? ??????', description=f'[??? ????????? ????????????]({domain})', color=0x4461ff)
                                        eb.add_embed_field(name='???????????? ?????????', value=str(msg.author), inline=False)
                                        eb.add_embed_field(name='??? ??????', value=str(msg.content), inline=False)
                                        eb.add_embed_field(name='?????? ??????', value=res["reason"], inline=False)
                                        webhook.add_embed(eb)
                                        webhook.execute()
                                    except Exception as e:
                                        await interaction.user.send(e)
                                except:
                                    pass
                    else:
                        await interaction.respond(embed=discord.Embed(title="??????????????? ?????? ??????", description="?????? ????????? ?????????????????? ????????????.\n??? ??????????????? ??????????????????.", color=0x4461ff))
                if interaction.custom_id == "????????????":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM serverinfo")
                    serverinfo = cur.fetchone()
                    con.close()
                    try:
                        bankdata = json.loads(serverinfo[9])
                        assert len(bankdata['banknum']) > 1
                    except Exception as e:
                        return await interaction.respond(embed=discord.Embed(title="???????????? ???????????? ??????", description="????????? ??????????????? ?????????????????? ????????????.\n??? ??????????????? ??????????????????.", color=0x4461ff))
                    try:
                        nam = await interaction.user.send(embed=discord.Embed(description=f"??????????????? ??????????????????.", color=0x4461ff))
                        await interaction.respond(embed=discord.Embed(title="?????? ??????", description="DM??? ??????????????????.", color=0x4461ff))
                        def check(name):
                            return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))
                        try:
                            name = await client.wait_for("message", timeout=60, check=check)
                            await nam.delete()
                            name = name.content
                        except asyncio.TimeoutError:
                            try:
                                await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ?????????????????????.", color=0x4461ff))
                            except:
                                pass
                            return None
                        mone = await interaction.user.send(embed=discord.Embed(description=f"????????? ????????? ??????????????????.", color=0x4461ff))
                        def check(money):
                            return (isinstance(money.channel, discord.channel.DMChannel) and (interaction.user.id == money.author.id))
                        try:
                            money = await client.wait_for("message", timeout=60, check=check)
                            await mone.delete()
                            money = money.content
                        except asyncio.TimeoutError:
                            try:
                                await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ?????????????????????.", color=0x4461ff))
                            except:
                                pass
                            return None
                        if money.isdigit():
                            await interaction.user.send(embed=discord.Embed(title="?????? ??????", description=f"```{bankdata.get('bankname')} {bankdata.get('banknum')} {bankdata.get('bankowner')}```?????? {money}?????? ?????? ?????????????????? ??????????????????.\n\n<@{interaction.user.id}>?????? ????????????: `{name}`", color=0x4461ff))
                        else:
                            await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description=f"????????? ????????? ??????????????????.", color=0x4461ff))
                    except Exception as e:
                        print(e)
                        return await interaction.respond(embed=discord.Embed(title="?????? ?????? ??????", description="DM??? ?????????????????? ????????? ?????? ????????? ????????????.", color=0x4461ff))
                    try:
                        if money.isdigit():
                            webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                            eb = DiscordEmbed(title='???????????? ?????? ??????', description=f'[??? ????????? ????????????]({domain})', color=0x4461ff)
                            eb.add_embed_field(name='???????????? ?????????', value=f"<@{interaction.user.id}>({interaction.user})", inline=False)
                            eb.add_embed_field(name='????????????', value=f"{name}", inline=False)
                            eb.add_embed_field(name='?????? ????????? ????????????', value=f"!???????????? <@{interaction.user.id}> {money}", inline=False)
                            webhook.add_embed(eb)
                            webhook.execute()
                    except:
                        pass
                if interaction.custom_id == "??????":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM products;")
                    products = cur.fetchall()
                    options = []
                    try:
                        for product in products:
                            options.append(SelectOption(description=str(product[1])+"???????????? "+str(len(product[2].split('\n')))+"???",label=product[0], value=product[0]))
                        gg = await interaction.user.send(embed=discord.Embed(title='?????? ??????', description='????????? ????????? ??????????????????.', color=0x4461ff)
                            ,
                            components = [
                                [Select(placeholder="????????????", options=options)]
                            ]
                        )
                        await interaction.respond(embed=discord.Embed(title="?????? ??????", description="DM??? ??????????????????.", color=0x4461ff))
                    except:
                        await interaction.respond(embed=discord.Embed(title="??????", description="????????? ????????????.", color=0x4461ff))
                    try:
                        event = await client.wait_for("select_option", timeout=30, check=None)
                        product_name = event.values[0]
                        await gg.delete()
                    except asyncio.TimeoutError:
                        gg.delete()
                        await interaction.user.send(embed=discord.Embed(title='?????? ??????', description='?????? ??????', color=0x4461ff))
                        return
                    cur.execute("SELECT * FROM products WHERE name = ?;", (str(product_name),))
                    product_info = cur.fetchone()
                    if (product_info != None):
                        if (str(product_info[2]) != ""):
                            info_msg = await interaction.user.send(embed=discord.Embed(title="?????? ??????", description="???????????? ????????? ????????? ??????????????????.", color=0x4461ff))
                            def check(msg):
                                return (msg.author.id == interaction.user.id)
                            try:
                                msg = await client.wait_for("message", timeout=20, check=check)
                            except asyncio.TimeoutError:
                                try:
                                    await info_msg.delete()
                                except:
                                    pass
                                await interaction.user.send(embed=discord.Embed(title="?????? ??????", description="???????????? ?????? ??????????????????.", color=0x4461ff))
                                return None

                            try:
                                await info_msg.delete()
                            except:
                                pass
                            try:
                                await msg.delete()
                            except:
                                pass
                            
                            if not msg.content.isdigit() or int(msg.content) == 0:
                                await interaction.user.send(embed=discord.Embed(title="?????? ??????", description="????????? ???????????? ??????????????????.", color=0x4461ff))
                                return None

                            buy_amount = int(msg.content)

                            if (len(product_info[2].split("\n")) >= buy_amount):
                                if (int(user_info[1]) >= int(product_info[1] * buy_amount)):
                                    try_msg = await interaction.user.send(embed=discord.Embed(title="?????? ?????? ????????????..", color=0x4461ff))
                                    stocks = product_info[2].split("\n")
                                    bought_stock = []
                                    for n in range(buy_amount):
                                        picked = random.choice(stocks)
                                        bought_stock.append(picked)
                                        stocks.remove(picked)
                                    now_stock = "\n".join(stocks)
                                    now_money = int(user_info[1]) - (int(product_info[1]) * buy_amount)
                                    now_bought = int(user_info[2]) + (int(product_info[1]) * buy_amount)
                                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                    cur = con.cursor()
                                    cur.execute("UPDATE users SET money = ?, bought = ? WHERE id == ?;", (now_money, now_bought, interaction.user.id))
                                    con.commit()
                                    cur.execute("UPDATE products SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                    con.commit()
                                    con.close()
                                    bought_stock = "\n".join(bought_stock)
                                    if (len(bought_stock) > 1000):
                                        con = sqlite3.connect("../DB/docs.db")
                                        cur = con.cursor()
                                        docs_name = randomstring.pick(30)
                                        cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                        con.commit()
                                        con.close()
                                        docs_url = f"{domain}/rawviewer/" + docs_name
                                        try:
                                            try:
                                                webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                                eb = DiscordEmbed(title='?????? ?????? ??????', description=f'[??? ????????? ????????????]({domain})', color=0x4461ff)
                                                eb.add_embed_field(name='???????????? ?????????', value=str(interaction.user), inline=False)
                                                eb.add_embed_field(name='?????? ??????', value=str(product_name), inline=False)
                                                eb.add_embed_field(name='?????? ??????', value='[????????? ?????? ??????](' + docs_url + ')', inline=False)
                                                webhook.add_embed(eb)
                                                webhook.execute()
                                            except:
                                                pass

                                            try:
                                                webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_buylogwebhk(interaction.guild.id))
                                                webhook.add_embed(DiscordEmbed(description="<@" + str(interaction.user.id) + ">" + "???, `" + product_name + "` ?????? `" + str(buy_amount) + "`??? ?????? ???????????????! :thumbsup:"))
                                                webhook.execute()
                                            except:
                                                pass
                                            try:
                                                buyer_role = interaction.guild.get_role(get_roleid(interaction.guild.id))
                                                await interaction.user.add_roles(buyer_role)
                                            except:
                                                pass
                                            await interaction.user.send(embed=discord.Embed(title="????????? ?????????????????????!", color=0x4461ff).add_field(name="???????????? ??????", value="`" + product_name + "`", inline=False).add_field(name="???????????? ??????", value='[????????? ?????? ??????](' + docs_url + ')', inline=False).add_field(name="?????? ??????", value="`" + str(int(product_info[1]) * buy_amount) + "`???", inline=False).set_footer(text=interaction.guild.name))
                                        except:
                                            try:
                                                await try_msg.delete()
                                            except:
                                                await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ?????? ??? ??? ??? ?????? ????????? ??????????????????.\n??? ??????????????? ??????????????????.", color=0x4461ff))

                                    else:
                                        try:
                                            try:
                                                webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_logwebhk(interaction.guild.id))
                                                eb = DiscordEmbed(title='?????? ?????? ??????', description=f'[??? ????????? ????????????]({domain})', color=0x4461ff)
                                                eb.add_embed_field(name='???????????? ?????????', value=str(interaction.user), inline=False)
                                                eb.add_embed_field(name='?????? ??????', value=str(product_name), inline=False)
                                                eb.add_embed_field(name='?????? ??????', value=bought_stock, inline=False)
                                                webhook.add_embed(eb)
                                                webhook.execute()
                                            except:
                                                pass

                                            try:
                                                webhook = DiscordWebhook(username=webhook_name, avatar_url=webhook_profile_url, url=get_buylogwebhk(interaction.guild.id))
                                                webhook.add_embed(DiscordEmbed(description="<@" + str(interaction.user.id) + ">" + "???, `" + product_name + "` ?????? `" + str(buy_amount) + "`??? ?????? ???????????????!", color=0x4461ff))
                                                webhook.execute()
                                            except:
                                                pass

                                            try:
                                                buyer_role = interaction.guild.get_role(get_roleid(interaction.guild.id))
                                                await interaction.user.add_roles(buyer_role)
                                            except:
                                                pass

                                            await try_msg.edit(embed=discord.Embed(title="????????? ?????????????????????!", color=0x4461ff).add_field(name="???????????? ??????", value="`" + product_name + "`", inline=False).add_field(name="???????????? ??????", value="`" + str(bought_stock) + "`", inline=False).add_field(name="?????? ??????", value="`" + str(int(product_info[1]) * buy_amount) + "`???", inline=False).set_footer(text=interaction.guild.name))
                                        except:
                                            try:
                                                await try_msg.delete()
                                            except:
                                                pass
                                            await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="?????? ?????? ??? ??? ??? ?????? ????????? ??????????????????.\n??? ??????????????? ??????????????????.", color=0x4461ff))
                                else:
                                    await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="????????? ???????????????.", color=0x4461ff))
                            else:
                                await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="????????? ???????????????.", color=0x4461ff))
                        else:
                            await interaction.user.send(embed=discord.Embed(title="?????? ?????? ??????", description="????????? ???????????????.", color=0x4461ff))

                if interaction.custom_id == "??????":
                    con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.author.id,))
                    user_info = cur.fetchone()
                    await interaction.respond(embed=discord.Embed(title=str(interaction.user.name) + "?????? ??????", description="?????? ??????: `" + str(user_info[1]) + "`???\n?????? ??????: `" + str(user_info[2]) + "`???", color=0x4461ff))

                if interaction.custom_id == "??????":
                    if interaction.user.guild_permissions.administrator or interaction.author.id == int(admin_id):
                        await interaction.user.send(embed=discord.Embed(description="??????????????? ??????????????????.", color=0x4461ff))
                        await interaction.respond(embed=discord.Embed(description="DM??? ??????????????????.", color=0x4461ff))
                        def check(license_key):
                            return (license_key.author.id == interaction.user.id and isinstance(license_key.channel, discord.channel.DMChannel))
                        license_key = await client.wait_for("message", timeout=30, check=check)
                        license_key = license_key.content
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        search_result = cur.fetchone()
                        con.close()
                        if (search_result != None):
                            if (search_result[2] == 0):
                                con = sqlite3.connect("../DB/" + "license.db")
                                cur = con.cursor()
                                cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), str(interaction.guild.id), license_key))
                                con.commit()
                                cur = con.cursor()
                                cur.execute("SELECT * FROM license WHERE code == ?;",(license_key,))
                                key_info = cur.fetchone()
                                con.close()
                                con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM serverinfo;")
                                server_info = cur.fetchone()
                                if (is_expired(server_info[1])):
                                    new_expiretime = make_expiretime(key_info[1])
                                else:
                                    new_expiretime = add_time(server_info[1], key_info[1])
                                cur.execute("UPDATE serverinfo SET expiredate = ?;", (new_expiretime,))
                                con.commit()
                                con.close()
                                await interaction.user.send(embed=discord.Embed(description=f"{key_info[1]}?????? ?????????????????????.", color=0x4461ff))
                            else:
                                await interaction.user.send(embed=discord.Embed(description="?????? ????????? ?????????????????????.", color=0x4461ff))
                        else:
                            await interaction.user.send(embed=discord.Embed(description="???????????? ?????? ?????????????????????.", color=0x4461ff))

                if interaction.custom_id == "?????????":
                    if interaction.user.guild_permissions.administrator or interaction.author.id == int(admin_id):
                        con = sqlite3.connect("../DB/" + str(interaction.guild.id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM serverinfo;")
                        server_info = cur.fetchone()
                        await interaction.respond(embed=discord.Embed(title="????????? ??????", description="?????????: `" + server_info[1] + f"`\n??? ??????: {domain}\n?????????: `" +str(interaction.guild.id) + "`\n????????????: `" + server_info[4] + "`", color=0x4461ff))

client.run(setting.token)