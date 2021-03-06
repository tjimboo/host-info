"""
Resolve the IP address of a given domain
data returned is in the format:
@filename 
@version 1.01 (python ver 2.7.3)
@author tjimboo
fqdn2 = socket.gethostbyname('tls.pki.nu')
"""
#import socket
import sys
import ssl, socket
import whois

addr  = input("What address do you want resolve?: ")

try:fqdn1 = socket.gethostbyname(addr)
except socket.gaierror:
    # this means we could not resolve the host
    print ("There was an error resolving the host.\nCheck your spelling and try again.")
    sys.exit()


print ("The requested domain name", addr, "resolves to IP address",  fqdn1)


#Check if ports are open
#FYI- You can test for a UDP port by changing “socket.SOCK_STREAM” to “socket.SOCK_DGRAM” 
# TODO test multiple ports
host = addr
port = 443

portsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
 portsocket.connect((host, port))
 portsocket.shutdown(2)
 print ("Success connecting to", host + " on port: " + str(port))

except:
 print ("Cannot connect to ")
 print (host + " on port: " + str(port))
 sys.exit ("Seems port 443 is not open.\nScript has stopped.")

#Fetch Issuer CA and show information
hostname = addr
ctx = ssl.create_default_context()
ss = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
ss.connect((hostname, 443))
cert = ss.getpeercert()

subject = dict(x[0] for x in cert['subject'])
issued_to = subject['commonName']
issuer = dict(x[0] for x in cert['issuer'])
issued_by = issuer['commonName']
valid_to =  cert['notAfter']
#san = cert['subjectAltName']

print ("Server certificate issued to:", issued_to)
print ("Server certificate issued by:", issuer['commonName'])
print ("Valid to::", valid_to) 
#print ("SubjectAltName", san)

#Get WHOIS info for selected domain

w = whois.whois(addr)
print ("WHOIS-STATUS:", w['status'])
print ("Is host using DNSSEC:", w['dnssec'])
print ("Expiration date:", w['expiration_date'])
print ("Name Servers:", w['name_servers'])
