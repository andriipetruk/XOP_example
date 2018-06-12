import email.Parser
import xml.etree.ElementTree as ET
import json


def main(filename):
    
    # open file in FS
    inputFile = open(filename, "r")
    p = email.Parser.Parser()
    msg = p.parse(inputFile)
    inputFile.close()
    
    # splitting file to parts
    partCounter = 1
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        name = part.get_param("name")
        if name == None:
            name = "part-%i" % partCounter
        partCounter+=1
        # write a part to disk
        fileOutput = filename+"_part_"+str(partCounter)
        f = open(fileOutput, "wb")
        f.write(part.get_payload(decode=1))
        f.close()
        # trying parsing a part of the file as XML
        try:
          tree = ET.parse(fileOutput)
        except:
          pass 
          jsonData = {}
          # reading elements of a XML as KV and creating JSON
          for elem in tree.iter(tag='submitClaim'):
             for i in elem:
                 key = i.tag
                 value = i.text
                 jsonData[key] = value
          jsonRaw = json.dumps(jsonData)
          print jsonRaw  


if __name__=="__main__":
    main('licence')
