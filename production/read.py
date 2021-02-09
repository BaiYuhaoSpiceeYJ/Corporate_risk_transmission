import os

def get_graph_from_data(input_file):
    """
    Args:
        input_file:trade file
    Return:
        a dict: {BlackA:{WhiteA:1, WhiteC:3}, WhiteB:{BlackA:1}}
    """
    if not os.path.exists(input_file):
        return {}
    graph = {}
    graph_count = {}
    linenum = 0

    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("\t")

        if len(item) < 3:
            continue
        AA, BB, amount = item[0].split(' ')[0], item[1].split(' ')[0], item[2]

        if AA not in graph:
            graph[AA] = {}
        if AA not in graph_count:
            graph_count[AA] = 0
        if BB not in graph[AA]:
            graph[AA][BB] = 0

        graph[AA][BB] += 1  # abs(float(amount))
        graph_count[AA] += 1  # abs(float(amount))

        if BB not in graph:
            graph[BB] = {}
        if BB not in graph_count:
            graph_count[BB] = 0
        if AA not in graph[BB]:
            graph[BB][AA] = 0

        graph[BB][AA] += 1  # abs(float(amount))
        graph_count[BB] += 1  # abs(float(amount))
    fp.close()
    # print(len(list(graph.keys())))
    return graph, graph_count

def get_black_from_data(input_file):

    if not os.path.exists(input_file):
        return {}
    linenum = 0
    items = []
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = (line.strip().split()[0]).split(r' ')[0]
        items.append(item)
    fp.close()
    return items

