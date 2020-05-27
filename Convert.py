#-*- coding: utf-8 -*-

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import time
import os
import sys

class XMLHandler:
    def __init__(self, xml_path: str or Path):
        self.xml_path = Path(xml_path)
        self.root = self.__open()

    def __open(self):
        with self.xml_path.open() as opened_xml_file:
            self.tree = ET.parse(opened_xml_file)
            return self.tree.getroot()

def converter(xml_files: str, output_folder: str) -> None:
    xml_files = sorted(list(Path(xml_files).rglob("*.xml")))
    #On ouvre le fichier en lecture
    fichier = open("manifest.temp","w+")
    fichier.write("[")
    
    for _, xml in enumerate(xml_files, start=1):
        xml_content = XMLHandler(xml)

        for _,sg_box in enumerate(xml_content.root.iter('annotation')):
            


            for _, sg_box_ in enumerate(xml_content.root.iter('object')):

                fichier.write("{\"image\":\"" + sg_box.find("filename").text + "\",")
                fichier.write("\"annotations\":[")
                fichier.writelines("\n")

                #On calcule les boudind boxes
                width = int(sg_box_.find("bndbox").find("xmax").text) - int(sg_box_.find("bndbox").find("xmin").text)
                height = int(sg_box_.find("bndbox").find("ymax").text) - int(sg_box_.find("bndbox").find("ymin").text)
                y = int(sg_box_.find("bndbox").find("ymin").text)
                x = int(sg_box_.find("bndbox").find("xmin").text)

                fichier.write("{\"label\":\"" + sg_box_.find("name").text + "\",")
                fichier.write("\"coordinates\":{")

                fichier.write("\"x\":" + str(x) + " ")
                fichier.write("\"y\":" + str(y) + " ")
                fichier.write("\"width\":" + str(width) + " ")
                fichier.write("\"height\":" + str(height) + "}")
                fichier.writelines("}\n")

                fichier.write("]},")
                fichier.writelines("\n")


    fichier.write("]")
    fichier.close()

    #On remplace ,] par ]
    fin = open('manifest.temp', 'r+')
    fout = open('manifest.json', 'w+')

    for line in fin:
	    fout.write(line.replace(',]', ']'))

    fin.close()
    fout.close()
    os.remove('manifest.temp')

  
if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('USAGE: {} repertoire'.format(sys.argv[0]))
	else:
		t1 = time.time()
		XML_FOLDER = sys.argv[1]
		OUTPUT_FOLDER =  "."

		converter(XML_FOLDER, OUTPUT_FOLDER)
		print('Temps de Traitement : %d ms'%((time.time()-t1)*1000))
