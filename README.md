# URL Condenser

## Installation

### Discord Bot Invite
To invite the discord bot to your server click [here](https://discord.com/api/oauth2/authorize?client_id=1105237323798556764&permissions=0&scope=bot)

### Self-hosted

#### Requirements
Python 3.10+
MariaDB 10.6+

#### Steps
1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`. Note: If you are using an Ubuntu or Debian based distro you need to install the `libmariadb-dev package` with `sudo apt install libmariadb-dev`
3. Create a database with a table named urls and also create a user with insert and select permissions on that table
4. Rename default_config.py to config.py and fill in the required fields
5. Run the server with `python3 main.py`
