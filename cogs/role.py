from typing import overload


VILLAGER="村人"
WOLF="人狼"

class Role:
    def __init__(self,name=None,team=None,forecast=None):
        """役職クラス
        Args:
            name (str, optional): 役職名. 初期値:None.\n
            team (str, optional): 所属陣営. 初期値:None.\n
            forecast (str, optional): 占い結果. 初期値:None.\n
        """
        self.name=name
        self.team=team
        self.forecast=forecast
        self.survivor=True #生存フラグ

    def isSurvival(self):
        #生存しているかどうか
        return self.survivor

    def death(self):
        #生存フラグを折る
        self.survivor=False

    def reset(self):
        self.survivor=True


class Villager(Role):
    def __init__(self):
        super().__init__(name="村人", team=VILLAGER, forecast=VILLAGER)


class Seer(Role):
    def __init__(self):
        super().__init__(name="占い師", team=VILLAGER, forecast=VILLAGER)

    def getForecast(self,memberRole,member):
        """占い結果を取得する

        Args:
            memberRole (dict): プレイヤーと役職の辞書型配列
            member (discord.Member): 占いたいプレイヤー

        Returns:
            str: 占い結果(VILLAGER or WOLF)
        """
        return memberRole[member].forecast

class Knight(Role):
    def __init__(self):
        super().__init__(name="騎士", team=VILLAGER, forecast=VILLAGER)
        self.protect  = None

    def setProtect(self,member):
        """守るプレイヤーを設定

        Args:
            member (discord.Member): 守るプレイヤー
        """
        self.protect = member

    def isProtect(self,member):
        """指定したプレイヤーを守っているか

        Args:
            member (discord.Member): 守っているか確認したいプレイヤー

        Returns:
            bool: 守っているかどうか
        """
        if self.isSurvival():
            return self.protect == member
        return False

    def reset(self):
        self.survivor = True
        self.protect  = None

class Medium(Role):
    def __init__(self):
        super().__init__(name="霊媒師", team=VILLAGER, forecast=VILLAGER)

    def getForecast(self,memberRoles,member):
        """霊媒結果を取得する

        Args:
            memberRole (dict): プレイヤーと役職の辞書型配列
            member (discord.Member): 霊媒をしたいプレイヤー

        Returns:
            str: 霊媒結果(VILLAGER or WOLF)
        """
        return memberRoles[member].forecast

class Wolf(Role):
    def __init__(self):
        super().__init__(name="人狼", team=WOLF, forecast=WOLF)

class Madman(Role):
    def __init__(self):
        super().__init__(name="狂人", team=WOLF, forecast=VILLAGER)