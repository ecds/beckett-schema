import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import os
import csv
import re
import xml.etree.ElementTree as ET

infile = sys.argv[1]
outdir = sys.argv[2]

'''
Code,Year,Month,Day,
PhysDes,LeavesSides,Envelope,Postmark,
Repository,Sender,PlaceWritten,PlaceSent,
Transcriber,OwnerProp,TranscriDate,Translator,
TranslatDate,Copied,Publish,Volume,PrevPubl,PlacePrevPubl,
Prev Pub Con't,Additional,DateEntry,EntryDate,PrimaryLang,
Recipient,OwnerRights,File,Previously Published
'''

with open(infile, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        filename = '_'.join([row['Year'], row['Month'].zfill(2), row['Day'].zfill(2), \
                            row['Recipient'].title(), row['Code']])
        filename = re.sub(' ', '_', filename)
        
        letter = ET.Element('letter')
        metadata = ET.SubElement(letter, 'metadata')
        content = ET.SubElement(letter, 'content')

        # change keys to preferred metadata elements
        metadata_elements = {'code': 'Code', 
                            'recipient': 'Recipient'}
                            # 'physical_description': 'PhysDes',
                            # 'leaves_sides': 'LeavesSides',
                            # 'envelope': 'Envelope',
                            # 'postmark': 'Postmark',
                            # 'respository': 'Repository',
                            # 'place_written': 'PlaceWritten',
                            # 'place_sent': 'PlaceSent',
                            # 'primary_language': 'PrimaryLang'}

        for k in metadata_elements.keys():
            element = ET.SubElement(metadata, k)
            element.text = row[metadata_elements[k]]

        #h/t http://stackoverflow.com/a/9092358
        declaration = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-model href="https://raw.githubusercontent.com/emory-libraries-ecds/beckett-schema/master/beckett.rnc"?>
<?xml-stylesheet type="text/css" href="https://raw.githubusercontent.com/emory-libraries-ecds/beckett-schema/master/beckett.css"?>\n'''

        tree = ET.ElementTree(letter)
        out = os.path.join(outdir, os.path.basename(filename + '.xml'))
        with open(out, 'w') as outfile:
            outfile.write(declaration)
            tree.write(outfile, xml_declaration=False, encoding='utf-8') 
            outfile.close()

