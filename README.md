# AIDungeon2

### The model for AI Dungeon2 is temporarily unavailable to download due to cost. We're working on a solution!

Read more about AIDungeon2 and how it was built [here](https://pcc.cs.byu.edu/2019/11/21/ai-dungeon-2-creating-infinitely-generated-text-adventures-with-deep-learning-language-models/).

Play the game in Colab [here](http://www.aidungeon.io).

To play the game locally, it is recommended that you have an nVidia GPU with 12 GB or more of memory, and CUDA installed. If you do not have such a GPU, each turn can take a couple of minutes or more for the game to compose its response. To install and play locally:
```
git clone --branch master https://github.com/AIDungeon/AIDungeon/
cd AIDungeon
./install.sh # Installs system packages and creates python3 virtual environment
./download_model.sh
source ./venv/bin/activate
./play.py
```

Discord Bot
------------------------
To run as a Discord bot, create a config.ini in the root directory with the following contents
```
[discord]
bot_prefix = !ai
token = <discord bot token here>
```

By default it will pass any text after "!ai" into the game. You can configure this prefix.
To create a bot and get a token for the bot, follow the instructions here: https://discordpy.readthedocs.io/en/latest/discord.html

To start the bot run the discordClient.py:
```
python3 discordClient.py
```

Also included is a systemd service file which you can place in /usr/lib/systemd/system/. This assumes you cloned the game into /opt/AIDungeon2.

Community
------------------------

AIDungeon is an open source project. Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, documentation, or even new core features.

Resources:

* **Website**: [aidungeon.io](http://www.aidungeon.io/)
* **Email**: aidungeon.io@gmail.com
* **Twitter**: [creator @nickwalton00](https://twitter.com/nickwalton00), [dev @benjbay](https://twitter.com/benjbay)
* **Reddit**: [r/AIDungeon](https://www.reddit.com/r/AIDungeon/)
* **Discord**: [aidungeon discord](https://discord.gg/Dg8Vcz6)


Contributing
------------------------
Contributing to AIDungeon is easy! Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/)
from your fork. Before you send it, summarize your change in the
[Unreleased] section of [the CHANGELOG](CHANGELOG.md) and make sure
``develop`` is the destination branch.

AIDungeon uses a rough approximation of the
[Git Flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model.  The ``develop`` branch contains the latest
contributions, and ``master`` is always tagged and points to the latest
stable release.

If you're a contributor, make sure you're testing and playing on `develop`.
That's where all the magic is happening (and where we hope bugs stop).
