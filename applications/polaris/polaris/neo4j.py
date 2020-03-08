#!/usr/bin/python3
from py2neo import Graph, Node, Relationship
 

#graph = Graph('http://localhost:7474', username='test', password='test2020')
graph = Graph()
test_node_1 = Node(label='test', name='king')
test_node_2 = Node(label='test', name='queen')
test_node_3 = Node(label='test', name='princess')
#r = Relationship(test_node_1, 'loves', test_node_2)
t = graph.begin()
t.create(test_node_1)
t.commit()
