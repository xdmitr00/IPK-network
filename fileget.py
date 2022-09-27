#author: Daria Dmitrievich
import socket
import sys
import re
import os.path

def get(SURL,NAMESERVER):
    if re.match("^fsp:\/\/[a-zA-Z0-9\-_\.]+\/[a-zA-Z0-9\/\-_\.]*[(a-zA-Z0-9\-_\.)+|\*]$",SURL):
        server = SURL[6:SURL.find('/',7)] 
        string = SURL[::-1]
        name = string[0:string.find('/')] 
        name = name[::-1]
        PATH = SURL[SURL.find('/',7)+1:len(SURL)]  
    else: 
        sys.exit("Chyba,nespravne argument SURL")
    if re.match("^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$",NAMESERVER):
        IPadress = NAMESERVER[0:NAMESERVER.find(':')]
        port = NAMESERVER[::-1]
        sPort = port[0:port.find(':')]
        sPort = int (sPort[::-1]) 
    else:
        sys.exit("Chyba,nespravne NAMESERVER")
       
     
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    adress=(IPadress,sPort)
    client.settimeout(30)
    try:
        client.connect(adress)
        client.send(("WHEREIS " + server).encode('utf-8'))
        req = client.recv(1024).decode('utf-8')
    except socket.timeout:
        sys.exit("Chyba, zadna odezva2")
    client.close

    
    if req:
        if req.find('OK') != -1:
            IPadress = req[3:req.find(':')]
            port = req[::-1]
            sPort = port[0:port.find(':')]
            sPort = int(sPort[::-1])
            adress=(IPadress,sPort)
            client2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client2.settimeout(30)
            try:
                client2.connect(adress)
                client2.send(("GET " + PATH +" FSP/1.0\r\nHostname: " + server +"\r\nAgent: xdmitr00\r\n\r\n").encode('utf-8'))
                req2 = client2.recv(1024).decode('utf-8')
            except socket.timeout:
                sys.exit("Chyba, zadna odezva2")
            client2.close
            if req2:
                if req2.find('Success') != -1:
                    leng = int(req2[req2.find(':') + 1 : req2.find('\r\n\r\n')])
                    zapis = req2[req2.find('\r\n\r\n') + 4 : len(req2)]
                    if os.path.isfile(name):
                        i = 1
                        while os.path.isfile(name + str(i)):
                            i=i+1
                        name = name + str(i)
                    soub = open(name,'w')
                    if not(zapis):
                        try:
                            zapis = client2.recv(1024).decode('utf-8')
                        except socket.timeout:
                            sys.exit("Chyba, zadna odezva3")
                    pocet = 0;
                    while zapis:
                        soub.write(zapis)
                        pocet = pocet + len(zapis);
                        try:
                            zapis = client2.recv(1024).decode('utf-8')
                        except socket.timeout:
                            sys.exit("Chyba, zadna odezva2")
                    soub.close()
                    if leng == pocet:
                        sys.exit(0)
                    else:
                        print(leng)
                        print(pocet)
                        sys.exit("chyba, nedokoncilo stahovani")
                
                else:
                     sys.exit("Chyba req2" + req2)
            else:
                  sys.exit("chyba, zadna odezva")        
        else:
            sys.exit("Chyba req" + req)
    else:
        sys.exit("chyba, zadna odezva")

    



if len(sys.argv) == 5:
    if sys.argv[1] == "-f": 
        if sys.argv[3] == "-n":
            get(sys.argv[2],sys.argv[4])
    elif sys.argv[1] == "-n": 
        if sys.argv[3] == "-f":
            get(sys.argv[4],sys.argv[2])
    else:
        sys.exit("chyba argv")
else:
    sys.exit("chyba argv")

