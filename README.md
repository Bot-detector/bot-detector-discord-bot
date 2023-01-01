# bot-detector-discord-bot
The bot detector discord bot is the public interface via discord of the bot detector plugin and its functionalities.

# How does it work?
The bot detector discord bot is a stand alone component that can interface with other components via its API.
![image](https://user-images.githubusercontent.com/40169115/154528234-fcd0ae4c-78a1-4d52-b446-0b7086bdf55a.png)

## setup
```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## setup pre-commit
```
pre-commit --version
pre-commit install
```
# for admin purposes saving & upgrading

```
venv\Scripts\activate
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '==', '>=' } | Set-Content requirements.txt"
call pip install -r requirements.txt --upgrade
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '>=', '==' } | Set-Content requirements.txt"
```
