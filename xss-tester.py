import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame

pygame.mixer.music.load("song.ogg") #Tozan
pygame.mixer.music.play(-1)

level = -2
target = ""
message=""
gemacht=False

import requests
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

class XSSTester:
    def __init__(self):
        self.payloads = [
            "<script>alert('Hallo Kumpel!')</script>",
            "<img src=x onerror=alert('Hallo Kumpel!')>",
            "<svg onload=alert('Hallo Kumpel!')>",
            "'-alert('Hallo Kumpel!')-'",
            '"><script>alert("Hallo Kumpel!")</script>',
            "<iframe src='javascript:alert(\"Hallo Kumpel!\")'>",
        ]
        
        self.found_vulnerabilities = []
    
    def test_url(self, url):
        global message
        message+=f"\n🔍 Testing URL: {url}\n"
        message+="=" * 60+"\n"
        
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        if not params:
            message+="⚠️  No parameters in URL found\n"
            message+="💡 Example: http://example.com/page?input=test\n"
            return
        
        for param_name in params.keys():
            message+=f"\n📝 Testing parameter: {param_name}\n"
            
            for i, payload in enumerate(self.payloads, 1):
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(test_params, doseq=True)}"
                
                try:
                    response = requests.get(test_url, timeout=5)
                    
                    if payload in response.text:
                        vulnerability = {
                            'url': url,
                            'parameter': param_name,
                            'payload': payload,
                            'vulnerable': True
                        }
                        self.found_vulnerabilities.append(vulnerability)
                        
                        message+=f"  ✓ Payload {i}: POTENTIAL VULNERABLE!\n"
                        message+=f"    → {payload[:50]}...\n"
                    else:
                        message+=f"  ✗ Payload {i}: Filtered or encoded\n"
                
                except requests.exceptions.RequestException as e:
                    message+=f"  ❌ Error at Payload {i}: {e}\n"
    
        message+="\n" + "=" * 60+"\n"
        if self.found_vulnerabilities:
            message+=f"⚠️  {len(self.found_vulnerabilities)} potential XSS-Vulnerability found!\n"
            message+="\n📋 Details:\n"
            for vuln in self.found_vulnerabilities:
                message+=f"\n  Parameter: {vuln['parameter']}\n"
                message+=f"  Payload: {vuln['payload']}\n"
        else:
            message+="✓ No obvious XSS-weakpoints found\n"
            message+="  (That means not, that the site is 100% secure!)\n"
        
        message+="=" * 60+"\n"
    
def draw():
    global level, target, message
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to test:", center=(400, 130), fontsize=24, color=(250, 200, 255))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        #screen.blit("back",(0,0))
        screen.draw.text(message, center=(400, 130), fontsize=24, color=(250, 200, 255))

def on_key_down(key, mod, unicode):  
    global level, target    
    if key == keys.ESCAPE:
        pygame.quit()
    elif key == keys.BACKSPACE:
        target = target[:-1]   
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "127.0.0.1"
        target+="/index.html?input=test"
        level = 2
    elif level == 1 and unicode:
        target += unicode

def update():
    global level,message,gemacht
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==2 and not gemacht:
        gemacht=True
        message+="=" * 60+"\n"
        message+="🔐 XSS Vulnerability Tester\n"
        message+="=" * 60+"\n"
        message+="⚠️  ONLY for own websites or with permission!\n"
        message+="=" * 60+"\n"
        tester = XSSTester()
        message+="URL testing\n"
        url = target
        tester.test_url(url)
    if level==2 and keyboard.space:
        level=0        

pgzrun.go()


