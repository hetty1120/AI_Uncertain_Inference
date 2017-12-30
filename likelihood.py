
# coding: utf-8

# In[121]:

import xml.dom.minidom
from xml.dom.minidom import parse
import random
import re
import time


# In[122]:

def event_values(event, parents_list):
    return tuple([event[i] for i in parents_list])


# In[123]:

class Bayes_node:
    
    def __init__(self, var, values, parents, table):
        self.var = var
        self.values = values
        self.parents = parents
        self.cpt = table
        self.children = []
        
    def get_possibility(self, value, event):
        get_value = event_values(event, self.parents)
        return self.cpt[tuple([value])][get_value]


# In[124]:

class Bayes_DAG:
    
    def __init__(self, expressions):
        self.nodes = []
        self.variables = []
        total = len(expressions)
        give_node = {}
        for expression in expressions:
            give_node[tuple([expression[0]])] = False
            
        # construct DAG (make sure the variables order is right)
        while total > 0:
            for expression in expressions:
                if give_node[tuple([expression[0]])] == False:
                    result = self.add(expression)
                    if result == True:
                        give_node[tuple([expression[0]])] = True
                        total -= 1
        
            
    def add(self, expression):
        node = Bayes_node(*expression)
        if all((parent in self.variables) for parent in node.parents) == False:
            return False
        self.variables.append(node.var)
        self.nodes.append(node)
        for parent in node.parents:
            self.find_node(parent).children.append(node)
        return True
    
    def find_node(self, var):
        for node in self.nodes:
            if node.var == var:
                return node
            
    def find_values(self, var):
        return self.find_node(var).values


# In[125]:

def parse_xml(filename):

    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    nodes = collection.getElementsByTagName("VARIABLE")
    
    bayes_net = []
    
    variables = {}
    
    # read variables
    for node in nodes:
        
        var = node.getElementsByTagName('NAME')[0].childNodes[0].data
        values = node.getElementsByTagName("OUTCOME")
        values_list = [i.childNodes[0].data for i in values]
        variables[var] = values_list
    
    nodes = collection.getElementsByTagName("DEFINITION")
    
    
    # read possibility distribution table
    for node in nodes:
        
        name = node.getElementsByTagName('FOR')[0].childNodes[0].data
        
        parents = node.getElementsByTagName("GIVEN")
        parents_list = [i.childNodes[0].data for i in parents]
            
        table = node.getElementsByTagName("TABLE")
        
        p_table = {}
        
        for value in variables[name]:
            p_table[tuple([value])] = {}

        if len(parents_list) == 0:
            p_numbers = table[0].childNodes[0].data.split()
            p_table[tuple(["true"])] = {():float(p_numbers[0])}
            p_table[tuple(["false"])] = {():float(p_numbers[1])}
        
        else: 
            for i in range(3,table[0].childNodes.length):
                exp = table[0].childNodes[i].data.split()
                if ((parents_list[0]) in exp) or (("!"+parents_list[0]) in exp):
                    parents_combination = []
                    for string in exp:
                        if string.startswith("!"):
                            parents_combination.append("false")
                        else:
                            parents_combination.append("true")
                    parents_combination = tuple(parents_combination)
                else:
                    p_table[tuple(["true"])][parents_combination] = float(exp[0])
                    p_table[tuple(["false"])][parents_combination] = float(exp[1])

        bayes_net.append([name,variables[name],parents_list,p_table])
    
    return bayes_net


# In[126]:

def parse_bif(filename):
    
    readfile = open(filename)
    readfile.readline()
    readfile.readline()
    
    prior_probability_pattern_1 = re.compile(r"probability \( ([^|]+) \) \{\s*")
    prior_probability_pattern_2 = re.compile(r"  table (.+);\s*")
    conditional_probability_pattern_1 = (re.compile(r"probability \( (.+) \| (.+) \) \{\s*"))
    conditional_probability_pattern_2 = re.compile(r"  \((.+)\) (.+);\s*")
    
    variables = {}
    
    bayes_net = []
    
    while True:
        
        line = readfile.readline()
        
        if not line:
            break
            
        if line.startswith("variable"):
            
            var = line[9:-3]
            new_line = readfile.readline()
            indexa = new_line.find("{")
            indexb = new_line.find("}")
            new_line = new_line[indexa+2:indexb-1]
            variables[var] = new_line.split(", ")
            
            readfile.readline()
        
        elif line.startswith("probability"):
            
            match = prior_probability_pattern_1.match(line)
            
            if match:
                
                # prior probabilities:
                variable = match.group(1)
                parents = []
                line = readfile.readline()
                match = prior_probability_pattern_2.match(line)
                p = [float(i) for i in match.group(1).split(', ')]
                table = {}
                for i in range(len(variables[variable])):
                    value = variables[variable][i]
                    table[tuple([value])] = {():p[i]}
                
                readfile.readline()  
                
            else:
                match = conditional_probability_pattern_1.match(line)
                if match:
                    variable = match.group(1)
                    parents = match.group(2).split(', ')
                    table = {}
                    for value in variables[variable]:
                        table[tuple([value])] = {}
                    
                    while True:
                        line = readfile.readline()
                        if line.startswith("}"):
                            break
                        match = conditional_probability_pattern_2.match(line)
                        given = match.group(1).split(', ')
                        p = [float(i) for i in match.group(2).split(', ')]
                        for i in range(len(variables[variable])):
                            value = variables[variable][i]
                            table[tuple([value])][tuple(given)] = p[i]
                            
            bayes_net.append([variable,variables[variable],parents,table])

    return bayes_net


# In[127]:

def normalize(result):
    result_sum = 0
    
    for i in result:
        result_sum += result[i]
    
    if result_sum == 0:
        print(result)
        return True
    
    for i in result:
        result[i] = result[i]/result_sum
        
    print(result)


# In[128]:

def generate_sampling(bn,evidence):
    
    sample = {}
    w = 1.0
    
    for var in bn.variables:
        if var in evidence:
            var_node = bn.find_node(var)
            p = var_node.get_possibility(evidence[var],sample)
            w = w * p
            sample[var] = evidence[var]
        else:
            var_node = bn.find_node(var)
            start = 0
            number = random.random()
            for value in bn.find_values(var):
                p = var_node.get_possibility(value,sample)
                start += p
                if number <= start:
                    sample[var] = value
                    break
        
            
    return sample,w


# In[129]:

def likelihood_sampling(var,evidence,bn,times):
    
    result = {}
    for value in bn.find_values(var):
        result[value] = 0
    
    for i in range(times):
        sample, w = generate_sampling(bn,evidence)
        result[sample[var]] += w
            
    return normalize(result)


# In[130]:

while True:
    print("Please type the filename, the sampling times, the query variable and evidence variables in one line(if no more question, please type END)")
    line = input()
    if line == "END":
        break
    else:
        line = line.split(" ")
        filename = line[0]
        if filename.endswith("bif"):
            net_construct = parse_bif(filename)
        elif filename.endswith(".xml"):
            net_construct = parse_xml(filename)
        else:
            Raise
        
        bn = Bayes_DAG(net_construct)
        
        times = int(line[1])
        
        q_var = line[2]
        evidence = {}
        
        for i in range(3,len(line)):
            if line[i] in bn.variables:
                evidence[line[i]] = line[i+1]
            else:
                continue
                
    starttime = time.time()
    
    likelihood_sampling(q_var,evidence,bn,times)
    
    endtime = time.time()
    
    print("time cost:%.2f"%(endtime-starttime))


# In[ ]:



