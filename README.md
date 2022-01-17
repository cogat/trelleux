# Running update_trello_with_macos_reminders

```
cp template.env .env
# (and edit values)
brew install keith/formulae/reminders-cli
# grant reminders access - run `reminders` or see https://github.com/keith/reminders-cli/issues/13
python3 -m venv venv
. ./venv/bin/activate
./update_trello_with_macos_reminders.py
```

Once it runs successfully manually, to install and run every 5 mins:

```
cp lauched.trelleux.template.plist ~/Library/LaunchAgents/lauched.trelleux.plist
# edit the plist file to use correct paths
launchctl load -w ~/Library/LaunchAgents/lauched.trelleux.plist
```

(may need to grant more permissions for the python runner)
