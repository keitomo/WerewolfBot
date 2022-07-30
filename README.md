# WerewolfBot

Discordで人狼ゲームのGMをやってくれるBot

## 特徴

- Buttonを使用したわかりやすいUI
  ![](image/README/1659200032414.png)
- 議論時間をカウントしてくれる
- セルフホスティング可能なので、（構築できれば）いつでも遊べる

## 実行環境

- Python 3.10以降
- 必要ライブラリはrequirements.txt内に記載

## 実行方法

- 必要なライブラリを一括で追加

```bash
pip install -r requirements.txt
```

- pycordのみ別で追加

```bash
pip install git+https://github.com/Pycord-Development/pycord
```

- discordbot.py内の以下を書き換え

```python
token = os.environ['BOT_TOKEN']　#自分のBotトークンに書き換え
```

- ./cogs/control.py内の以下を書き換え

```python
guildId=int(os.environ['GUILD_ID']) #Botを使用するサーバーIDに書き換え
```

- 実行コマンド

```
python3 discordbot.py
```

## 遊び方

- 遊びたいDiscordサーバーで `/wwg start` と入力する
- あとはやればわかると思います。

## ゲーム仕様
基本的な人狼ゲームのルールと同じです。
- 役職一覧<br>
  |役職名|村人|占い師|騎士|霊媒師|人狼|狂人|
  |:----:|:----:|:----:|:----:|:----:|:----:|:----:|
  |陣営|村人|村人|村人|村人|人狼|人狼|
  |占い結果|村人|村人|村人|村人|人狼|村人|

  ※ 占い結果と霊媒結果は同じ
- 勝利条件
  - 人狼が0人になる  →  村人陣営勝利
  - 人狼と村人陣営が同じ人数になる  →  人狼陣営勝利
- 投票仕様
  - 決戦投票なし
  - 同数投票があった場合、同数だった人をランダムで一人を処刑する
- 騎士仕様
  - 連日同じ人は守れない
- 人狼仕様
  - 襲撃先の指定は各人狼のDMに送られる
  - もし、各人狼が別々の人を襲撃しようとした場合、ランダムでどちらかが襲撃される

## 何かあったら

連絡ください。
