import discord
from discord.ui import Button,View
from cogs.role import Role,Villager,Seer,Knight,Medium,Wolf,Madman

async def mainEmbed(game):
    embed = discord.Embed(title="人狼ゲーム",description="以下の状況でゲームをスタートします")
    embed.add_field(name="参加者",value=game.getMembers())
    embed.add_field(name="役職",value=game.getRoles())
    embed.add_field(name="議論時間",value=str(int(game.getTime()/60))+"分")

    joinBtn = Button(label="参加する",style=discord.ButtonStyle.green,emoji="🤚")
    leaveBtn = Button(label="退出する",style=discord.ButtonStyle.blurple,emoji="👋")
    confBtn = Button(label="設定する",style=discord.ButtonStyle.secondary,emoji="⚙")
    startBtn= Button(label="開始する",style=discord.ButtonStyle.green,emoji="🐺")
    endBtn= Button(label="終了する",style=discord.ButtonStyle.red,emoji="💥")

    async def join(interaction):
        game.addMembers(interaction.user)
        _embed,_ = await mainEmbed(game)
        await interaction.message.edit(embed=_embed)

    async def leave(interaction):
        game.subMembers(interaction.user)
        _embed,_ = await mainEmbed(game)
        await interaction.message.edit(embed=_embed)

    async def conf(interaction):
        _embed,_view = await configEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    async def start(interaction):
        _embed,_view = await startEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)
        _embed,_view = await game.gameProcess(interaction)
        await interaction.message.edit(embed=_embed,view=_view)

    async def end(interaction):
        _embed=discord.Embed(title="人狼ゲーム",description="ゲームを終了しました。")
        await interaction.message.edit(embed=_embed,view=View(timeout=600.0))

    view=View(timeout=600.0)
    view.add_item(joinBtn)
    view.add_item(leaveBtn)
    view.add_item(confBtn)
    view.add_item(startBtn)
    view.add_item(endBtn)

    joinBtn.callback = join
    leaveBtn.callback = leave
    confBtn.callback = conf
    startBtn.callback= start
    endBtn.callback = end
    return embed,view

async def configEmbed(game):
    embed = discord.Embed(title="人狼ゲーム",description="役職の人数・議論時間の変更ができます")
    result=""
    btnList=[]
    roles = [Villager(),Seer(),Knight(),Medium(),Wolf(),Madman()]
    for i,role in enumerate(roles):
        result += role.name+" "
        result += str(game.countRole(role)) +"人\n"
        btnList.append(Button(label=role.name,style=discord.ButtonStyle.gray,custom_id=str(i)))
    embed.add_field(name="役職",value=result)
    embed.add_field(name="議論時間",value=str(int(game.getTime()/60))+"分")

    async def option(interaction):
        roleId = int(interaction.data["custom_id"])
        _embed,_view = await optionEmbed(game,roles[roleId])
        await interaction.message.edit(embed=_embed,view=_view)

    timeBtn = Button(label="時間変更",style=discord.ButtonStyle.gray)

    async def timeOption(interaction):
        _embed,_view = await timeEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    backBtn= Button(label="戻る",style=discord.ButtonStyle.gray,emoji="⬅️")
    async def back(interaction):
        _embed,_view = await mainEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    view=View(timeout=600.0)
    for btn in btnList:
        view.add_item(btn)
        btn.callback = option
    view.add_item(timeBtn)
    timeBtn.callback=timeOption
    view.add_item(backBtn)
    backBtn.callback=back
    return embed,view

async def optionEmbed(game,role:Role):
    embed = discord.Embed(title="人狼ゲーム",description="役職の人数を変更します")
    result = str(game.countRole(role))+"人\n"
    embed.add_field(name=role.name,value=result)

    upBtn = Button(label="増やす",style=discord.ButtonStyle.gray,emoji="⬆️")
    downBtn= Button(label="減らす",style=discord.ButtonStyle.gray,emoji="⬇️")
    backBtn= Button(label="戻る",style=discord.ButtonStyle.gray,emoji="⬅️")

    async def up(interaction):
        game.addRoles(role)
        _embed,_ = await optionEmbed(game,role)
        await interaction.message.edit(embed=_embed)

    async def down(interaction):
        game.subRoles(role)
        _embed,_ = await optionEmbed(game,role)
        await interaction.message.edit(embed=_embed)

    async def back(interaction):
        _embed,_view = await configEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    view=View(timeout=600.0)
    view.add_item(upBtn)
    view.add_item(downBtn)
    view.add_item(backBtn)
    upBtn.callback = up
    downBtn.callback = down
    backBtn.callback = back

    return embed,view

async def timeEmbed(game):
    embed = discord.Embed(title="人狼ゲーム",description="議論時間を変更します")
    embed.add_field(name="議論時間",value=str(int(game.getTime()/60))+"分")
    btnList=[]
    btnList.append(Button(label="3分",style=discord.ButtonStyle.gray,custom_id="180"))
    btnList.append(Button(label="5分",style=discord.ButtonStyle.gray,custom_id="300"))
    btnList.append(Button(label="8分",style=discord.ButtonStyle.gray,custom_id="480"))
    backBtn= Button(label="戻る",style=discord.ButtonStyle.gray,emoji="⬅️")

    async def time(interaction):
        time = int(interaction.data["custom_id"])
        game.setTime(time)
        _embed = discord.Embed(title="人狼ゲーム",description="議論時間を変更します")
        _embed.add_field(name="議論時間",value=str(int(game.getTime()/60))+"分")
        await interaction.message.edit(embed=_embed)

    async def back(interaction):
        _embed,_view = await configEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    view=View(timeout=600.0)
    for btn in btnList:
        view.add_item(btn)
        btn.callback = time
    view.add_item(backBtn)
    backBtn.callback = back

    return embed,view


async def startEmbed(game):
    view = View(timeout=600.0)
    if game.setMemberRoles():
        embed = discord.Embed(title="人狼ゲーム",description="ゲームを開始します。しばらくお待ちください。")
        suv =""
        for mem,role in game.getMemberRoles().items():
            if role.isSurvival():
                suv += mem.mention+"\n"
            _embed,_view = await roleEmbed(game,mem,role)
            if mem.dm_channel == None:
                await mem.create_dm()
            await mem.dm_channel.send(embed=_embed,view=_view)
        roles=""
        for role in [Villager(),Seer(),Knight(),Medium(),Wolf(),Madman()]:
            roles += role.name+" "
            roles += str(game.countRole(role)) +"人\n"
        embed.add_field(name="生存者一覧",value=suv,inline=True)
        embed.add_field(name="役職一覧",value=roles,inline=True)
    else :
        embed,view = await mainEmbed(game)
        embed.add_field(name="エラー",value="プレイヤー人数と役職人数が一致しません。",inline=False)
    return embed,view

async def roleEmbed(game,member,role:Role):
    embed = discord.Embed(title="人狼ゲーム",description="あなたの役職は・・・・")
    embed.add_field(name=role.name+"です",value="あなたは"+role.team+"陣営です",inline=False)
    view = View(timeout=600.0)
    if isinstance(role,Villager):
        embed.add_field(name="役割",value="議論に参加して、人狼を見つけましょう。",inline=False)
    elif isinstance(role,Seer):
        embed.add_field(name="役割",value="毎晩、誰か一人の陣営を知ることができます。",inline=False)
        embed,view = await seerEmbed(game,member,role,embed)
    elif isinstance(role,Knight):
        embed.add_field(name="役割",value="毎晩、誰か一人を人狼の襲撃から護衛することができます。",inline=False)
        embed,view = await knightEmbed(game,member,role,embed)
    elif isinstance(role,Medium):
        embed.add_field(name="役割",value="毎朝、投票でつるされた人の陣営を知ることができます。",inline=False)
        embed,view = await mediumEmbed(game,role,embed)
    elif isinstance(role,Wolf):
        embed.add_field(name="役割",value="村人たちを恐怖に陥れましょう。",inline=False)
        embed,view = await wolfEmbed(game,member,embed)
    elif isinstance(role,Madman):
        embed.add_field(name="役割",value="村人たちを混乱させ、人狼を勝たせましょう。",inline=False)

    return embed,view

async def seerEmbed(game,member:Seer,role,embed:discord.Embed):
    view = View(timeout=600.0)
    roleDict = game.getMemberRoles()

    async def action(interaction):
        userId = interaction.data["custom_id"]
        user = game.id2member[userId]
        _embed = discord.Embed(title="人狼ゲーム",description="占いました")
        _embed.add_field(name="占い先",value=getNickname(user))
        _embed.add_field(name="占い結果",value=role.getForecast(roleDict,user))
        await interaction.message.edit(embed=_embed,view=View(timeout=600.0))
        game.countdownWait()

    embed.add_field(name="占い",value="誰を占いますか?")
    btnList = actionBtnList(game)
    for btn in btnList:
        userId = btn.custom_id
        user = game.id2member[userId]
        if roleDict[user].isSurvival():
            if userId != str(member.id):
                view.add_item(btn)
                btn.callback = action
    game.countupWait()
    return embed,view

async def knightEmbed(game,member,role:Knight,embed:discord.Embed):
    view = View(timeout=600.0)
    roleDict = game.getMemberRoles()
    async def action(interaction):
        userId = interaction.data["custom_id"]
        user = game.id2member[userId]
        role.setProtect(user)
        _embed = discord.Embed(title="人狼ゲーム",description="護衛しました！")
        _embed.add_field(name="護衛先",value=getNickname(user))
        await interaction.message.edit(embed=_embed,view=View(timeout=600.0))
        game.countdownWait()

    if game.getTurn() != 0:
        embed.add_field(name="護衛",value="誰を護衛しますか?")
        btnList = actionBtnList(game)
        for btn in btnList:
            userId = btn.custom_id
            user = game.id2member[userId]
            if roleDict[user].isSurvival():
                if userId != str(member.id):
                    if role.protect != None and userId != str(role.protect.id):
                        view.add_item(btn)
                        btn.callback = action
                    elif role.protect == None:
                        view.add_item(btn)
                        btn.callback = action
        game.countupWait()
    else:
        pass

    return embed,view

async def mediumEmbed(game,role:Medium,embed:discord.Embed):
    view = View(timeout=600.0)
    roleDict = game.getMemberRoles()

    if game.getTurn() != 0:
        user = game.lastVote
        embed = discord.Embed(title="人狼ゲーム",description="霊媒結果")
        embed.add_field(name="霊媒先",value=getNickname(user))
        embed.add_field(name="霊媒結果",value=role.getForecast(roleDict,user))
    else:
        pass
    return embed,view

async def wolfEmbed(game,member,embed:discord.Embed):
    view = View(timeout=600.0)
    roleDict = game.getMemberRoles()
    async def action(interaction):
        userId = interaction.data["custom_id"]
        user = game.id2member[userId]
        game.addWolfVote(user)
        _embed = discord.Embed(title="人狼ゲーム",description="襲撃しました！")
        _embed.add_field(name="襲撃先",value=getNickname(user))
        await interaction.message.edit(embed=_embed,view=View(timeout=600.0))
        game.countdownWait()

    if game.getTurn() != 0:
        embed.add_field(name="襲撃",value="誰を襲撃しますか?")
        btnList = actionBtnList(game)
        for btn in btnList:
            userId = btn.custom_id
            user = game.id2member[userId]
            if roleDict[user].isSurvival():
                if userId != str(member.id):
                    view.add_item(btn)
                    btn.callback = action
        game.countupWait()
    else:
        result = ""
        for mem,role in roleDict.items():
            if isinstance(role,Wolf) and mem!=member:
                result += mem.mention +"\n"
        if result == "":
            result = "誰もいませんでした・・・"
        else:
            result+="人狼同士、チャットでコミュニケーションをとりましょう！"
        embed.add_field(name="あなたの仲間は・・・",value=result)

    return embed,view

async def talkEmbed(game):
    view = View(timeout=600.0)
    embed = discord.Embed(title="人狼ゲーム")
    embed.add_field(name=str(game.getTurn()+1)+"日目 昼",value="話し合いを行ってください。",inline=False)
    suv =""
    death=""
    for mem,role in game.getMemberRoles().items():
        if role.isSurvival():
            suv += mem.mention+"\n"
        else:
            death += mem.mention+"\n"
    roles=""
    for role in [Villager(),Seer(),Knight(),Medium(),Wolf(),Madman()]:
        roles += role.name+" "
        roles += str(game.countRole(role)) +"人\n"
    embed.add_field(name="生存者一覧",value=suv,inline=True)
    if death != "":
        embed.add_field(name="死者一覧",value=death,inline=True)
    else:
        embed.add_field(name="死者一覧",value="なし",inline=True)
    embed.add_field(name="役職一覧",value=roles,inline=True)

    skipBtn = Button(label="投票を行う",style=discord.ButtonStyle.gray)

    async def skip(interaction):
        game.talkTime=0
        await interaction.message.edit(view=View(timeout=600.0))

    view.add_item(skipBtn)
    skipBtn.callback=skip

    return embed,view

async def endVoteEmbed(game):
    view = View(timeout=600.0)
    embed = discord.Embed(title="人狼ゲーム",description="投票が終わりました。")
    user=game.lastVote
    embed.add_field(name="投票の結果吊られたのは・・・・",value=getNickname(user)+"さんです")
    return embed,view

async def voteEmbed(game,member):
    view = View(timeout=600.0)
    roleDict = game.getMemberRoles()
    embed = discord.Embed(title="人狼ゲーム",description="投票をしてください")

    async def vote(interaction):
        userId = interaction.data["custom_id"]
        user = game.id2member[userId]
        game.addVote(user)
        _embed = discord.Embed(title="人狼ゲーム",description="投票しました！")
        _embed.add_field(name="投票先",value=getNickname(user))
        await interaction.message.edit(embed=_embed,view=View(timeout=600.0))
        game.countdownWait()

    btnList = actionBtnList(game)
    for btn in btnList:
        userId = btn.custom_id
        user = game.id2member[userId]
        if roleDict[user].isSurvival():
            if userId != str(member.id):
                view.add_item(btn)
                btn.callback = vote
    game.countupWait()
    return embed,view

async def sendVoteEmbed(game):
    for mem,role in game.getMemberRoles().items():
        if role.isSurvival():
            _embed,_view = await voteEmbed(game,mem)
            if mem.dm_channel == None:
                await mem.create_dm()
            await mem.dm_channel.send(embed=_embed,view=_view)

async def nightEmbed(game):
    view = View(timeout=600.0)
    embed = discord.Embed(title="人狼ゲーム",description=str(game.getTurn()+1)+"日目 夜")
    embed.add_field(name="夜になりました。",value="夜の行動を行ってください。")
    return embed,view

async def morningEmbed(game):
    view = View(timeout=600.0)
    embed = discord.Embed(title="人狼ゲーム")
    embed.add_field(name=str(game.getTurn()+1)+"日目 昼",value="話し合いを行ってください。",inline=False)
    if game.lastWolf!=None:
        embed.add_field(name="昨晩襲撃されたのは・・・",value=getNickname(game.lastWolf)+"さんです")
    else:
        embed.add_field(name="昨晩は・・・",value="襲撃されませんでした！！")
    return embed,view

async def endEmbed(game,result):
    view=View(timeout=600.0)
    embed = discord.Embed(title="人狼ゲーム",description="ゲームが終了しました！")
    embed.add_field(name="勝利したのは・・・",value=result+"陣営です！！")
    roleList = ""
    for mem,role in game.getMemberRoles().items():
        roleList += role.name+":"+getNickname(mem)+"\n"
    embed.add_field(name="役職一覧",value=roleList)
    restartBtn=Button(label="もう一度遊ぶ",emoji="🔄")
    async def restart(interaction):
        game.reset()
        _embed,_view = await mainEmbed(game)
        await interaction.message.edit(embed=_embed,view=_view)

    view.add_item(restartBtn)
    restartBtn.callback = restart
    return embed,view

async def sendNightEmbed(game):
    for mem,role in game.getMemberRoles().items():
        embed = discord.Embed(title="人狼ゲーム",description=str(game.getTurn()+1)+"日目 夜")
        if role.isSurvival():
            if isinstance(role,Seer):
                embed,view = await seerEmbed(game,mem,role,embed)
                await mem.dm_channel.send(embed=embed,view=view)
            elif isinstance(role,Knight):
                embed,view = await knightEmbed(game,mem,role,embed)
                await mem.dm_channel.send(embed=embed,view=view)
            elif isinstance(role,Medium):
                embed,view = await mediumEmbed(game,role,embed)
                await mem.dm_channel.send(embed=embed,view=view)
            elif isinstance(role,Wolf):
                embed,view = await wolfEmbed(game,mem,embed)
                await mem.dm_channel.send(embed=embed,view=view)

def actionBtnList(game):
    btnList=[]
    for mem in game.members:
        btnList.append(Button(label=getNickname(mem),style=discord.ButtonStyle.gray,custom_id=str(mem.id)))

    return btnList

def getNickname(member):
    if member.nick != None:
        return member.nick
    else:
        return member.name