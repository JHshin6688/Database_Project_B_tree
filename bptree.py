# Check carefully the format of the tree representation in text
# Note that the last node in each branch or level (including the root) is denoted by `-
# The file name must be bptree.py (case sensitive)
# The class name must be BPTree (case sensitive)
# Let's fix n to be 5. That is, a node can hold up to 4 search keys
# Let's assume that there is NO duplicate key

class BPTree(object):
    class Node:
        def __init__(self):
            self.top = True
            self.leaf = True
            self.parent = None
            self.value = []
            self.num_list = []
            self.child_nodes = []

    def __init__(self):
        self.root = self.Node()

    def insert(self, node, key):
        root = node

        while node.leaf == False:
            index = 0
            a = node.value

            while index < len(a):
                if key < a[index]:
                    break
                index += 1

            node = node.child_nodes[index]

        node.num_list.append(key)
        node.num_list.sort()

        if(len(node.num_list) == 5):
            child1 = self.Node()
            child2 = self.Node()
            child1.num_list = node.num_list[0:2]
            child2.num_list = node.num_list[2:5]
            delete_node = node.num_list
            child1.top = False
            child2.top = False

            if node.parent != None:
                node = node.parent

            child1.parent = node
            child2.parent = node
            node.leaf = False

            if node.child_nodes != []:
                for i in node.child_nodes:
                    if i.num_list == delete_node:
                        break
                node.child_nodes.remove(i)

            node.child_nodes.append(child1)
            node.child_nodes.append(child2)

            node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)


            node.value.append(child2.num_list[0])
            node.value.sort()

            #non-leaf nodes update
            if(len(node.value) == 5):
                while len(node.value) == 5:
                    node1 = self.Node()
                    node2 = self.Node()
                    node1.value = node.value[0:2]
                    node2.value = node.value[3:5]
                    save = node.value[2]
                    node1.child_nodes = node.child_nodes[0:3]
                    node2.child_nodes = node.child_nodes[3:6]
                    node1.top = False
                    node2.top = False
                    node1.leaf = False
                    node2.leaf = False
                    delete = node.value

                    for i in range(3):
                        node1.child_nodes[i].parent = node1
                        node2.child_nodes[i].parent = node2

                    if node.top == True:
                        count = len(node.child_nodes)
                        for j in range(count):
                            node.child_nodes.pop()

                        node.child_nodes.append(node1)
                        node.child_nodes.append(node2)
                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.value)
                        node1.parent = node
                        node2.parent = node
                        node.value = [save]
                        node.leaf = False
                        node.num_list = []


                    else:
                        node = node.parent
                        node.value.append(save)
                        node.value.sort()

                        for i in node.child_nodes:
                            if i.value == delete:
                                break
                        node.child_nodes.remove(i)
                        node.child_nodes.append(node1)
                        node.child_nodes.append(node2)
                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.value)
                        node1.parent = node
                        node2.parent = node
                        node.leaf = False

        return root

    def get_index(self, node):
        children = node.parent.child_nodes
        for i in range(len(children)):
            if children[i].value == node.value:
                break
        
        return i

    def delete(self, node, key):
        root = node
        index = 0

        while node.leaf == False:
            a = node.value
            index = 0
            while index < len(a):
                if key < a[index]:
                    break
                index += 1
            node = node.child_nodes[index]


        if len(node.num_list) >= 3:
            node.num_list.remove(key)
            return root

        else:
            if node.top == True:
                node.num_list.remove(key)

            else:             
                if index == len(node.parent.child_nodes) -1:
                    node.num_list.remove(key)
                    val = node.num_list[0]
                    node.parent.child_nodes[index -1].num_list.append(val)
                    node.parent.child_nodes[index -1].num_list.sort()
                    keep = node.parent.child_nodes[index -1].num_list

                    node = node.parent
                    node.value.pop()
                    del node.child_nodes[index]

                else:
                    node.num_list.remove(key)
                    val = node.num_list[0]
                    node.parent.child_nodes[index +1].num_list.append(val)
                    node.parent.child_nodes[index +1].num_list.sort()
                    keep = node.parent.child_nodes[index +1].num_list

                    node = node.parent
                    del node.value[index]
                    del node.child_nodes[index]                    

                if node.top == True:
                    if len(node.child_nodes) == 1:
                        if len(node.child_nodes[0].num_list) == 5:
                            new_child = self.Node()
                            new_child.top = False
                            new_child.leaf = True
                            new_child.parent = node

                            if index == len(node.child_nodes):
                                new_child.num_list = keep[3:5]
                                node.child_nodes[0].num_list = keep[0:3]
                                node.value = [keep[3]]

                            else:
                                new_child.num_list = keep[2:5]
                                node.child_nodes[0].num_list = keep[0:2]
                                node.value = [keep[2]]

                            node.child_nodes.append(new_child)
                            node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)
                            

                        else:
                            node.value = []
                            node.num_list = node.child_nodes[0].num_list
                            node.leaf = True
                            node.child_nodes.pop()
                            
                    else:
                        if len(keep) == 5:
                            child1 = self.Node()
                            child2 = self.Node()
                            child1.top = False
                            child2.top = False

                            if index == len(node.child_nodes):
                                child1.num_list = keep[0:3]
                                child2.num_list = keep[3:5]
                                node.value.append(keep[3])
                            
                            else:
                                child1.num_list = keep[0:2]
                                child2.num_list = keep[2:5]
                                node.value.append(keep[2])

                            node.value.sort()
                            child1.parent = node
                            child2.parent = node
                            for i in range(len(node.child_nodes)):
                                if node.child_nodes[i].num_list == keep:
                                    break
                            
                            del node.child_nodes[i]
                            node.child_nodes.append(child1)
                            node.child_nodes.append(child2)
                            node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)
                
                else:
                    if len(keep) == 5:
                        child1 = self.Node()
                        child2 = self.Node()
                        child1.top = False
                        child2.top = False

                        if index == len(node.child_nodes):
                            child1.num_list = keep[0:3]
                            child2.num_list = keep[3:5]
                            node.value.append(keep[3])
                        
                        else:
                            child1.num_list = keep[0:2]
                            child2.num_list = keep[2:5]
                            node.value.append(keep[2])
                                                    
                        node.value.sort()
                        child1.parent = node
                        child2.parent = node
                        for i in range(len(node.child_nodes)):
                            if node.child_nodes[i].num_list == keep:
                                break
                        
                        del node.child_nodes[i]
                        node.child_nodes.append(child1)
                        node.child_nodes.append(child2)
                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)

                    index = self.get_index(node)

                    if len(node.child_nodes) == 2:
                        while len(node.child_nodes) == 2:
                            length = len(node.parent.child_nodes)
                            index = self.get_index(node)

                            if index == length -1:
                                target_node = node.parent.child_nodes[index -1]
                                index -= 1
                            else:
                                target_node = node.parent.child_nodes[index +1]


                            if len(target_node.value) == 2:
                                if len(node.parent.value) == 1:
                                    for child in node.child_nodes:
                                        node.parent.child_nodes.append(child)
                                        child.parent = node.parent

                                    for child in target_node.child_nodes:
                                        node.parent.child_nodes.append(child)
                                        child.parent = node.parent
                                    
                                    for i in range(2):
                                        del node.parent.child_nodes[0]
                                    
                                    for v in node.value:
                                        node.parent.value.append(v)
                                    
                                    for v in target_node.value:
                                        node.parent.value.append(v)
                                    
                                    node.parent.value.sort()
                                    if node.parent.child_nodes[0].leaf == True:
                                        node.parent.child_nodes = sorted(node.parent.child_nodes, key=lambda x: x.num_list)

                                    else:
                                        node.parent.child_nodes = sorted(node.parent.child_nodes, key=lambda x: x.value)

                                    node = node.parent
                                
                                else:
                                    target_node.value.append(node.parent.value[index])
                                    target_node.value.append(node.value[0])
                                    del node.parent.value[index]
                                    target_node.value.sort()

                                    for i in range(2):
                                        target_node.child_nodes.append(node.child_nodes[i])
                                        node.child_nodes[i].parent = target_node
                                    
                                    node.parent.value.sort()
                                    if target_node.child_nodes[0].leaf == True:
                                        target_node.child_nodes = sorted(target_node.child_nodes, key=lambda x: x.num_list)

                                    else:
                                        target_node.child_nodes = sorted(target_node.child_nodes, key=lambda x: x.value)


                                    delete = node.value
                                    node = node.parent
                                    for i in range(len(node.child_nodes)):
                                        if node.child_nodes[i].value == delete:
                                            break

                                    del node.child_nodes[i]

                            else:
                                alpha = self.get_index(node)

                                num = node.parent.value[index]
                                node.value.append(num)
                                node.value.sort()

                                if alpha == index:      # merge with the right node
                                    node.child_nodes.append(target_node.child_nodes[0])
                                    target_node.child_nodes[0].parent = node
                                    del target_node.child_nodes[0]

                                    if node.child_nodes[0].leaf == True:
                                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)
                                    else:
                                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.value)

                                    new = target_node.value[0]
                                    del target_node.value[0]
                                    del node.parent.value[index]
                                    node.parent.value.append(new)
                                    node.parent.value.sort()
                                    node = node.parent

                                else:                   #merge with the left node
                                    count = len(target_node.child_nodes) -1
                                    node.child_nodes.append(target_node.child_nodes[count])
                                    target_node.child_nodes[count].parent = node
                                    del target_node.child_nodes[count]

                                    if node.child_nodes[0].leaf == True:
                                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.num_list)
                                    else:
                                        node.child_nodes = sorted(node.child_nodes, key=lambda x: x.value)     

                                    new = target_node.value[count -1]                           
                                    del target_node.value[count -1]
                                    del node.parent.value[index]
                                    node.parent.value.append(new)
                                    node.parent.value.sort()
                                    node = node.parent

                            if node.top == True:
                                break  
            return root

    def regular_node(self, node, start_string, last):
        #start_string = "   |"
        #start_string = "    "
        string = start_string
        if node.leaf == True:
            if last == False:
                string += "  |- {}\n".format(node.num_list)
            else:
                string += "  `- {}\n".format(node.num_list)

        else:
            count3 = len(node.child_nodes)
            if last == False:
                string += "  |- {}\n".format(node.value)
                start_string += "  |"
                for k in range(count3):
                    if k != count3 -1:
                        string += self.regular_node(node.child_nodes[k], start_string, False)
                    else:
                        string += self.regular_node(node.child_nodes[k], start_string, True)

            else:
                string += "  `- {}\n".format(node.value)
                start_string += "   "
                for k in range(count3):
                    if k != count3 -1:
                        string += self.regular_node(node.child_nodes[k], start_string, False)
                    else:
                        string += self.regular_node(node.child_nodes[k], start_string, True)

        return string


    def print_nodes(self, node):
        string = """"""
        if node.leaf == True:
            string = "`- {}\n".format(node.num_list)
        else:
            string = "`- {}\n".format(node.value)

        count = len(node.child_nodes)
        for i in range(count):
            ## not last node
            if i != count-1:
                if node.child_nodes[i].leaf == True:
                    string += "   |- {}\n".format(node.child_nodes[i].num_list)

                else:
                    #not leaf
                    string += "   |- {}\n".format(node.child_nodes[i].value)
                    start_string = "   |"
                    count2 = len(node.child_nodes[i].child_nodes)
                    for j in range(count2):
                        if j != count2 -1:
                            string += self.regular_node(node.child_nodes[i].child_nodes[j], start_string, False)
                        else:
                            string += self.regular_node(node.child_nodes[i].child_nodes[j], start_string, True)

            ## last node
            else:
                if node.child_nodes[i].leaf == True:
                    string += "   `- {}\n".format(node.child_nodes[i].num_list)

                else:
                    string += "   `- {}\n".format(node.child_nodes[i].value)
                    start_string = "    "
                    count2 = len(node.child_nodes[i].child_nodes)
                    for j in range(count2):
                        if j != count2 -1:
                            string += self.regular_node(node.child_nodes[i].child_nodes[j], start_string, False)
                        else:
                            string += self.regular_node(node.child_nodes[i].child_nodes[j], start_string, True)
        return string

    # insert_keys: integer list
    # delete_keys: integer list (an empty list in the first assignment)
    # return: result string (sequence of tree representations)
    # def show(self, insert_keys, delete_keys):
        # Fill in here

        # First, run all insertions in insert_keys (the value is simply set to be the key)
        # Then, run all deletions in delete_keys
        # For each insertion or deletion, show the operation and tree
        # See this file for the details of the format

    # bogus implementation
    # Replace this bogus implementation with a real one
    def show(self, insert_keys, delete_keys):
        if len(delete_keys) == 0:
            root = self.Node()
            answer_string = """"""
            for key in insert_keys:
                string = """Insert {}\n""".format(key)
                tree = self.insert(root, key)
                string += self.print_nodes(tree)
                answer_string += string
            result = answer_string[:-1]
        
        else:
            root = self.Node()
            answer_string = """"""
            for key in insert_keys:
                string = """Insert {}\n""".format(key)
                tree = self.insert(root, key)
                string += self.print_nodes(tree)
                answer_string += string
            
            for key in delete_keys:
                string = """Delete {}\n""".format(key)
                tree = self.delete(root, key)
                string += self.print_nodes(tree)
                answer_string += string
                
            result = answer_string[:-1]
        return(result)

# IMPORTANT:
# Using a unittest library, your BPTree implementation will be imported,
# and the following code with a different input will be executed.

if __name__ == '__main__':
    bpt = BPTree()
    # For cases with only inserting numbers
    #print(bpt.show([72, 99, 67, 70, 52, 28, 27, 89, 94, 10], []))
    #print(bpt.show([35, 71, 44, 60, 81, 61, 29, 95, 63, 23], []))
    #print(bpt.show([29, 26, 40, 34, 65, 73, 15, 12, 82, 44], []))
    #print(bpt.show([28, 50, 9, 44, 15, 68, 12, 73, 49, 62], []))
    #print(bpt.show([3, 97, 18, 96, 82, 84, 41, 67, 56, 11], []))
    #print(bpt.show([8, 13, 19, 28, 60, 69, 81, 34, 42, 51, 84, 88, 74, 91, 17, 11, 99], []))
    #print(bpt.show([1,2,3,4,5,6,7,8,9,10,11,12,13,14, 15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37], []))
    #print(bpt.show([8, 13, 19, 28, 60, 69, 81, 34, 42, 51, 84, 88, 74, 91, 17, 11, 99,29, 9,10,12,14,15,18,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131], []))

    # For cases with inserting and deleting numbers
    #print(bpt.show([72, 99, 67, 70, 52, 28, 27, 89, 94, 10], [67, 10, 99, 94]))
    #print(bpt.show([35, 71, 44, 60, 81, 61, 29, 95, 63, 23], [71, 61, 95, 63, 81]))
    #print(bpt.show([29, 26, 40, 34, 65, 73, 15, 12, 82, 44], [40, 82, 29, 15]))
    #print(bpt.show([28, 50, 9, 44, 15, 68, 12, 73, 49, 62], [50, 62, 49, 73]))
    #print(bpt.show([3, 97, 18, 96, 82, 84, 41, 67, 56, 11], [18, 67, 96, 82, 97, 41, 56]))
    print(bpt.show([12,14,0,10,5,3,15,1,2,16,18,11,8,9,4,6,7,13,17,19],[5,6,16,10,11,4,19,18,0,17,12,9,7,2,13,3,1,14,15]))
    #print(bpt.show([40, 46,35,30,49,13,10,5,37,11,45,24,32,42,33,22,29,18,28,7,9,2,47,0,14,34,38,4,17,16,20,26,6,19,21,41,1,3,27,31,36,43,23,44,8,39,48,15,12,25],[33,22,17,34,5,21,49,30,32,11,36,4,19,18,0,9,8,15,38,1,10,41,35,40,13,27,28,45,6,39,7,48,43,46,24,26,12,20,42,23,14,47,3,37,29,2,31,16,25]))
    #print(bpt.show([79,29,95,62,68,85,25,60,93,45,73,81,61,43,6,44,57,30,97,17,64,26,72,99,96,15,69,16,90,23,3,87,11,5,13,35,48,51,54,38,63,33,47,37,58,12,56,59,49,94,39,77,24,78,98,22,71,92,41,46,88,8,76,91,4,42,70,32,86,84,80,27,21,20,18,83,82,52,40,74,31,9,36,14,0,50,65,67,1,7,2,10,55,28,19,34,89,53,66,75], [39,74,52,88,38,17,14,73,18,89,0,10,4,97,70,64,49,82,11,37,51,24,8,9,22,83,55,13,92,41,46,69,96,72,66,3,15,12,99,62,50,90,68,32,63,78,28,91,33,34,81,77,45,76,23,58,79,54,42,43,95,53,5,1,85,75,84,2,19,16,86,31,94,40,36,59,30,57,35,47,65,20,21,60,25,87,67,27,71,6,61,80,7,44,26,48,98,93,29]))
    #print(bpt.show([21,26, 35, 95, 12, 10, 27, 30, 28, 29,100,5], [30,35,95]))
    #####