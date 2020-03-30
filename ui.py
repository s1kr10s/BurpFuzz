from java.awt import Component
from java.awt import FlowLayout
from java.awt import Panel
from java.awt.event import ActionEvent
from java.awt.event import ActionListener
from javax.swing import JButton
from javax.swing import JLabel
from java.awt import BorderLayout
from javax.swing import JCheckBox
from javax.swing import JTable
from javax.swing import JScrollPane
from javax.swing.table import DefaultTableModel
from javax.swing import JTextField
from javax.swing import JTextArea
from java.io import PrintWriter
from utils import Helpers

#from java.awt import GridLayout
#from javax.swing import JOptionPane
#from javax.swing import JPanel

class GUI(Helpers):
#class GUI():

    def gui(self):

        self.panel = Panel()
        self.panel.setLayout(None)

        '''
        self.scn_lbl = JLabel("Enable scanning")
        self.scn_lbl.setBounds(10, 5, 100, 20)
        self.panel.add(self.scn_lbl)
        self.enable = JCheckBox()
        self.enable.setBounds(130, 5, 50, 20)
        self.panel.add(self.enable)

        self.rand_lbl = JLabel("Randomize payloads")
        self.rand_lbl.setBounds(10, 20, 100, 20)
        self.panel.add(self.rand_lbl)
        self.randomize = JCheckBox()
        self.randomize.setBounds(130, 20, 50, 20)
        self.panel.add(self.randomize)

        self.pyld_lbl = JLabel("Payloads List (Line separated)")
        self.pyld_lbl.setBounds(10, 35, 180, 20)
        self.panel.add(self.pyld_lbl)

        self.payloads_list = JTextArea()
        self.pyld_scrl = JScrollPane(self.payloads_list)
        self.pyld_scrl.setBounds(10, 55, 600, 200)
        self.panel.add(self.pyld_scrl)
        '''

        self.path_text = JLabel("Path File Template:")
        self.path_text.setBounds(10, 30, 300, 20)
        self.panel.add(self.path_text)

        self.path_template = JTextField()
        self.path_template.setBounds(10, 50, 400, 30)
        self.panel.add(self.path_template)

        self.save_btn = JButton("Guardar Config", actionPerformed=self.save_settings)
        self.save_btn.setBounds(10, 80, 150, 30)
        self.panel.add(self.save_btn)

        self.load_settings()
        return self

