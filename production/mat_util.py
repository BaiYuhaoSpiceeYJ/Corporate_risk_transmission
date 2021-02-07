from scipy.sparse import coo_matrix
import numpy as np
import read

# 将图转为矩阵，输出稀疏矩阵M
# coo_matrix数据结构：
# row = [0,1,3]
# col = [2,2,1]
# data = [5,1,7]
# 即mat[0,2] = 5,mat[1,2] = 1,mat[3,1] = 7，其余均为0

def graph_to_m(graph, graph_count):
    vertex = list(graph.keys())
    address_dict = {}
    total_len = len(vertex)

    for index in range(len(vertex)):
        address_dict[vertex[index]] = index
    row = []
    col = []
    data = []
    for element_i in graph:
        # weight = 1/len(graph[element_i]) # 矩阵的数值是顶点i出度的倒数
        row_index = address_dict[element_i]  # i的行索引
        for element_j in graph[element_i]:  # i的列索引
            weight = graph[element_i][element_j] / graph_count[element_i]
            col_index = address_dict[element_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    m = coo_matrix((data, (row, col)), shape=(total_len, total_len))
    return m, vertex, address_dict

# 计算I-alpha*(M.T)
def mat_all_point(m_mat, vertex, alpha):
    """
    get E-alpha*m_mat.T
    Args:
        m_mat:
        vertex: total item and user point
        alpha: the prob for random walking
    Return:
        a sparse
    """
    total_len = len(vertex)
    row = []
    col = []
    data = []
    for index in range(total_len):
        row.append(index)
        col.append(index)
        data.append(1)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data, (row, col)), shape=(total_len, total_len))  # 用coo的方式初始化单位矩阵，用np.eye会超内存
    return eye_t.tocsr() - alpha*m_mat.tocsr().transpose()  # 用tocsr格式计算，更加快速

