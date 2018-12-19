# cybozu_slack_bot
Cybozu Garoon の予定を Slack に通知してくれます。
実装は雑です。


# Install
```
git clone git@github.com:halhorn/cybozu_slack_bot.git
cd cybozu_slack_bot
cp -fr secret.sample secret
emacs secret/cybozu.yml
emacs secret/slack.yml
```

パスワードを直接ファイルに書かないで環境変数 `CYBOZU_PASS` に入れても動きます。

# Run
```
cd cybozu_slack_bot
python -m bot.run
```
