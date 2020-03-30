import json
import os
from javax.swing import JOptionPane

class URL(object):
    PARAM_URL = 0
    PARAM_BODY = 1
    PARAM_COOKIE = 2
    PARAM_XML = 3
    PARAM_XML_ATTR = 4
    PARAM_MULTIPART_ATTR = 5
    PARAM_JSON = 6

class Helpers(object):

    def get_payloads(self):

        return (self.path_template.getText().replace(" ","%20")).split("\n")

    #setea nueva configuracion para los templates
    def save_settings(self, evnt):

        config = {
        #'isEnabled': 0, 
        #'Randomize': 0, 
        #'Payloads': [],
        'Path_Template': []
        }

        #config['isEnabled'] = self.enable.isSelected()
        #config['Randomize'] = self.randomize.isSelected()

        for payload in self.get_payloads():
            config['Path_Template'].append(payload)

        f = open("./config.json", "w") 
        f.write(json.dumps(config))
        f.close() # For some reason jython doesn't close the file without this line

        JOptionPane.showMessageDialog(self.panel, "Settings saved", "Configuration", JOptionPane.INFORMATION_MESSAGE)
        print("[+] Settings saved")
        return

    #carga la configuracion guardada
    def load_settings(self):

        # Check if there's saved config if true then load it
        if os.path.isfile('./config.json'):

            f = open("./config.json", "r")
            config = json.loads(f.read())
            f.close() # For some reason jython doesn't close the file without this line

            #self.enable.setSelected(config['isEnabled'])
            #self.randomize.setSelected(config['Randomize'])
            self.path_template.setText('\n'.join(config['Path_Template']))
            print("[+] Settings loaded")

        return

