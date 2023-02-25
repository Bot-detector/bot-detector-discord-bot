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
# for admin purposes saving & upgrading

```
venv\Scripts\activate
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '==', '>=' } | Set-Content requirements.txt"
call pip install -r requirements.txt --upgrade
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '>=', '==' } | Set-Content requirements.txt"
```

# structure:
There are 3 main directories in the project:

1. `core`: This directory contains the central part of this project. It contains most of the boiler plate code like security dependencies, database connections, configuration, middlewares etc. It also contains the base classes for the models, repositories, and controllers. The `core` directory is designed to be as minimal as possible and usually requires minimal attention. Overall, the `core` directory is designed to be as generic as possible and can be used in any project. While building additional feature you may not need to modify this directory at all except for adding more controllers to the `Factory` class in `core/factory.py`.

2. `app`: This directory contains the actual application code. It contains the models, repositories, controllers, and schemas for the application. This is the directory you will be spending most of your time in while building features. The directory has following sub-directories:

   - `models` Here is where you add new tables
   - `repositories` For each model, you need to create a repository. This is where you add the CRUD operations for the model.
   - `controllers` For each logical unit of the application, you need to create a controller. This is where you add the business logic for the application.
   - `schemas` This is where you add the schemas for the application. The schemas are used for validation and serialization/deserialization of the data.

3. `api`: This directory contains the API layer of the application. It contains the API router, it is where you add the API endpoints.
