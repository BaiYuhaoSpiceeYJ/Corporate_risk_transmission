import read
import operator
import mat_util
from scipy.sparse.linalg import gmres
import numpy as np

# 二分图，固定定点，alpha概率，给固定定点推荐的数目
# 输出词典，key为item，value是pr值，长度是推荐数目
def personal_rank_mat(graph, graph_count, root, alpha, recom_num=10):
    """
    Args:
        graph:user item graph
        root:the fix user to recom
        alpha:the prob to random walk
        recom_num:recom item num
    Return:
        a dict, key: itemid, value: pr score
    A*r = r0
    """
    m, vertex, address_dict = mat_util.graph_to_m(graph, graph_count)
    if root not in address_dict:
        return {}
    score_dict = {}
    recom_dict = {}
    mat_all = mat_util.mat_all_point(m, vertex, alpha)  # A矩阵
    index = address_dict[root]
    initial_list = [[0] for row in range(len(vertex))]  # r0矩阵，为一个列向量，除了根节点为1，其余均为0
    initial_list[index] = [1]
    r_zero = np.array(initial_list)
    res = gmres(mat_all, r_zero, tol=1e-8)[0]  # tol为误差，gmres用来解Ax=b，即Ar=r0

    for index in range(len(res)):
        point = vertex[index]
        # if point in graph[root]:  # 过滤掉根结点user行为过的item
        #    continue
        score_dict[point] = res[index]
    for zuhe in sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:recom_num]:
        point, score = zuhe[0], zuhe[1]
        recom_dict[point] = score

    return recom_dict


def get_one_user_by_mat(user):
    alpha = 0.8
    graph, graph_count = read.get_graph_from_data(r"..\data\企业交易数据all.txt")
    recom_result = personal_rank_mat(graph, graph_count, user, alpha, 10000)
    # print(recom_result)
    # print(len(list(recom_result)))
    # print(recom_result)
    return recom_result


def get_all_user_by_mat():
    all_black_data = read.get_black_from_data(r"..\data\黑名单企业.txt")
    all_result = {}
    i = 1
    for data in all_black_data:
        print('{} {}/{}'.format(data, i, len(all_black_data)))
        i += 1

        result = get_one_user_by_mat(data)
        for element in result:
            if element not in all_black_data:
                if element not in all_result:
                    all_result[element] = 0
                all_result[element] += result[element]
    # print(len(list(all_result)))
    all_result = sorted(all_result.items(), key=operator.itemgetter(1), reverse=True)
    # print(len(list(all_result)))
    for i in range(len(list(all_result))):
        print(all_result[i], file=open(r'..\data\result.txt', 'a'))


if __name__ == "__main__":
    # recom_result_mat = get_one_user_by_mat(user="诺亚正行基金销售有限公司基金代销专户")
    get_all_user_by_mat()



