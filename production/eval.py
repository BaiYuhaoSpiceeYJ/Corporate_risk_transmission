import os

def get_all_black_list(path):

    if not os.path.exists(path):
        return {}
    linenum = 0
    items = []
    fp = open(path)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = (line.strip().split()[0]).split(r' ')[0]
        items.append(item)
    fp.close()
    return items


def get_all_non_black_list(path):
    if not os.path.exists(path):
            return {}
    items = []
    fp = open(path)
    for line in fp:
        item = (line.strip().split('\'')[1]).split(r' ')[0]
        items.append(item)
    fp.close()
    # print(items)
    return items


def get_all_trade_data(path, non_black_list, black_list):
    if not os.path.exists(path):
        return {}

    graph = {}
    graph_count = {}

    linenum = 0
    pass_count = 0
    fp = open(path)
    for line in fp:
        #print(line)
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split('\t')

        if len(item) < 3:
            continue
        AA, BB, amount = item[0].split(r' ')[0], item[1].split(r' ')[0], item[2]

        #try:
        if AA not in graph and AA not in black_list:
            graph[AA] = 0
        if AA not in graph_count and AA not in black_list:
            graph_count[AA] = 0
        if BB not in graph and BB not in black_list:
            graph[BB] = 0
        if BB not in graph_count and BB not in black_list:
            graph_count[BB] = 0

        if AA in black_list and BB not in black_list:
            graph[BB] += 1
            graph_count[BB] += 1
        elif BB in black_list and AA not in black_list:
            graph[AA] += 1
            graph_count[AA] += 1
        elif AA not in black_list and BB not in black_list:
            graph_count[AA] += 1
            graph_count[BB] += 1
        else:
            pass
        #except Exception as e:
        #    pass_count += 1
        #    print(pass_count)


    fp.close()
    print(len(list(graph.keys())))
    print(len(list(graph_count.keys())))
    return graph, graph_count


black_list = get_all_black_list(r'C:\Users\SpiceeYJ\Desktop\Corporate risk transmission\data\黑名单企业.txt')
print(len(black_list))
#print(black_list)

non_black_list = get_all_non_black_list(r'C:\Users\SpiceeYJ\Desktop\Corporate risk transmission\data\result.txt')
print(len(non_black_list))
#print(non_black_list)

graph, graph_count = get_all_trade_data(r'C:\Users\SpiceeYJ\Desktop\Corporate risk transmission\data\企业交易数据all.txt',
                                        non_black_list, black_list)

total_black_trade = 0
total_trade = 0
i = 0

for etr in graph:
    total_black_trade += int(graph[etr])
    total_trade += int(graph_count[etr])

for item in non_black_list:
    if item in graph and i < 10000:
        print('{} {}/{}'.format(item, graph[item], graph_count[item]), file=open(r'..\data\result_explication.txt', 'a'))
        i += 1
print(total_black_trade, total_trade)
