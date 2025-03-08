from ctypes import BigEndianStructure
import socket
import array
import time
import sys
from socket import inet_aton
import packet_protocol as pp

class Communication:
    def __init__(self,address,port=502):
        self.pos_0=0x00
        self.pos_1=0x00
        self.pos_2=0x00
        self.pos_3=0x00
        self.val = 0

        # limit step number
        self.upper_lim=333200  
        self.lower_lim=158650 
        
        self.is_set_pos = False

        # IP addreess
        self.address = address
        self.port = 502

        self.BUFSIZE = 4096

        print("***************************************")
        print("* Modbus TCP sample program for AZ series *")
        print("* Python *")
        print("* *")
        print("***************************************")
        print("\nDriver IP Address >" + self.address)
        print("\nDriver Port >" + str(self.port))

        # ソケット
        self.client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #TCP/IP

        # self.client  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #UDP/IP

        # タイムアウトを設定
        self.client.settimeout(5)

        # ドライバと接続
        try:
            self.client.connect((self.address, int(self.port)))

        except OSError as msg:
            self.client.close()
            self.client = None

        # 接続失敗時は終了
        if self.client is None:
            print("could not open socket.")
            print("  IPAddress: " + self.address)
            print("  Port: " + str(self.port))
            input()
            sys.exit()
        self.frm_count = 0
        self.current_position =0
        self.get_current_position()
        self.target_pos = self.get_current_position()

    def decimal_to_hexadecimal(self,value):
        byte_array = value.to_bytes(4, byteorder='big')
        # print(hex(byte_array[0]))
        # print(hex(byte_array[1]))
        # print(hex(byte_array[2]))
        # print(hex(byte_array[3]))
        return byte_array

    def get_current_position(self):
        frm_count_array = self.frm_count.to_bytes(2, "big")
        wkfrm = array.array('B', [])
        wkfrm.extend(frm_count_array)
        wkfrm.extend(pp.frm_Mon)

        # クエリ送信
        self.client.sendto(wkfrm,(self.address,self.port))
        rcvData  = self.client.recv(self.BUFSIZE)
        #print(rcvData)

        self.current_position = int.from_bytes(array.array('B', [rcvData[19], rcvData[20], rcvData[17], rcvData[18] ]), byteorder='big', signed=True)
        #print("Position:",self.current_position)
        
        return self.current_position
    
    def set_target_position(self, target_pos):
        if target_pos > self.upper_lim or target_pos < self.lower_lim:
            print("\x1b[31mTarget position is out of range\x1b[39m")
            return False
        self.is_set_pos = True
        self.pos_0,self.pos_1,self.pos_2,self.pos_3=self.decimal_to_hexadecimal(target_pos)
        self.target_pos=target_pos
        # print("pos_0:",self.pos_0)
        # print("pos_1:",self.pos_1)
        # print("pos_2:",self.pos_2)
        # print("pos_3:",self.pos_3)
        return True
    def send_target_position(self):
        if not self.is_set_pos:
            print("\x1b[31mPlease set target position first\x1b[39m")
            return
        frm_count_array = self.frm_count.to_bytes(2, "big")
        wkfrm = array.array('B', [])
        wkfrm.extend(frm_count_array)
        pp.frm_ExeOpe[19]=self.pos_2
        pp.frm_ExeOpe[20]=self.pos_3
        pp.frm_ExeOpe[21]=self.pos_0
        pp.frm_ExeOpe[22]=self.pos_1
        wkfrm.extend(pp.frm_ExeOpe)
        #answer=[0, 0, 0, 0, 0, 47, 0, 16, 1, 4, 0, 20, 40, 0, 0, 0, 0, 1, 0, 0, 1, 13, 64, 0, 3, 134, 160, 0, 1, 7, 208, 0, 0, 5, 220, 0, 0, 3, 232, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # for i in range(47):
        #     if wkfrm[i]!=answer[i]:
        #         print("Error at index:",i)
        #         print("Expected:",answer[i])
        #         print("Actual:",wkfrm[i])
            
        # print ("done")
        #return

        self.client.sendto(wkfrm,(self.address,self.port))
        rcvData  = self.client.recv(self.BUFSIZE)
        print(rcvData)
        self.frm_count += 1
        time.sleep(0.1)

            # ダイレクトデータ運転のトリガをOFFするクエリ
            # 送信用のクエリ作成
        frm_count_array = self.frm_count.to_bytes(2, "big")
        wkfrm = array.array('B', [])
        wkfrm.extend(frm_count_array)
        wkfrm.extend(pp.frm_ExeOpe_TrgOFF)

        self.client.sendto(wkfrm,(self.address,self.port))
        rcvData  = self.client.recv(self.BUFSIZE)

        # print(rcvData)
        # print("rcvData[0]:",rcvData[7])
        self.frm_count += 1
    def get_target_position(self):
        return self.target_pos
        
    

if __name__ == '__main__':
    comm = Communication(address="192.168.1.20")
        #comm.get_current_position()
    print(comm.set_target_position(333201))
    comm.send_target_position()
    #time.sleep(1)
    while True:
        comm.get_current_position()
        time.sleep(1)