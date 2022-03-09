from REParser import parser
from RENode import RENode


charID = -1
allNodes = {}

def eval_expression(tree):
    global allNodes
    global charID

    if tree[0] == 'char':
        charID = charID+1
        n = RENode(_op='leaf', _sy=tree[1], _pos=charID)
        tree[1] = n
        print(tree)
        allNodes.update({charID: n})
        return tree[1]
    elif tree[0] == 'cat':
        l = eval_expression(tree[1])
        r = eval_expression(tree[2])
        n = RENode(_op='.', _lc=l, _rc=r)
        print(tree)
        return n
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
        global allNodes
        global charID
        charID = -1
        allNodes = {}

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
                print('\nThe value is \n' + str(answer) + '\n')
        except Exception as inst:
            print(inst.args[0])


main()