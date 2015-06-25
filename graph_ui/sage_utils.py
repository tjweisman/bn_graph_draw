def graph_jacobian(laplacian_matrix):
    """compute the jacobian group (in elementary divisor form) from a
    laplacian matrix"""
    Q = matrix(laplacian_matrix)
    return filter(lambda x: x != 0 and x != 1, Q.elementary_divisors())
