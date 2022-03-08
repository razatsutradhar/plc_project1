from REParser import parser
charID = -1


class Node:
    def __init__(self, id, c, first_pos, last_pos, follow_pos, nullable=False):
        self.id = id
        self.c = c
        self.first_pos = first_pos
        self.last_pos = last_pos
        self.follow_pos = follow_pos
        self.nullable = nullable

    def __repr__(self):
        return '[id: ' + str(self.id) + ', char: ' + str(self.c) + ', first: ' + str(self.first_pos) + ', last: ' + str(self.last_pos) + ', follow: ' + str(self.follow_pos) + ', nullable: ' + str(self.nullable) + ' ]'



def eval_expression(tree):
    if tree[0] == 'char':
        global charID
        charID = charID+1
        n = Node(id=charID, c=tree[1], first_pos=[tree[1]], last_pos=[tree[1]], follow_pos=[], nullable=False)
        tree[1] = n
        print(tree)
        return tree[1]
    elif tree[0] == 'cat':
        print(tree)
        eval_expression(tree[1])
        eval_expression(tree[2])
    elif tree[0] == 'union':
        print(tree)
        eval_expression(tree[1])
        eval_expression(tree[2])
    elif tree[0] == 'kleene':
        print(tree)
        eval_expression(tree[1])



def read_input():
    result = ''
    while True:
        data = input('RE: ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0:i + 1]
            break
        else:
            result += data + ' '
    return result


def main():
    while True:
        data = read_input()
        if data == 'exit;':
            break
        try:
            tree = parser.parse(data)
        except Exception as inst:
            print(inst.args[0])
            continue
        try:
            answer = eval_expression(tree)
            if isinstance(answer, str):
                print('\nEVALUATION ERROR: ' + answer + '\n')
            else:
                print('\nThe value is ' + str(answer) + '\n')
        except Exception as inst:
            print(inst.args[0])


main()