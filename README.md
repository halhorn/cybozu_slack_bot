# cybouzu_slack_bot
Cybouzu Garoon の予定を Slack に通知してくれます。
実装は雑です。


# Install
```
git clone git@github.com:halhorn/cybouzu_slack_bot.git
cd cybouzu_slack_bot
cp -fr secret.sample secret
emacs secret/cybouzu.yml
emacs secret/slack.yml
```

パスワードを直接ファイルに書かないで環境変数 `CYBOUZU_PASS` に入れても動きます。

# Run
```
cd cybouzu_slack_bot
python -m bot.run
```
