import pywinio
import time

class keyIo:
  
    def __init__(self):
    
        # KeyBoard Commands
        # Command port
        self.KBC_KEY_CMD = 0x64
        # Data port
        self.KBC_KEY_DATA = 0x60
        #init
        self.g_winio = pywinio.WinIO()

        self.scancode_dict = {
            'esc': 0x01,
            '1': 0x02,
            '2': 0x03,
            '3': 0x04,
            'tab': 0x0f,
            'q': 0x10,
            'w': 0x11,
            'e': 0x12,
            'r': 0x13,
            't': 0x14,
            'y': 0x15,
            'u': 0x16,
            'i': 0x17,
            'o': 0x18,
            'p': 0x19,
            '[': 0x1a,
            ']': 0x1b,
            'enter': 0x1c,
            'lctrl': 0x1d,
            'a': 0x1e,
            's': 0x1f,
            'd': 0x20,
            'f': 0x21,
            'g': 0x22,
            'h': 0x23,
            'j': 0x24,
            'k': 0x25,
            'l': 0x26,
            ';': 0x27,
            '\'': 0x28,
            '`': 0x29,
            'lshift': 0x2a,
            'z': 0x2c,
            'x': 0x2d,
            'c': 0x2e,
            'v': 0x2f,
            'b': 0x30,
            'n': 0x31,
            'm': 0x32,
            '<': 0x33,
            '>': 0x34,
            '/': 0x35,
            'lalt': 0x38,
            'sp': 0x39,
            'capslk': 0x3a,
            'f1': 0x3b,
            'f2': 0x3c,
            'f3': 0x3d,
            'f4': 0x3e,
            'f5': 0x3f,
            'f6': 0x40,
            'f7': 0x41,
            'f8': 0x42,
            'f9': 0x43,
            'f10': 0x44
        }

    def wait_for_buffer_empty(self):
        '''
        Wait keyboard buffer empty
        '''

        winio = self.g_winio

        dwRegVal = 0x02
        while (dwRegVal & 0x02):
                dwRegVal = winio.get_port_byte(self.KBC_KEY_CMD)

    def key_down(self, scancode):
        winio = self.g_winio

        self.wait_for_buffer_empty();
        winio.set_port_byte(self.KBC_KEY_CMD, 0xd2);
        self.wait_for_buffer_empty();
        winio.set_port_byte(self.KBC_KEY_DATA, scancode)

    def key_up(self, scancode):
        winio = self.g_winio

        self.wait_for_buffer_empty();
        winio.set_port_byte( self.KBC_KEY_CMD, 0xd2);
        self.wait_for_buffer_empty();
        winio.set_port_byte( self.KBC_KEY_DATA, scancode | 0x80);

    def key_press(self, keycode, press_time = 0.2):
        scancode = self.scancode_dict[keycode]
        self.key_down( scancode )
        time.sleep( press_time )
        self.key_up( scancode )

