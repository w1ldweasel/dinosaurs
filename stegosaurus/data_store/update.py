import neo4j
import os

from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
# desktop app setup - locally hosted
# TODO - where to host this?  need to change URI to appropriate location

#getting the credentials from environment variables
user = os.environ.get('USER')
pword = os.environ.get('PW')

driver = GraphDatabase.driver(uri, auth=(user, pword))
# default account, just to get things running

# TODO - retrieve data from processor, insert in CSV form? remove this hard coding
#use LOAD CSV function in Neo4j documentation

#Cypher query to write exploit node to DB
def create_exploit(tx, eID, cID):
     tx.run("CREATE (a:exploit {eID: $eID})-[:EXPLOITS]->(b:cve {cID: $cID})"
           , eID=eID, cID=cID)

#Create the reverse relationship (Bi Directional)
def reverse_cveexp(tx, cID, eID):
    tx.run("CREATE (b:cve {cID: $cID})-[:IS_EXPLOITED_BY]->(a:exploit {eID: $eID})"
           , cID=cID, eID=eID)

#run write exploit function
with driver.session() as session:
    exploitDB = '10259'
    CVEID = 'CVE-2009-4156'
    session.write_transaction(create_exploit, exploitDB, CVEID)
    #session.write_transaction(create_exploit, '10180', 'CVE-2009-4092')
    #session.write_transaction(create_exploit, '10180', 'CVE-2009-4091')
    #testing an exploit that impacts multiple CVEs

#run reverse function
with driver.session() as session:
    CVEIDrev = 'CVE-2009-4156'
    exploitDBrev = '10259'
    session.write_transaction(reverse_cveexp, CVEIDrev, exploitDBrev)
#    session.write_transaction(reverse_cveexp, 'CVE-2009-4092', '10180')
#    session.write_transaction(reverse_cveexp, 'CVE-2009-4091', '10180')


driver.close()
