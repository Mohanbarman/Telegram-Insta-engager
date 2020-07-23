import json
import instapy
import sys

def start_engaging(profile_names, post_links, comment=False, account=1):

    username = ac_1['username']
    password = ac_1['password']

    if account == 2:
        username = ac_2['username']
        password = ac_2['password']

    print(f'logging in with : {username}')

    session = instapy.InstaPy(username=username, password=password, headless_browser=False)
    session.login()

    session.set_do_like(enabled=True, percentage=100)

    if comment:
        comments = [
            'Love to consume your posts man',
            'Your page really deserves to be seen by many peoples',
            'Love your page buddy',
        ]
        session.set_comments(comments=comments)
        session.set_do_comment(enabled=comment, percentage=100)

    session.interact_by_URL(urls=post_links, randomize=False, interact=True)
    session.interact_by_users(usernames=profile_names, amount=1, randomize=False)

args = sys.argv

if '-l' not in args:
    print('Please give me the path of links with -l option..')
    sys.exit()

path = args[args.index('-l') + 1]

with open(path, 'r') as f:
    data = json.load(f)

pro_names = []
pos_links = data['post_links']

if 'profile_names' in data:
    pro_names = data['profile_names']


for i in range(0, pos_links.count(None)):
    pos_links.remove(None)

for i in range(0, pro_names.count(None)):
    pro_names.remove(None)


for i in pos_links:
    print(f'Post : {i}')
for i in pro_names:
    print(f'profile : {i}')

comment = False
account = 1

ac_1 = {}
ac_2 = {}

with open('ig_accounts.json', 'r') as f:
    acc = json.load(f)
    ac_1['username'] = acc['ac1']['username']
    ac_1['password'] = acc['ac1']['password']

    ac_2['username'] = acc['ac2']['username']
    ac_2['password'] = acc['ac2']['password']

args = sys.argv
if '-c' in args:
    comment = True

if not '-d' in args and not '-a' in args:
    print('Please tell which account to use using -a <account> option.')
    sys.exit()

account = int(args[args.index('-a') + 1])
    
while True:
    try:
        start_engaging(profile_names=pro_names, post_links=pos_links, comment=comment, account=account)
        break
    except not KeyboardInterrupt:
        pass
