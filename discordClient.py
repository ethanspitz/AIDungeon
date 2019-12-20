import discord, pexpect, systemd.daemon, syslog

TOKEN = 'NjUzMzgwNjMyNTI0NzUwODY4.Xe3C9w.TxkVjyrV01Jry-3QcF09cjmWxt4'

bot_prefix = '!ai '
first_print = True
max_msg_len = 2000-7
client = discord.Client()
child = pexpect.spawn('/bin/bash -c "source ./venv/bin/activate; ./venv/bin/python play.py"', timeout=None, encoding='utf-8')
save_game_response = ""
previous_command = ""
last_match = ""

async def sendDiscordMessage(channel, msg):
    # Send discord message that is always safe to send by breaking message into chunks
    msg_chunks = [msg[i:i+max_msg_len] for i in range (0, len(msg), max_msg_len)]
    
    for chunk in msg_chunks:
        await channel.send('```' + str(chunk) + '```')
        syslog.syslog(syslog.LOG_INFO, chunk)

async def waitForSuccessfulPrompt(channel, timeoutConf):
    # For use after sending input to the program, this function will wait until the program responds.
    # It is smart enough to detect crashes and also automatically restart the program.
    # return 1 on timeout
    global child
    global last_match
    index = child.expect( [pexpect.EOF, pexpect.TIMEOUT, 'Enter the number of your choice:', '\r\n>', 'What is your name\?', 'What is the ID of the saved game\?', 'Please rate the story quality from 1-10:'], timeout=timeoutConf)

    if index == 0:
        # EOF, we crashed
        response = child.before
        await sendDiscordMessage(channel, response)
        await handleCrashRestartAndWaitForPrompt(channel)
    elif index == 1:
        # Timed out. Time to bail.
        return 1
    else:
        # not EOF or timeout, save match
        last_match = child.after
    return 0

async def save_game(channel):
    # silently save game save id to memeory in case of crash
    global child
    global save_game_response

    syslog.syslog(syslog.LOG_INFO, "Saving Game");

    child.sendline("/save")
    await waitForSuccessfulPrompt(channel, None)
    save_game_response = child.before + child.after


async def handleCrashRestartAndWaitForPrompt(channel):
    # EOF was reached. Program must have died
    global child
    global save_game_response

    log_message = '```' + "AI Dungeon 2 Crashed. Restarting." + '```'
    await channel.send(log_message)
    syslog.syslog(syslog.LOG_INFO, log_message)
   
    # extract id only
    log_message = '```' + "Save ID to recover:\n\n" + save_game_response.split('following ID:',1)[1].split("\n")[0].strip() + '```'
    await channel.send(log_message)
    syslog.syslog(syslog.LOG_INFO, log_message)

    child = pexpect.spawn('/bin/bash -c "source ./venv/bin/activate; ./venv/bin/python play.py"', timeout=None, encoding='utf-8')
    await waitForSuccessfulPrompt(channel, None)

@client.event
async def on_message(message):
    global child
    global last_match
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.channel.name == 'ai-adventure' and message.content.startswith(bot_prefix):
    
        syslog.syslog("Processing message: " + message.content)

        previous_command = message.content[len(bot_prefix):]
        child.sendline(previous_command)
        await waitForSuccessfulPrompt(message.channel, None)
        response = child.before + child.after
        await sendDiscordMessage(message.channel, response)

        # get any stragglers, but only give a second timeout this time.
        while not await waitForSuccessfulPrompt(message.channel, 1):
            response = child.before + child.after
            await sendDiscordMessage(message.channel, response)

        if str(last_match).strip() == '>':
            # Normal prompt, should be safe to save the game
            await save_game(message.channel)


@client.event
async def on_ready():
    global first_print
    syslog.syslog(syslog.LOG_INFO, 'Logged in as')
    syslog.syslog(syslog.LOG_INFO, client.user.name)
    syslog.syslog(syslog.LOG_INFO, str(client.user.id))
    syslog.syslog(syslog.LOG_INFO, '------')
    channel = client.get_channel(653366602766745611)

    if first_print:
        response = child.before + child.after
        await sendDiscordMessage(channel, response)
        syslog.syslog(syslog.LOG_INFO, "Finished Spawning")
        first_print = False

# Beginning of main
# don't wait for successful prompt here
index = child.expect( [pexpect.EOF, 'Enter the number of your choice:', '\r\n>', 'What is your name\?'], timeout=None)
if index == 0:
    # we crashed immediately. Bail
    quit()
systemd.daemon.notify('READY=1')
client.run(TOKEN)
