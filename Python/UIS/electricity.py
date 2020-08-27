import PyPDF2, os
import numpy as np
from pathlib import Path
import pyinputplus as pyip

PATH = Path(
    Path.home() / "jose2" / "Documents" / "Stuff" / "UIS"/"Fourth Semester" / "ELECTRONIC"
)

def trabajo_medio_conmutación(potencia, t_phl, t_plh, factor = -3):
    p = unit(potencia, factor)
    t_prom = (unit(t_phl, -9) + unit(t_plh, -9))/(2)
    A = unit(p * t_prom, 0) 
    return A

def unit(valor , factor):
    if factor < 0:
        power = 1/np.power(10, -factor)
    else:
        power = np.power(10, factor)
    return valor * power


def fmax(t_phl, t_plh, factor = 3):
    time = unit(t_plh + t_plh, -9)
    f = unit(1/time, factor)
    return f

def leer_trabajo(familia = ''):
    power = pyip.inputFloat(f"Digite la potencia {familia}: ", limit=3, greaterThan=0)
    times = []
    for i in range(2):
        t_prom = pyip.inputFloat(f"Digite el tiempo {familia}: ", limit=3, greaterThan=0, blank=True)
        times.append(t_prom)
    factor = pyip.inputInt(f"Factor (opcional): ", blank=True)
    if not factor:
        factor = -3
    A = trabajo_medio_conmutación(power, times[0],times[1], factor= factor)
    return A

def menu():
    while True:
        options = ["Trabajo medio de conmutación","Comparar familias", "Frecuencia maxima", "Salir"]
        for index,opc in enumerate(options,1):
            print(f"[{index}] {opc}")
        
        opc = pyip.inputInt("Opcion: ", limit = 1, min = 1,blank = True, max = len(options))
        times = []
        if opc == len(options):
            break
        
        elif opc == 1:
            A = leer_trabajo()       
            print(f"Trabajo medio: {A} [J]")
        
        elif opc == 2:
            A1 = leer_trabajo(familia = "Familia 1")  
            A2 = leer_trabajo(familia = "Familia 2")       
            print(f"Familia 1: Trabajo medio {A1} [J]")
            print(f"Familia 2: Trabajo medio {A2} [J]")
            if A1 < A2:
                print("La Familia 1 es MEJOR")
            else:
                print("La Familia 2 es MEJOR")

        elif opc == 3:
            for i in range(2):
                t_prom = pyip.inputFloat("Digite el tiempo: ", limit=3, greaterThan=0, blank=True)
                times.append(t_prom)
            factor = pyip.inputFloat(f"Factor (opcional): ", blank = True) 
            if not factor:
                factor = -3     
            f = fmax(times[0],times[1], factor = factor)  
            
            print(f"Frecuencia maxima: {f} [MHz]")


""" search for a key sentence through all PDFs of electricty subject"""
class Matcher():
    def __init__(self, pattern, unit):
        self.path = PATH / unit
        self.set_pattern(pattern)
        self.search()
    
    def set_pattern(self, pattern):
        length = len(pattern)
        if length > 15:
            middle = int(length/2)
            self.pattern = [pattern[:middle], pattern[middle:]]
        else:
            self.pattern = [pattern]
    
    def search(self):
        """ """
        pdfs = self.find_pdfs()
        if not pdfs:
            return
        pattern = self.pattern
        matches = []
        # search in each pdf the target pattern
        for pdf in pdfs:
            with open(pdf, "rb") as pdf_file:
                pdf_obj = PyPDF2.PdfFileReader(pdf_file)

                for numpage in range(pdf_obj.numPages): #check in every page for the pattern
                    page = pdf_obj.getPage(numpage)
                    raw = page.extractText()

                    if [sub for sub in pattern if sub in raw]: # if match, parse the page text
                        text = self.find_matches(page)
                        data = (text, pdf, numpage)
                        matches.append(data)
        if matches:
            self.organize(matches)
        else:
            mssg = " ".join(pattern)
            print(f"[INFO] '{mssg}' keyword wasn't found.")
    
    def organize(self, data):
        for match in data:

            text, pdf, page = match
            for index, paragraph in enumerate(text,1):
                print(f"[{index}] {paragraph}")
            
            print(f"Fuente: {pdf}, page: {page + 1}")

    def parse_page(self, raw_text):
        segments = raw_text.split(r"\n")
        text = [segment.replace("\n","") for segment in segments]
        return text

    def find_matches(self, page):
        text = self.parse_page(page.extractText())
        target_segments = []
        for segment in text:
            if self.pattern[0] in segment:
                target_segments.append(segment)

        assert target_segments
        return target_segments


    def find_pdfs(self):
        assert hasattr(self, "path")
        if not os.path.exists(str(self.path)):
            print(f"[INFO] Unit {self.path.name} not created yet.")
            return
        if not self.path.is_dir():
            print("Given path is not a directory.")
            return
        path = self.path
        os.chdir(str(self.path))
        pdfs = []
        for directory, directories, files in os.walk(path):
            for file in files:
                if file.endswith("pdf"):
                    pdfs.append(file)
        
        if pdfs:
            return pdfs
        print("[INFO] No pdfs were found.")



if __name__ == "__main__":
    Matcher("tiempo", "3")
    # menu()
    



