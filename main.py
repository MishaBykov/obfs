import sys
import re


class Node:
    def __init__(self, prev, type_node, body, name):
        self.prev = prev
        self.type = type_node
        self.body = body
        self.name = name


root_tree = [Node(None, 'root', [], 'root'), Node(None, 'root', [], 'root')]
active_node = [root_tree[0], root_tree[1]]


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


def analysis_str(string, ind_root):
    a_n = active_node[ind_root]
    if string[0] == '/' and string[1] == '/':
        a_n.body.append(Node(a_n, 'comment', [], string[:-1]))
        return
    string = re.sub(' *\n *', ' ', string)
    if string[-1] == '}':
        a_n = a_n.prev
    elif string[-1] == '{':
        if 'if' in string:
            a_n.body.append(Node(a_n, 'if', [], string[:-1]))
        elif 'while' in string:
            a_n.body.append(Node(a_n, 'while', [], string[:-1]))
        elif '(' in string and ('=' not in string or string.find('=') > string.find('(')):
            a_n.body.append(Node(a_n, 'function', [], string[:-1]))
        a_n = a_n.body[-1]
    elif string[-1] == ';':
        if 'if' in string:
            a_n.body.append(Node(a_n, 'if', [], string))
        elif 'while' in string:
            a_n.body.append(Node(a_n, 'while', [], string))
        elif len(string.split('=')[0].split('(')[0].strip().split()) > 1 \
                and re.match('[a-zA-Z][a-zA-Z0-9_]*', string.split('=')[0].split('(')[0].strip().split()[-1]) \
                        is not None:
            a_n.body.append(Node(a_n, 'variable', [], string))  # FIX_ME
        else:
            a_n.body.append(Node(a_n, 'other', [], string))
    elif string[-1] == '/' and string[-2] == '*':
        a_n.body.append(Node(a_n, 'comment', [], string[string.find("/*"):]))


def analysis_file(file_path, ind_root):
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
            analysis_str(string_file[id_prev_sep:id_sep + 1], ind_root)
            id_prev_sep = id_sep + 1
        elif id_sep + 1 != len_string_file and string_file[id_sep:id_sep + 2] in separate2:
            if string_file[id_sep:id_sep + 2] == '//':
                i = id_sep
                while string_file[i] != '\n':
                    i += 1
                analysis_str(string_file[id_sep:i + 1], ind_root)
                len_string_file -= len(string_file[id_sep:i + 1])
                string_file = string_file[:id_sep] + string_file[i + 1:]
            else:
                analysis_str(string_file[id_prev_sep:id_sep + 2], ind_root)
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
            rename_node_in_depth(root, variables[0].split()[1], 'v' + str(rename_variables.count_rename))
        except AttributeError:
            rename_variables.count_rename = 0
            rename_node_in_depth(root, variables[0].split()[1], 'v' + str(rename_variables.count_rename))
        rename_variables.count_rename += 1
        for i in range(1, len(variables)):
            rename_node_in_depth(
                root.prev, variables[i].split('=')[0].strip(), 'v' + str(rename_variables.count_rename)) # FIX_ME (type a(1, 2, 3) & type a = 1, b = 2, c = 3))
            rename_variables.count_rename += 1
    for i in root.body:
        rename_variables(i)


def rename_functions(root):
    if root.type == 'function':
        func_name = str(root.name).split('(')[0].split()[-1]
        try:
            rename_node_in_depth(root, func_name, 'f' + str(rename_functions.count_rename))
        except AttributeError:
            rename_functions.count_rename = 0
            rename_node_in_depth(root, func_name, 'f' + str(rename_functions.count_rename))
        rename_functions.count_rename += 1
        rename_args = str(root.name).split('(')[1].split(',')
        for arg in rename_args:
            a = re.split('[^a-zA-Z]', arg)
            arg_name = -1
            while not a[arg_name].isalpha():
                arg_name -= 1
            arg_name = a[arg_name]
            rename_node_in_depth(root, arg_name, 'f' + str(rename_functions.count_rename))
            rename_functions.count_rename += 1
    for i in root.body:
        rename_functions(i)


if __name__ == '__main__':
    analysis_file('quick-sort.cpp', 0)
    analysis_file('merge-sort.cpp', 1)
    del_type(root_tree[0], 'comment')
    rename_functions(root_tree[0])
    rename_variables(root_tree[0])

    del_type(root_tree[1], 'comment')
    rename_functions(root_tree[1])
    rename_variables(root_tree[1])

    file0 = open('out0.cpp', 'w')
    file1 = open('out1.cpp', 'w')
    print_root(root_tree[0], file0)
    print_root(root_tree[1], file1)
    file0.close()
    file1.close()
