import neo4j
import os

from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
# local desktop app setup
# TODO - where to host? change URI

#getting the credentials from environment variables
user = os.environ.get('USER')
pword = os.environ.get('PW')

driver = GraphDatabase.driver(uri, auth=(user, pword))
# default account, just to get things running

# TODO - receive query request from presentation layer

#Cypher query to get exploit details
#clear down list, run the Cypher query, loop through results & write to list
def get_exploit(tx, eID):
    edetails = []
    result = tx.run("MATCH (a:exploit)-[:EXPLOITS]->(b) WHERE a.eID = $eID "
                    "RETURN b.cID AS cID", eID=eID)
    for record in result:
        edetails.append(record["cID"])
    return edetails
#this allows iteration if exploit impacts multiple CVEs

#Cypher query to get CVE details
def get_CVE(tx, cID):
    cdetails = []
    result = tx.run("MATCH (b)-[:IS_EXPLOITED_BY]->(a) WHERE b.cID = $cID "
                    "RETURN a.eID AS eID", cID=cID)
    for record in result:
        cdetails.append(record["eID"])
    return cdetails
#this allows iteration if CVE has multiple exploits

#run read exploit function
#get list by running function with required input, loop through & print
with driver.session() as session:
    exploit = "10180"
    edetails = session.read_transaction(get_exploit, exploit)
    for cve in edetails:
        print(cve)
        print("%s is exploited by %s"%(cve, exploit))
        #just playing around with printing the query out

#run read CVE function
with driver.session() as session:
    cvenum = "CVE-2009-4186"
    cdetails = session.read_transaction(get_CVE, cvenum)
    for exploit in cdetails:
        print(exploit)
        print("%s exploits %s"%(exploit, cvenum))

# TODO - need to integrate with and send this output to presentation layer


driver.close()