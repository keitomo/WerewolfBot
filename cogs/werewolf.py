import asyncio
from cogs.createEmbed import morningEmbed, nightEmbed, sendNightEmbed, sendVoteEmbed, talkEmbed,endVoteEmbed,endEmbed
from cogs.role import VILLAGER, WOLF
from cogs.role import Role,Villager,Seer,Knight,Medium,Wolf,Madman
import random
import discord
import statistics
import copy

class WerewolfGame:

    def __init__(self):
        self.members=list() #プレイヤーリスト
        self.roles=list() #役職リスト
        self.memberRoles=dict() #プレイヤーと役職の辞書
        self.turn=0 #現在のターン数を取得
        self.id2member=dict()
        self.voteList = list()
        self.wolfVoteList = list()
        self.lastVote=None #投票でつるされた人(霊媒師用)
        self.lastWolf=None #人狼に襲撃された人
        self.waitCount=0 #各役職の処理を待つための変数
        self.time = 180
        self.talkTime = 0

    def getTurn(self):
        return self.turn

    def countupTurn(self):
        self.turn+=1
        return self.turn

    def getTime(self):
        return self.time

    def setTime(self,time):
        self.time = time

    def countupWait(self):
        self.waitCount+=1

    def countdownWait(self):
        self.waitCount-=1

    def getMembers(self):
        """登録されているプレイヤーの文字列を返す

        Returns:
            str: 登録されているプレイヤーの文字列
        """
        result = "だれもいません"
        for mem in self.members:
            if result == "だれもいません":
                result = mem.mention
            else:
                result += mem.mention
            result += "\n"
        return result

    def getRoles(self):
        """登録されている役職の文字列を返す

        Returns:
            str: 登録されている役職の文字列
        """
        result = "設定されていません"
        for role in self.roles:
            if result == "設定されていません":
                result = role.name
            else:
                result += role.name
            result += "\n"
        return result

    def countRole(self,role):
        """役職が何人いるか数える

        Args:
            role (Role): 数えたい役職

        Returns:
            int: 役職の数
        """
        return sum(isinstance(r,role.__class__) for r in self.roles)

    def addMembers(self,member:discord.Member):
        """プレイヤーを追加する関数

        Args:
            member (discord.Member): 追加するプレイヤー
        """
        if not member in self.members:
            self.members.append(member)

    def subMembers(self,member:discord.Member):
        """プレイヤーを削除する関数

        Args:
            member (discord.Member): 削除するプレイヤー
        """
        if member in self.members:
            self.members.remove(member)

    def addRoles(self,role:Role):
        """役職を追加する関数

        Args:
            role (Role): 追加する役職
        """
        self.roles.append(copy.deepcopy(role))

    def subRoles(self,role:Role):
        """役職を削除する関数

        Args:
            role (Role): 削除する役職
        """
        for r in self.roles:
            if isinstance(r,role.__class__):
                self.roles.remove(r)
                return

    def setRoles(self,roles:list):
        """役職を一括追加する関数（初期化も行う）

        Args:
            roles (list): 追加する役職リスト(Role型)
        """
        self.roles=roles

    def setMemberRoles(self):
        """役職を割り振る関数
        """
        if len(self.roles)==len(self.members):
            self.memberRoles.clear
            random.seed()
            #役職リストをシャッフル
            random.shuffle(self.roles)
            for i,mem in enumerate(self.members):
                self.memberRoles[mem] = self.roles[i]
                self.id2member[str(mem.id)]=mem
            return True
        else:
            return False

    def getMemberRoles(self):
        """プレイヤーと役職の辞書配列を取得する関数

        Returns:
            dict: プレイヤーと役職の辞書配列 {discord.Member:Role}
        """
        return self.memberRoles

    def resetRole(self):
        """人数に合わせて初期役職を決めてくれる関数（4~9人まで対応、10人以上は9人の役職配置になる）
        """
        memberCount = len(self.members)
        if memberCount<=3:
            return
        elif memberCount == 4:
            self.setRoles([Villager(),Villager(),Wolf(),Seer()])
        elif memberCount == 5:
            self.setRoles([Villager(),Villager(),Villager(),Wolf(),Seer()])
        elif memberCount == 6:
            self.setRoles([Villager(),Villager(),Knight(),Wolf(),Madman(),Seer()])
        elif memberCount == 7:
            self.setRoles([Villager(),Villager(),Knight(),Medium(),Wolf(),Madman(),Seer()])
        elif memberCount == 8:
            self.setRoles([Villager(),Villager(),Knight(),Medium(),Wolf(),Wolf(),Madman(),Seer()])
        else :
            self.setRoles([Villager(),Villager(),Villager(),Knight(),Medium(),Wolf(),Wolf(),Madman(),Seer()])

    def isEndGame(self):
        """ゲームが終了したか確認する関数

        Returns:
            bool,str:ゲームの終了をtrue/falseで返す,優勝したチームをstrで返す
        """
        wolfCount = 0 #生存している人狼の人数を保持
        villCount = 0 #生存している村人の人数を保持
        for role in self.getMemberRoles().values():
            #全プレイヤーのRoleを取得
            if role.isSurvival():
                #生存していたら
                if role.forecast == VILLAGER:
                    #占い結果がVILLAGER
                    villCount+=1
                elif role.forecast == WOLF:
                    #占い結果がWOLF
                    wolfCount+=1
        if wolfCount==0:
            #生存している人狼が0人なら
            #村人陣営の勝ち
            return True,VILLAGER
        if wolfCount>=villCount:
            #生存している人狼と村陣営の人数が同じなら
            #人狼陣営の勝ち
            return True,WOLF
        return False,None

    def killMember(self,member,vote=False):
        """プレイヤーを処刑する関数

        Args:
            member (discord.Member): 処刑するプレイヤー
            vote (bool): 投票による処刑かどうか.人狼による処刑の場合はFalse.
        """
        result=False
        if vote:
            #投票による処刑の場合
            self.memberRoles[member].death() #処刑
            result = True
        else:
            #人狼による殺害の場合
            knightList =[] #騎士一覧
            isProtect=False #騎士が守っているかどうか
            for role in self.memberRoles.values():
                if isinstance(role,Knight):
                    #役職が騎士なら
                    knightList.append(role)
            #騎士がmemberを守っているのか確認
            for knight in knightList:
                if isProtect==False:
                    #騎士がまだ守っていなかったら
                    isProtect=knight.isProtect(member) #騎士が守っているか確認
            if not isProtect:
                #騎士が守っていなかったら
                self.memberRoles[member].death() #殺害
                result=True
        return result

    def voteProcess(self):
        """投票処理を行う
        """
        random.shuffle(self.voteList)
        member = statistics.mode(self.voteList)
        self.killMember(member,True)
        self.lastVote=member
        self.voteList.clear()

    def wolfVoteProcess(self):
        """人狼の襲撃処理を行う
        """
        random.shuffle(self.wolfVoteList)
        member = statistics.mode(self.wolfVoteList)
        result = self.killMember(member)
        if result:
            self.lastWolf=member
        else:
            self.lastWolf=None
        self.wolfVoteList.clear()

    def addVote(self,member):
        self.voteList.append(member)

    def addWolfVote(self,member):
        self.wolfVoteList.append(member)

    async def gameProcess(self,interaction):
        """ゲームの処理を行う
        """
        isEnd=False
        result=None
        while True:
            if self.waitCount==0:
                await asyncio.sleep(5)
            while self.waitCount!=0:
                await asyncio.sleep(1)
            isEnd , result = self.isEndGame()
            if isEnd :
                await asyncio.sleep(5)
                embed,view = await endEmbed(self,result)
                await interaction.message.edit(embed=embed,view=view)
                break
            embed,view=await talkEmbed(game=self)
            self.talkTime = self.time
            embed.add_field(name="残り時間",value=str(self.talkTime))
            await interaction.message.edit(embed=embed,view=view)
            while self.talkTime>0:
                embed.set_field_at(4,name="残り時間",value=str(self.talkTime))
                self.talkTime -= 1
                await interaction.message.edit(embed=embed)
                await asyncio.sleep(1)
                if self.talkTime<=0:
                    embed.set_field_at(4,name="残り時間",value="時間切れ！")
                    await interaction.message.edit(embed=embed)

            await sendVoteEmbed(game=self)

            if self.waitCount==0:
                await asyncio.sleep(5)
            while self.waitCount!=0:
                await asyncio.sleep(1)

            self.voteProcess()
            embed,view = await endVoteEmbed(game=self)
            await interaction.message.edit(embed=embed,view=view)

            isEnd , result = self.isEndGame()
            await asyncio.sleep(5)
            if isEnd :
                break
            else:
                self.countupTurn()
                embed,view= await nightEmbed(game=self)
                await interaction.message.edit(embed=embed,view=view)
                await asyncio.sleep(5)
                await sendNightEmbed(self)
                if self.waitCount==0:
                    await asyncio.sleep(5)
                while self.waitCount!=0:
                    await asyncio.sleep(1)
                self.wolfVoteProcess()
                await asyncio.sleep(5)
                embed,view=await morningEmbed(game=self)
                await interaction.message.edit(embed=embed,view=view)
                await asyncio.sleep(5)

        embed,view = await endEmbed(self,result)
        return embed,view

    def reset(self):
        self.memberRoles.clear()
        self.turn=0
        self.lastVote=None
        self.lastWolf=None
        for role in self.roles:
            role.reset()