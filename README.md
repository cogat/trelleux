# Running update_trello_with_macos_reminders

```
cp template.env .env
# (and edit values)
brew install keith/formulae/reminders-cli
python3 -m venv venv
. ./venv/bin/activate
./update_trello_with_macos_reminders
```

# Deploying to AWS Lambda:

```
pip install -t packages -r requirements.txt
cd packages && zip -r9 ../lambda.zip . && cd .. && zip -g lambda.zip *.py
aws lambda update-function-code --function-name trelleux --zip-file fileb://lambda.zip
```

## To install a rule that runs hourly:

```
aws events put-rule --schedule-expression "cron(0 * * * ? *)" --name UpdateTrelleux
aws events put-rule --schedule-expression "cron(* * * * ? *)" --name UpdateTrelleux
aws events put-targets --rule UpdateTrelleux --targets file://targets.json
```
