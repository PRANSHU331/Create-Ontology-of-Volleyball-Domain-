#!/usr/bin/env python
# coding: utf-8

# In[18]:


import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
import xml.etree.ElementTree as ET
import os
from rdflib import Graph,Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import  RDF, RDFS


# # Fetch data from XML

# In[ ]:



cwd=os.getcwd()

tree = ET.parse("FINAL_volleyball_data.xml")
root = tree.getroot()


# In[76]:


['Tournament Name', 'Location', 'Date', 'Venue', 'Organizer', 'Sponsors']


# In[20]:


waiters = []
AllWaiters = root.findall("Branch/Staff/Waiter")
for w in AllWaiters:
    wId = w.get('Id')
    name = w.find('Name')
    salary = w.find('Salary')
    contact = w.find('Contact')
    phn = contact[0]
    email = contact[1]
    waiters.append([wId,name.text,salary.text,phn.text,email.text])


# In[23]:


player = []
Allplayer = root.findall("tournament/teams/teams/team/players/player")

for player in Allplayer:
    player_name = player.find('name').text
    jersey = player.get('jersey')
    height = player.get('height')
    weight = player.get('weight')
    birthdate = player.get('birthdate')
    hometown = player.get('hometown')
    year = player.get('year')
    position = player.find('position').text
    player1.append([team_id, player_name, jersey, height, weight, birthdate, hometown, year, position])


# In[24]:


print(*player, sep = "\n")


# In[25]:


import csv
from xml.etree import ElementTree as ET

# Parse the XML data
tree = ET.parse('FINAL_volleyball_data.xml')
root = tree.getroot()


# In[41]:


tournament1=[]

tournament = root.find('tournament')
tournament1.append([
    tournament.find('name').text,
    tournament.find('location').text,
    tournament.find('date').text,
    tournament.find('venue').text,
    tournament.find('organizer').text,
    ', '.join([sponsor.text for sponsor in tournament.findall('sponsor')])
])


team1=[]
teams = tournament.find('teams')
for team in teams.findall('team'):
    team_id = team.get('teamID')
    team_name = team.find('name').text
    coach = team.find('coach').text
    team1.append([team_id, team_name, coach])

    # Write the players header
#     writer.writerow(['Team ID', 'Player Name', 'Jersey', 'Height', 'Weight', 'Birthdate', 'Hometown', 'Year', 'Position'])


allplayer=[]
for team in teams.findall('team'):
        team_id = team.get('teamID')
        for player in team.find('players').findall('player'):
            player_name = player.find('name').text
            jersey = player.get('jersey')
            height = player.get('height')
            weight = player.get('weight')
            birthdate = player.get('birthdate')
            hometown = player.get('hometown')
            year = player.get('year')
            position = player.find('position').text
            allplayer.append([team_id, player_name, jersey, height, weight, birthdate, hometown, year, position])

                       
match1=[]            
match = tournament.find('match')
match_id = match.get('id')
court = match.get('court')
team1 = match.find('team1')
team1_id = team1.get('teamref')
team1_captain = team1.get('captain')
team1_color = team1.get('color')
team1_serve_order = team1.get('serve_order')
team2 = match.find('team2')
team2_id = team2.get('teamref')
team2_captain = team2.get('captain')
team2_color = team2.get('color')
team2_serve_order = team2.get('serve_order')            
match1.append([match_id, court, team1, team1_id, team1_captain, team1_color, team1_serve_order, team2, team2_id,team2_captain,team2_color,team2_serve_order])


# In[32]:


print(*tournament1, sep = "\n")


# In[33]:


print(*team1, sep = "\n")


# In[34]:


print(*allplayer, sep = "\n")


# In[42]:


print(*match1, sep = "\n")


# In[35]:


g=Graph()
filename = cwd+"/A3.owl"
g.parse(filename, format='xml')
# g.(filename, format='xml')


# In[36]:


def isAlreadyDefined(subs):
    for s in g.subjects():
        if(subs in str(s)):
            return True
    return False

myNamespace="http://www.semanticweb.org/ajay/ontologies/2022/3/Volleyballonto"
namedIndividual = URIRef('http://www.w3.org/2002/07/owl#NamedIndividual')
rdftype = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


# In[44]:


triplets=[]
obj_properties=[]  
att_properties=[]  




arc_class=str(myNamespace)+"#allplayer"
for indv in allplayer:
    
    individualName=str(myNamespace)+"#"+str(indv[1]).replace(' ','_')
    arc_individual = URIRef(individualName)
    if(isAlreadyDefined(individualName)==False): 
        triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
        triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))

        subject=arc_individual
        #pred= URIRef(str(myNamespace)+"#id")
        literal=indv[0]
        att_properties.append( (subject, URIRef(str(myNamespace)+"#team_id")  , Literal(literal,datatype=XSD.string)) )
        att_properties.append( (subject, URIRef(str(myNamespace)+"#name"), Literal(indv[1],datatype=XSD.string)) )
        att_properties.append( (subject, URIRef(str(myNamespace)+"#position"), Literal(indv[2],datatype=XSD.string)) )


# In[46]:


att_properties[0]


# In[47]:


team1_class=str(myNamespace)+"#team"
for indv in team1:
    individualName=str(myNamespace)+"#"+str(indv[0])
    arc_individual = URIRef(individualName)
    if(isAlreadyDefined(individualName)==False): 
        triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
        triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))

        subject=arc_individual
        att_properties.append( (subject, URIRef(str(myNamespace)+"#orderDetails"), Literal(indv[2],datatype=XSD.string)) )


# In[50]:


team1_class=str(myNamespace)+"#team"
for indv in match1:
    individualName=str(myNamespace)+"#"+str(indv[0])
    arc_individual = URIRef(individualName)
    if(isAlreadyDefined(individualName)==False): 
        triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
        triplets.append((arc_individual,RDF.type, URIRef(namedIndividual)))

        subject=arc_individual
        att_properties.append( (subject, URIRef(str(myNamespace)+"#orderDetails"), Literal(indv[2],datatype=XSD.string)) )


# In[52]:


att_properties


# # Add object properties "hasplayer"
# #### Team hasplaer player
# #### Use attribute teamid hasplayer played in the XML to make the mapping

# In[54]:


for team in team1:
    individualName=str(myNamespace)+"#"+str(team[0]).replace(' ','_')  
    sub = URIRef(individualName)         
    pred=URIRef((myNamespace)+"#hasplayer")

    for ord in allplayer: 
        if(ord[0]==team[0]):
            individualName=str(myNamespace)+"#"+str(ord[0]).replace(' ','_') 
            obj = URIRef(individualName)
            obj_properties.append((sub,pred,obj))  


# # Add object properties "hasname"
# #### Order hasname name
# #### Use attribute teamid played team in the XML to make the mapping

# In[56]:


for order in allplayer:
    individualName=str(myNamespace)+"#"+str(order[0]).replace(' ','_')
    sub = URIRef(individualName)         
    pred=URIRef((myNamespace)+"#hasname")
    
    individualName=str(myNamespace)+"#"+str(order[1]).replace(' ','_') 
    obj = URIRef(individualName)
    obj_properties.append((sub,pred,obj))  


# In[57]:


print(*obj_properties, sep = "\n")


# # Print triplets

# In[61]:


for triplet in triplets:
    print(triplet)


# In[62]:


for o in obj_properties:
    print(o)


# In[63]:


for a in att_properties:
    print(a)


# In[65]:


print("Total Added Triples = ",int(len(triplets))+int(len(obj_properties))+int(len(att_properties)))
print(int(len(triplets)))
print(int(len(obj_properties)))
print(int(len(att_properties)))


# In[66]:


for i in triplets:
    g.add(i)

for i in obj_properties:
    g.add(i)

for i in att_properties:
    g.add(i)


# In[67]:


count= 0
for s,p,o in g:
    count +=1
print(count)


# In[68]:


g.serialize(destination="Volleyball_draft1.owl",format='xml')


# In[70]:


from owlready2 import *

onto_path.append(cwd)
onto = get_ontology("file://Volleyball_draft1.owl").load()


# In[71]:


print(type(onto))


# In[72]:


with onto: sync_reasoner()
onto.save("VolleyballOntologyRdf_syn.owl")


# In[73]:


import rdflib
g2=rdflib.Graph()
fl = "VolleyballOntologyRdf_syn.owl"
g2.parse(fl, format='xml')


# In[74]:


c=0
for t in g2.triples((None,None,None)):
    c+=1
print(c)


# In[75]:


from rdflib.compare import to_isomorphic, graph_diff
iso1 = to_isomorphic(g)
iso2 = to_isomorphic(g2)

in_both, in_first, in_second = graph_diff(iso1,iso2)

def dump_nt_sorted(g):
    for l in sorted(g.serialize(format='nt').splitlines()):
        if(l) : print(l)

dump_nt_sorted(in_second)


# In[ ]:




