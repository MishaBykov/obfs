import sys
import re


class Node:
    def __init__(self, prev, type_node, body, name):
        self.prev = prev
        self.type = type_node
        self.body = body
        self.name = name


root_tree = Node(None, 'root', [], 'root')
active_node = root_tree


def print_root(root, out_file=sys.stdout):
    if len(root.body) > 1:
        print('{', file=out_file)
        for i in root.body:
            print(i.name, file=out_file)
            print_root(i, out_file)
        print('}', file=out_file)
    else:
        for i in root.body:
            print(i.name, file=out_file)
            print_root(i, out_file)
            print(';', file=out_file)


def del_type(root, node_type):
    i = 0
    len_body = len(root.body)
    while i < len_body:
        if root.body[i].type == node_type:
            del root.body[i]
            len_body -= 1
            i -= 1
        else:
            del_type(root.body[i], node_type)
        i += 1


def analysis_str(string=''):
    global active_node
    if string[0] == '/' and string[1] == '/':
        active_node.body.append(Node(active_node, 'comment', [], string[:-1]))
        return
    string = re.sub(' *\n *', ' ', string)
    if string[-1] == '}':
        active_node = active_node.prev
    elif string[-1] == '{':
        if 'if' in string:
            active_node.body.append(Node(active_node, 'if', [], string[:-1]))
        elif 'while' in string:
            active_node.body.append(Node(active_node, 'while', [], string[:-1]))
        elif '=' not in string or string.find('=') > string.find('('):
            active_node.body.append(Node(active_node, 'function', [], string[:-1]))
        active_node = active_node.body[-1]
    elif string[-1] == ';':
        if 'if' in string:
            active_node.body.append(Node(active_node, 'if', [], string))
        elif 'while' in string:
            active_node.body.append(Node(active_node, 'while', [], string))
        elif len(string.split('=')[0].strip().split()) == 2:
            active_node.body.append(Node(active_node, 'variable', [], string))
        else:
            active_node.body.append(Node(active_node, 'other', [], string))
    elif string[-1] == '/' and string[-2] == '*':
        active_node.body.append(Node(active_node, 'comment', [], string[string.find("/*"):]))


def analysis_file(file_path):
    # init
    separate1 = [';', '{', '}']
    separate2 = ['//', '*/']

    id_prev_sep = 0
    id_sep = 0

    file = open(file_path)
    string_file = file.readlines()
    file.close()
    string_file = re.sub(r" +", ' ', " ".join(string_file))
    string_file = re.sub(r" *;", ';', string_file)
    len_string_file = len(string_file)
    # ---------
    while True:
        if string_file[id_sep] in separate1:
            analysis_str(string_file[id_prev_sep:id_sep + 1])
            id_prev_sep = id_sep + 1
        elif id_sep + 1 != len_string_file and string_file[id_sep:id_sep + 2] in separate2:
            if string_file[id_sep:id_sep + 2] == '//':
                i = id_sep
                while string_file[i] != '\n':
                    i += 1
                analysis_str(string_file[id_sep:i + 1])
                len_string_file -= len(string_file[id_sep:i + 1])
                string_file = string_file[:id_sep] + string_file[i + 1:]
            else:
                analysis_str(string_file[id_prev_sep:id_sep + 2])
                id_sep += 1
            id_prev_sep = id_sep + 1
        id_sep += 1
        if id_sep >= len_string_file:
            break


def rename_node_in_depth(root, old_name, new_name):
    for i in range(len(root.body)):
        root.body[i].name = re.sub('(^|[^A-Za-z])(' + old_name + ')([^A-Za-z])', r'\1' + new_name + r'\3',
                                   root.body[i].name)
        rename_node_in_depth(root.body[i], old_name, new_name)


def rename_variables(root):
    if root.type == 'variable':
        variables = str(root.name).replace(';', '').split(',')
        try:
            rename_node_in_depth(root.prev, variables[0].split()[1], 'v' + str(rename_variables.count_rename))
        except AttributeError:
            rename_variables.count_rename = 0
            rename_node_in_depth(root.prev, variables[0].split()[1], 'v' + str(rename_variables.count_rename))
        rename_variables.count_rename += 1
        for i in range(1, len(variables)):
            rename_node_in_depth(
                root.prev, variables[i].split('=')[0].strip(), 'v' + str(rename_variables.count_rename))
            rename_variables.count_rename += 1
    for i in root.body:
        rename_variables(i)


if __name__ == '__main__':
    analysis_file('quick-sort.cpp')
    del_type(root_tree, 'comment')
    rename_variables(root_tree)
    file = open('out.cpp', 'w')
    print_root(root_tree, file)
    file.close()