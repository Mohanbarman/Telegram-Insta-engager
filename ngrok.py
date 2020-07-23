from pyngrok import ngrok

def get_public_url():
    previous_urls = ngrok.get_tunnels()

    for i in previous_urls:
        ngrok.disconnect(i.public_url)

    url = ngrok.connect(port=5000)
    url = url.replace('http', 'https')
    return url

def disconnect():
    previous_urls = ngrok.get_tunnels()

    for i in previous_urls:
        print(f'disconnected : {i.public_url}')
        ngrok.disconnect(i.public_url)