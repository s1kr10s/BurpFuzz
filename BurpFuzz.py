#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Code By Miguel Mendez Z. & Pablo Pollanco

from burp import ITab
from burp import IBurpExtender
from burp import IScanIssue
from burp import IHttpListener
from burp import IProxyListener
from burp import IContextMenuFactory
from burp import IMessageEditorController
from burp import IInterceptedProxyMessage
from burp import IHttpRequestResponse
from burp import IExtensionStateListener
from java.io import PrintWriter
from java.awt import Font
from java.awt import Toolkit
from java.awt import GridLayout
from javax.swing import JOptionPane
from javax.swing import JPanel
from javax.swing import JMenuItem
from java.awt.event import ActionListener
from java.util import LinkedList
import java.lang as lang
from thread import start_new_thread
from ui import GUI
import re
import json
import os
import glob

TITLE = 'BurpFuzz'
VERSION = '1.0'
AUTHOR = 'Miguel Mendez Z. & Pablo Pollanco'
print('[+] {0} - version {1} \n[+] Authors: ({2})'.format(TITLE, VERSION, AUTHOR))

class BurpExtender(IBurpExtender, ITab, IContextMenuFactory, IExtensionStateListener, IHttpListener):
    def getTabCaption(self):
        # Setting extenstion tab name
        return "BurpFuzz"

    def getUiComponent(self):
        # Returning instance of the panel as in burp's docs
        return self.ui.panel

    def registerExtenderCallbacks(self, callbacks):

        gui = GUI()
        self.ui = gui.gui()

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName(TITLE)
        callbacks.registerHttpListener(self)
        callbacks.customizeUiComponent(self.ui.panel)
        callbacks.addSuiteTab(self)
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)
        self.initCallbacks()
        #self.gui()
        return

    def initCallbacks(self):
        self._callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        responses = invocation.getSelectedMessages()
        if responses > 0:
            ret = LinkedList()
            requestMenuItem = JMenuItem("Create BooFuzz Template")

            for response in responses:
                requestMenuItem.addActionListener(handleMenuItems(self,response, "request"))
            ret.add(requestMenuItem)
            return ret
        return None

    def sendRequestToAutorizeWork(self,messageInfo):
        req = []
        template = []
        data = False
        request = messageInfo.getRequest()
        httpService = messageInfo.getHttpService()
        self.panel = JPanel()
        self.panel.setLayout(GridLayout(2, 2))
        self.stdout.println('\n---------------------------------------\n')
        self.stdout.println('* Target - [{0}]'.format(httpService))
        self.stdout.println('-= Request Template =-')

        for i in request:
            req.append(chr(i))
        requetsFinal = "".join(req)

        template_head = '''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from boofuzz import *

def main():
    session = Session(
       target=Target(
           connection=SocketConnection("ip", 80, proto="tcp")
       ),
    )

    s_initialize(name="Request")'''

        template_footer = '''
    session.connect(s_get("Request"))
    session.fuzz()

if __name__ == "__main__":
    main()
'''        
        for line in requetsFinal.split("\n"):
            line = line.strip()
            if line == "":
                data = True
                print('')
            elif data == False:
                match_method = re.match(r"^(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE) ([^ ]*) (HTTP/.\..)", line)
                match_host = re.match(r"^Host: (.*)", line)
                match_other = re.match(r"^([^:]*): (.*)", line)
                if match_method != None: # method headers
                    template.append('    s_group("Method", ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE"])|    s_delim(" ")|    s_string("' + match_method.group(2) + '")|    s_delim(" ")|    s_group("HTTP-Version", ["HTTP/1.1", "HTTP/1.0"], "HTTP/1.1")|    s_static("\\r\\n")')
                elif match_host != None:
                    template_head = template_head.replace('ip', match_host.group(1))
                    template.append('    s_string("Host")|    s_delim(":")|    s_delim(" ")|    s_group("Hosts-line", ["localhost", "127.0.0.1", "' + match_host.group(1) + '"])|    s_static("\\r\\n")')
                elif match_other != None:
                    template.append('    s_static("' + match_other.group(1) + '")|    s_delim(":")|    s_delim(" ")|    s_string("' + match_other.group(2).strip("\n") + '")|    s_static("\\r\\n")')
                else:
                    pass
            else:
                # ideally process the data here so that we can also fuzz POST parameters
                template.append('s_string("' + line + ')"')

        #obtengo la ruta de donde se guardaran los templates
        if os.path.isfile('./config.json'):
            f = open("./config.json", "r")
            config = json.loads(f.read())
            path_template = '\n'.join(config['Path_Template'])

            if path_template <> "":
                #validamos la cantidad de archivos creados
                template_creados = len(glob.glob(str(path_template) + "/boofuzz_*.py"))+1
                f.close()

                for j, array_t in enumerate(template):
                    if j == 0:
                        f = open(str(path_template) + "/boofuzz_" + str(template_creados) + ".py", "a")
                        f.write(template_head + '\n' + array_t.replace("|","\n") + '\n')
                        f.close()
                        #self.stdout.println(str(j) + ' -> ' + str(array_t.replace("|","\n")))
                    elif j > 0:
                        f = open(str(path_template) + "/boofuzz_" + str(template_creados) + ".py", "a")
                        f.write(array_t.replace("|","\n") + '\n')
                        f.close()
                        #self.stdout.println(str(j) + ' -> ' + str(array_t.replace("|","\n")))

                f = open(str(path_template) + "/boofuzz_" + str(template_creados) + ".py", "a")
                f.write(template_footer)
                f.close()

                #mensaje de template creado
                JOptionPane.showMessageDialog(self.panel, "[boofuzz_" + str(template_creados) + ".py] template created for " + str(httpService), "Template Generator", JOptionPane.INFORMATION_MESSAGE)
            else:
                JOptionPane.showMessageDialog(self.panel, "Please set the path where templates will be saved.", "Settings Path", JOptionPane.WARNING_MESSAGE)

class handleMenuItems(ActionListener):

    def __init__(self, extender, messageInfo, menuName):
        self._extender = extender
        self._menuName = menuName
        self._messageInfo = messageInfo
        self.panel = JPanel()

    def actionPerformed(self, e):
        if self._menuName == "request":
            start_new_thread(self._extender.sendRequestToAutorizeWork,(self._messageInfo,))

