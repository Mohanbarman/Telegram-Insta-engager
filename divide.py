import os
import json

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]


def divide_links():
    with open('ig_links.json', 'r') as f:
        data = json.load(f)

    usernames = data['profile_names']
    post_links = data['post_links']

    u1, u2 = split_list(usernames, 2)
    p1, p2 = split_list(post_links, 2)

    new_json1 = {
        "profile_names": u1,
        "post_links": p1,
    }

    new_json2 = {
        "profile_names": u2,
        "post_links": p2,
    }

    os.chdir('links/')

    with open('links1.json', 'w') as f:
        json.dump(new_json1, f)

    with open('links2.json', 'w') as f:
        json.dump(new_json2, f)