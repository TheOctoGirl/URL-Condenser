import requests
import qrcode
import urllib.parse

def shorten(url):
    encoded_url = urllib.parse.quote(url,safe=':/?&=')
    print(encoded_url)
    params = {
        "url": encoded_url,
        "format": "json"
    }
    
    response = requests.get("https://is.gd/create.php", params=params)
    json = response.json()
    
    if "shorturl" in json:
        return json["shorturl"]
    
    elif json["errorcode"] == 1:
        raise InvalidURLError
    
    elif json["errorcode"] == 3:
        raise RateLimitError
    
    elif json["errorcode"] == 4:
        raise UnknownError
    
    else:
        raise UnknownError
    

def qr_code(url, background_color="white", fill_color="black"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=background_color)
    img.save("qr_code.png")
    return img

def unshorten(url):
    encoded_url = urllib.parse.quote(url,safe=':/?&=')
    params = {
        "shorturl": encoded_url,
        "format": "json"
    }
    response = requests.get("https://is.gd/forward.php", params=params)
    json = response.json()
    
    if "url" in json:
        decoded_url = urllib.parse.unquote(json["url"])
        return decoded_url
    
    elif json["errorcode"] == 1:
        raise InvalidURLError
    
    elif json["errorcode"] == 3:
        raise RateLimitError
    
    elif json["errorcode"] == 4:
        raise UnknownError
    
    else:
        raise UnknownError
    
def custom(url, custom_url):
    encoded_url = urllib.parse.quote(url,safe=':/?&=')
    params = {
        "url": encoded_url,
        "shorturl": custom_url,
        "format": "json"
    }
    response = requests.get("https://is.gd/create.php", params=params)
    json = response.json()
    
    if "shorturl" in json:
        return json["shorturl"]
    
    elif json["errorcode"] == 1:
        raise InvalidURLError
    
    elif json["errorcode"] == 2:
        raise InvalidCustomURLError
    
    elif json["errorcode"] == 3:
        raise RateLimitError
    
    elif json["errorcode"] == 4:
        raise UnknownError
    
    else:
        raise UnknownError


class InvalidURLError(Exception):
    pass

class InvalidCustomURLError(Exception):
    pass

class RateLimitError(Exception):
    pass

class UnknownError(Exception):
    pass