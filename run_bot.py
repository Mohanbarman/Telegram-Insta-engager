from divide import divide_links
import subprocess
import sys
import ngrok
import pyngrok
import os

args = sys.argv

url = ngrok.get_public_url()
print(url)

comment = 0
account = 1

for counter, i in enumerate(args):
    if i == '-c':
        comment = 1

    if i == '-a':
        account = args[counter + 1]

subprocess.run(['python', 'flask_app.py', url])

ngrok.disconnect()
pyngrok.ngrok.kill()

if '-d' in args:
    divide_links()
    os.chdir("/home/mohan/Programming/Python/Telegram-bot")

    if '-c' in args:
        subprocess.Popen(["termite", "-e", "python insta_bot.py -c -a 1 -l links/links1.json"])
        subprocess.Popen(["termite", "-e", "python insta_bot.py -c -a 2 -l links/links2.json"])

    if not '-c' in args:
        subprocess.Popen(["termite", "-e", "python insta_bot.py -a 1 -l links/links1.json"])
        subprocess.Popen(["termite", "-e", "python insta_bot.py -a 2 -l links/links2.json"])

    sys.exit()

if not '-a' in args:
    print('Pass account no. with -a option...')
    sys.exit()

if comment:
    subprocess.run(['python', 'insta_bot.py', '-c', '-a', account, '-l', 'ig_links.json'])
else :
    subprocess.run(['python', 'insta_bot.py', '-l', 'ig_links.json', '-a', account])
