import random

from Backend.Encryption.HexaPrism import HexaPrismEncryption
from Backend.Encryption.OctaPrism import OctaPrismEncryption
from Backend.Encryption.Octahedron import OctahedronEncryption
from Backend.Encryption.PentaPrism import PentaPrismEncryption
from Backend.Encryption.PentaPyramid import PentaPyramidEncryption
from Backend.Encryption.Steganography_Encryption import StegoEncryption


class Controller:
    def __init__(self):
        
        self.plain_text = ""
        self.zero_flag = False
        self.cipher = ""
        self.s1 = ""
        self.s2 = ""
        self.equivalent_ascii = ""
        self.key = ""

    def main(self,plain_text):
        self.plain_text = plain_text
        self.n = len(self.plain_text)
    
        for i in range(0, self.n):
            self.each = str(ord(self.plain_text[i]))
            self.equivalent_ascii += self.each
       
        self.len_of_ascii = len(self.equivalent_ascii)
        self.split = self.len_of_ascii / 2
        for i in range(self.len_of_ascii):
            if i < self.split:
                self.s1 += self.equivalent_ascii[i]
            elif i >= self.split and i < self.len_of_ascii:
                self.s2 += self.equivalent_ascii[i]
     
        if self.s2[0] == '0':
            self.zero_flag = True
       
        self.identification_of_algorithm()

     
        self.identification_of_key()
      
        self.cipher = str(str(self.which_algorithm) + str(self.which_key) + str(self.cipher))
       
        return (1,len(self.cipher),self.which_algorithm,self.Image_Steganography())

    def identification_of_algorithm(self):
        self.which_algorithm = random.randint(1,5)
        if self.which_algorithm == 1:
            octa = OctahedronEncryption()
            self.cipher = octa.encry(self.s1,self.s2)
        elif self.which_algorithm == 2:
            hexa = HexaPrismEncryption()
            self.cipher = hexa.encry(self.s1,self.s2)
        elif self.which_algorithm == 3:
            penta = PentaPrismEncryption()
            self.cipher = penta.encry(self.s1,self.s2)
        elif self.which_algorithm == 4:
            oprism = OctaPrismEncryption()
            self.cipher = oprism.encry(self.s1,self.s2)
        elif self.which_algorithm == 5:
            pprism = PentaPyramidEncryption()
            self.cipher = pprism.encry(self.s1,self.s2)


    def identification_of_key(self):
        self.which_key = random.randint(1,3)
        if self.which_key == 1:
            self.key = str(self.s1)
        elif self.which_key == 2:
            a_square = str(int(self.s1) * int(self.s1))
            self.key = str(a_square)
        else:
            self.key = str(self.s2)

    def Image_Steganography(self):
        imgste = StegoEncryption()
        self.cipher_text = str(str(self.cipher)+'.'+str(self.key)+str(int(self.zero_flag)))

        num = random.randint(1,10)
        path = ".\\Backend\\Assets\\"
        img = path+"I"+str(num)+".png"
        encrypted_img = imgste.encode(img,self.cipher_text)
        
     
        return encrypted_img

