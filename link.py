def identify_link_type(link):
    """A function to identify the type of links returns 1 if its post or 2 if it's profile link"""
    slink = link.split('/')
    if 'p' in slink or 'tv' in slink or 'reel' in slink:
        return 1
    else:
        return 2

def extract_username(link):
    """Extract usernames from the link only for profile links"""
    slink = link.split('/')

    for counter, i in enumerate(slink):
        if 'instagram' in i:
            if 'igshid' in slink[counter + 1]:
                return slink[counter + 1].split('?')[0]
            else:
                return slink[counter + 1]


def extract_post_link(link):
    """Extract the link of post"""

    slink = link.split('/')
    url = 'https://www.instagram.com/'

    if 'p' in slink:
        url += 'p/' + slink[slink.index('p') + 1][:12]
        return url
    
    if 'tv' in slink:
        url += 'tv/' + slink[slink.index('tv') + 1][:12]
        return url

    if 'reel' in slink:
        url += 'reel/' + slink[slink.index('reel') + 1][:12]
        return url