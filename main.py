import sys
import re
import copy


class Node:
    def __init__(self, prev, type_node, body, name):
        self.prev = prev
        self.type = type_node
        self.body = body
        self.name = name


root_tree = [Node(None, 'root', [], 'root'), Node(None, 'root', [], 'root')]
active_node = [root_tree[0], root_tree[1]]
opaque_predicates = [
    "(x + x & 1) == 0",
    "(x + -x & 1) == 0",
    "~x != x * 4u >> 2",
    "(-x & 1) == (x & 1)",
    "((-x ^ x) & 1) == 0",
    "(x * 0x80 & 0x56) == 0",
    "(x << 1 ^ 0x1765) != 0",
    "~(-x * 0x40) != x << 6",
    "(~(x * 0x80) & 0x3d) == 0x3d",
    "x - 0x9d227fa9 != x - 0x699c945e",
    "(y ^ y - 0x35f5f4d2) != 0x42a26409",
    "(x * 0x20000000 & 0x19a27923) == 0",
    "(int)(y * 9u + y * 0xf7u >> 3) >= 0",
    "(x * 4 & 8) == (x + x * 3 - 0x1fef9d8f & 8)",
    "(x | 0xffffdbe8) - 0x1baa != x || (x & 0x10) == 0x10",
    "(x ^ 0x1145f) != 0 || (x | 0xfffeffff) == 0xffffffff",
    "(uint)x / 0x59d7e3 != 0x90298cf9 || (x * 3 + x & 3) == 0",
    "((uint)x % 0x38 + 0xe4df62c8 & 0x6d755e00) == 0x64554200",
    "(x ^ 0x770363c6) != 0 || ((uint)x >> 0x19 ^ 0x926797eb) != 0",
    "(uint)y / 0x2369af8 - 0x78400000 != (uint)x / 0x1f2ce * 0x10",
    "(x & 0x8e3ef800) != 0x70641deb && (uint)x / 0x9388ea != 0x3ab69",
]


def get_opaque_predicates():
    try:
        get_opaque_predicates.count_get += 1
    except AttributeError:
        get_opaque_predicates.count_get = 0
    if get_opaque_predicates.count_get == len(opaque_predicates):
        get_opaque_predicates.count_get = 0
    return opaque_predicates[get_opaque_predicates.count_get]


def print_root(root, out_file=sys.stdout):
    for i in root.body:
        print(i.name, file=out_file)
        print_tree(i, out_file)


def print_tree(root, out_file=sys.stdout):
    if len(root.body) > 1:
        print('{', file=out_file)
        for i in root.body:
            print(i.name, file=out_file)
            print_tree(i, out_file)
        print('}', file=out_file)
    else:
        for i in root.body:
            print(i.name, file=out_file)
            print_tree(i, out_file)
            # print(';', file=out_file)


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
    if string[0] == '/' and string[1] == '/':
        active_node[ind_root].body.append(Node(active_node[ind_root], 'comment', [], string[:-1]))
        return
    string = re.sub(' *\n *', ' ', string)
    if string[-1] == '}':
        active_node[ind_root] = active_node[ind_root].prev
    elif string[-1] == '{':
        if 'if' in string:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'if', [], string[:-1]))
        elif 'while' in string:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'while', [], string[:-1]))
        elif '(' in string and ('=' not in string or string.find('=') > string.find('(')):
            active_node[ind_root].body.append(Node(active_node[ind_root], 'function', [], string[:-1]))
        active_node[ind_root] = active_node[ind_root].body[-1]
    elif string[-1] == ';':
        if 'if' in string:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'if', [], string))
        elif 'while' in string:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'while', [], string))
        elif len(string.split('=')[0].split('(')[0].strip().split()) > 1 and \
                        re.match('[a-zA-Z_][a-zA-Z0-9_]*', string.split('=')[0].split('(')[0].strip().split()[-1]) \
                        is not None:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'variable', [], string))
        else:
            active_node[ind_root].body.append(Node(active_node[ind_root], 'other', [], string))
    elif string[-1] == '/' and string[-2] == '*':
        active_node[ind_root].body.append(Node(active_node[ind_root], 'comment', [], string[string.find("/*"):]))


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
    print(old_name, new_name)
    for i in range(len(root.body)):
        root.body[i].name = re.sub('(^|[^A-Za-z_])(' + old_name + ')([^A-Za-z0-9_])', r'\1' + new_name + r'\3',
                                   root.body[i].name)
        rename_node_in_depth(root.body[i], old_name, new_name)


def rename_variables(root):
    if root.type == 'variable':
        string = ''
        if '(' in root.name:
            string = root.name[:root.name.find('(')] + root.name[str(root.name).rfind(')') + 1:]
        else:
            string = root.name
        variables = string.replace(';', '').split(',')
        arg0 = re.split('[^a-zA-Z0-9_]', variables[0])
        arg_ind = -1
        while not re.match('[a-zA-Z_][a-zA-Z0-9_]*', arg0[arg_ind]):
            arg_ind -= 1
        arg0 = arg0[arg_ind]
        try:
            rename_node_in_depth(root.prev, arg0, 'v' + str(rename_variables.count_rename))
        except AttributeError:
            rename_variables.count_rename = 0
            rename_node_in_depth(root.prev, arg0, 'v' + str(rename_variables.count_rename))
        rename_variables.count_rename += 1
        for i in range(1, len(variables)):
            arg = re.split('[^a-zA-Z0-9_]', variables[i].split('=')[0])
            arg_ind = -1
            while not re.match('[a-zA-Z_][a-zA-Z0-9_]*', arg[arg_ind]):
                arg_ind -= 1
            arg = arg[arg_ind]
            rename_node_in_depth(
                root.prev, arg, 'v' + str(rename_variables.count_rename))
            rename_variables.count_rename += 1
    for i in root.body:
        rename_variables(i)


def rename_functions(root):
    if root.type == 'function':
        func_name = str(root.name).split('(')[0].split()[-1]
        if func_name == 'main':
            return
        try:
            rename_node_in_depth(root.prev, func_name, 'f' + str(rename_functions.count_rename))
        except AttributeError:
            rename_functions.count_rename = 0
            rename_node_in_depth(root.prev, func_name, 'f' + str(rename_functions.count_rename))
        rename_functions.count_rename += 1
        rename_args = str(root.name).split('(')[1].split(')')[0].split(',')
        for arg in rename_args:
            arg = re.split('[^a-zA-Z0-9_]', arg)
            arg_ind = -1
            while not re.match('[a-zA-Z_][a-zA-Z0-9_]*', arg[arg_ind]):
                arg_ind -= 1
            arg_name = arg[arg_ind]
            root.name = re.sub('(^|[^A-Za-z])(' + arg_name + ')([^A-Za-z])', r'\1' + 'f' +
                               str(rename_functions.count_rename) + r'\3', root.name)
            rename_node_in_depth(root, arg_name, 'f' + str(rename_functions.count_rename))
            rename_functions.count_rename += 1
    for i in root.body:
        rename_functions(i)


def add_nodes(src_root, dst_root):
    for i in src_root.body:
        if ' main(' not in i.name:
            for j in range(len(dst_root.body)):
                args = str(i.name).split('(')[1].split(')')[0].split(',')
                for arg in args:
                    dst_root.body[j].body.insert(0, Node(dst_root, 'variable', [], arg+';'))
                func_name = str(i.name).split(maxsplit=1)[1]
                dst_root.body[j].body.append(Node(dst_root, 'if',
                                             [Node(dst_root, 'other', [], func_name)],
                                             'if (' + get_opaque_predicates() + ') '))

            dst_root.body.insert(0, i)


if __name__ == '__main__':
    analysis_file('quick-sort.cpp', 0)
    analysis_file('merge-sort.cpp', 1)

    del_type(root_tree[0], 'comment')
    del_type(root_tree[1], 'comment')

    # new_root = copy.deepcopy(root_tree[1])
    # add_nodes(root_tree[0], root_tree[1])
    # add_nodes(new_root, root_tree[0])

    rename_variables(root_tree[0])
    rename_variables(root_tree[1])

    rename_functions(root_tree[0])
    rename_functions(root_tree[1])

    file0 = open('out0.cpp', 'w')
    file1 = open('out1.cpp', 'w')
    print_root(root_tree[0], file0)
    print_root(root_tree[1], file1)
    file0.close()
    file1.close()
