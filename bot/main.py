#imports
import os
import platform
import time
from os import listdir
from os.path import join, realpath, split, splitext
from discord_slash import SlashCommand
rootdir=os.path.abspath(os.path.join(os.curdir))
import discord
import psutil
from discord.ext import commands, ipc

from botconfig import botconfig

#
intents=discord.Intents.all()
intents.members = True
intents.guilds = True
ver='0.0.1'
startTime=time.time()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def line(color):
    print(f"{color}-----------")
print(f"{bcolors.OKBLUE}-----------")
print('''
 __                             __               
[  |  _                        [  |  _           
 | | / ] __   _   ____   ,--.   | | / ] __   _   
 | '' < [  | | | [_   ] `'_\ :  | '' < [  | | |  
 | |`\ \ | \_/ |, .' /_ // | |, | |`\ \ | \_/ |, 
[__|  \_]'.__.'_/[_____]\'-;__/[__|  \_]'.__.'_/                                             
''')
print(f"{bcolors.OKBLUE}-----------")
def log(log):
    print(f'{bcolors.OKBLUE}[#] {log}')
def warning(warn):
    print(f'{bcolors.WARNING}[!] {warn}')
def error(error):
    print(f'{bcolors.FAIL}{error}')

class kuzaku(discord.ext.commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.ipc = ipc.Server(self, secret_key=os.getenv('ipckey'))

    async def on_ipc_ready(self):
        log("IPC сервер готов")

    async def on_ipc_error(self, endpoint, error):
        error(endpoint, "raised", error)
    async def on_connect(self):
        log('бот подключается...')
        line(bcolors.OKBLUE)
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f'{len(self.guilds)} guilds | k.help'))
        log(f'бот подключен к discord\'у!\n[#] имя пользователя: {self.user}\n[#] id: {self.user.id}\n[#] кол-во серверов: {len(self.guilds)}\n[#] количество пользователей: {len(self.users)}')
        line(bcolors.OKBLUE)


bot=kuzaku(command_prefix='k.', intents=intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
def load_ext(bot,dir):
    if platform.system() in ["Darwin", 'Windows']:
        for filename in os.listdir(f'{rootdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'{dir}.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    log(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
    elif platform.system()=='Linux':
        for filename in os.listdir(f'{os.curdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'bot.cogs.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    log(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
load_ext(bot, 'cogs')
line(bcolors.OKBLUE)
bot.load_extension('jishaku')

@bot.ipc.route()
async def get_stats(data):
    return {"status":"200", "message":"all is ok", "guilds":len(bot.guilds), "users":len(bot.users)}


if __name__ == '__main__':
    bot.ipc.start()
    bot.run(botconfig['token'])






