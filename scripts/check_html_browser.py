#!/usr/bin/env python3
"""Exercise the offline reader in an isolated installed Chromium via DevTools.

Optional QA dependency: websocket-client. No browser download is performed.
"""
import argparse
import base64
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import urllib.request
import websocket

class Browser:
    def __init__(self,socket):self.socket=socket;self.sequence=0;self.exceptions=[]
    def call(self,method,params=None):
        self.sequence+=1;number=self.sequence
        self.socket.send(json.dumps(dict(id=number,method=method,params=params or {})))
        while True:
            response=json.loads(self.socket.recv())
            if response.get('method')=='Runtime.exceptionThrown':self.exceptions.append(response['params'])
            if response.get('id')==number:
                if 'error' in response:raise RuntimeError(response['error'])
                return response.get('result',{})
    def js(self,expression):
        result=self.call('Runtime.evaluate',dict(expression=expression,returnByValue=True,awaitPromise=True))
        if 'exceptionDetails' in result:raise AssertionError(result['exceptionDetails'])
        return result['result'].get('value')
    def wait(self,expression,seconds=8):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if self.js(expression):return
            time.sleep(.04)
        raise AssertionError('Timed out: '+expression)
    def route(self,identity):
        self.js('location.hash='+json.dumps(identity))
        self.wait(f'document.getElementById({json.dumps(identity)}).hidden === false')
    def screenshot(self,path):
        path.write_bytes(base64.b64decode(self.call('Page.captureScreenshot',dict(format='png'))['data']))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--html',type=Path,default=Path(__file__).resolve().parents[1]/'html/index.html');parser.add_argument('--screenshots',type=Path,default=Path('/tmp/cw-html-preview'));args=parser.parse_args()
    chrome=shutil.which('chromium') or shutil.which('google-chrome')
    if not chrome:raise SystemExit('Installed Chromium is required for this optional check.')
    args.screenshots.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cw-html-chrome-') as profile:
        log=open(Path(profile)/'browser.log','w+')
        process=subprocess.Popen([chrome,'--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-first-run','--disable-background-networking','--disable-component-update','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=log,stderr=log)
        socket=None
        try:
            portfile=Path(profile)/'DevToolsActivePort';deadline=time.monotonic()+12
            while not portfile.exists():
                if process.poll() is not None or time.monotonic()>deadline:
                    log.seek(0);raise RuntimeError('Chromium failed to start: '+log.read()[-2500:])
                time.sleep(.05)
            port=portfile.read_text().splitlines()[0]
            targets=json.load(urllib.request.urlopen('http://127.0.0.1:'+port+'/json',timeout=5))
            target=next(t for t in targets if t['type']=='page')
            socket=websocket.create_connection(target['webSocketDebuggerUrl'],origin='http://localhost',timeout=10)
            b=Browser(socket);b.call('Runtime.enable');b.call('Page.enable');b.call('Network.enable')
            b.call('Network.setBlockedURLs',dict(urls=['http://*','https://*']))
            b.call('Emulation.setDeviceMetricsOverride',dict(width=1440,height=1000,deviceScaleFactor=1,mobile=False))
            b.call('Page.navigate',dict(url=args.html.resolve().as_uri()))
            b.wait('document.readyState === "complete" && !!document.getElementById("overview")')
            assert b.js('document.querySelectorAll(".route:not([hidden])").length')==1
            assert b.js('document.querySelectorAll(".reveal-button[aria-expanded=true]").length')==0
            b.js('document.fonts.ready');b.screenshot(args.screenshots/'overview.png')
            b.route('01-generalities');assert b.js('!document.getElementById("01-generalities").hidden')
            b.route('cw-support-calculus')
            assert b.js('document.getElementById("tree-01-generalities").open')
            b.js('document.querySelector("#cw-support-calculus .hint button").click()')
            assert b.js('!document.getElementById("cw-support-calculus-hint").hidden')
            assert b.js('document.getElementById("cw-support-calculus-solution").hidden')
            b.js('document.querySelector("#cw-support-calculus .solution button").click()')
            assert b.js('!document.getElementById("cw-support-calculus-solution").hidden')
            b.js('document.querySelector("#cw-support-calculus .hint button").click()')
            assert b.js('document.getElementById("cw-support-calculus-hint").hidden')
            assert b.js('!document.getElementById("cw-support-calculus-solution").hidden')
            b.route('cw-triangle-measures');b.screenshot(args.screenshots/'problem.png')
            b.route('cw-support-calculus')
            assert b.js('document.getElementById("cw-support-calculus-solution").hidden')
            b.call('Page.reload');b.wait('document.readyState === "complete" && !document.getElementById("cw-support-calculus").hidden')
            assert b.js('document.querySelectorAll(".reveal-button[aria-expanded=true]").length')==0
            b.js('const s=document.getElementById("search");s.value="Cheeger";s.dispatchEvent(new Event("input"));')
            assert b.js('document.querySelectorAll(".problem-nav-item:not([hidden])").length')>0
            assert b.js('document.querySelectorAll(".problem-nav-item:not([hidden])").length < document.querySelectorAll(".problem-nav-item").length')
            b.js('document.getElementById("search").value="zzzznomatch";document.getElementById("search").dispatchEvent(new Event("input"))')
            assert b.js('!document.getElementById("no-results").hidden')
            b.js('document.getElementById("search").value="";document.getElementById("search").dispatchEvent(new Event("input"))')
            b.route('cw-open-meissner')
            assert 'background' in b.js('document.querySelector("#cw-open-meissner .solution button").textContent')
            assert 'starting point' in b.js('document.querySelector("#cw-open-meissner .hint button").textContent')
            b.js('location.hash="unknown-problem"');b.wait('!document.getElementById("not-found").hidden')
            b.route('overview');b.js('document.querySelector(".skip-link").click()')
            assert b.js('!document.getElementById("overview").hidden && document.activeElement.id === "content"')
            b.call('Emulation.setDeviceMetricsOverride',dict(width=390,height=844,deviceScaleFactor=1,mobile=True))
            b.route('cw-triangle-measures')
            assert b.js('document.documentElement.scrollWidth <= innerWidth + 1')
            b.js('document.getElementById("menu-button").click()')
            assert b.js('document.getElementById("sidebar").classList.contains("is-open")')
            b.js("""document.querySelector('#tree-02-reuleaux-polygons a[href="#cw-regular-reuleaux"]').click()""")
            b.wait('!document.getElementById("cw-regular-reuleaux").hidden')
            assert b.js('!document.getElementById("sidebar").classList.contains("is-open")')
            b.screenshot(args.screenshots/'mobile.png')
            assert not b.exceptions,b.exceptions
            print('Browser checks passed: offline rendering, chapter/problem routes, independent reveal/close, reset on navigation/reload, search, open-question labels, missing links, skip link, mobile navigation and width.')
            print('Screenshots:',args.screenshots)
        finally:
            if socket:
                try:b.call('Browser.close')
                except (websocket.WebSocketException, OSError, ValueError):pass
                socket.close()
            else:process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()
            log.close()
if __name__=='__main__':main()
