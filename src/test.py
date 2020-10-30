import numpy as np


def qr_householder(A):
    m, n = A.shape
    Q = np.eye(m)  # Orthogonal transform so far
    R = A.copy()  # Transformed matrix so far

    for j in range(n):
        # Find H = I - beta*u*u' to put zeros below R[j,j]
        x = R[j:, j]
        normx = np.linalg.norm(x)
        rho = -np.sign(x[0])
        u1 = x[0] - rho * normx
        u = x / u1
        u[0] = 1
        beta = -rho * u1 / normx

        R[j:, :] = R[j:, :] - beta * np.outer(u, u).dot(R[j:, :])
        Q[:, j:] = Q[:, j:] - beta * Q[:, j:].dot(np.outer(u, u))

    return Q, R


def new_sol(data):
    m, n = data.shape
    A = np.array([data[:, 0], np.ones(m)]).T
    b = data[:, 1]

    Q, R = qr_householder(A)
    b_hat = Q.T.dot(b)

    R_upper = R[:n, :]
    b_upper = b_hat[:n]

    print(R_upper, b_upper)
    x = np.linalg.solve(R_upper, b_upper)
    slope, intercept = x


def solution():
    times = [10, 11, 12, 13, 14, 15, 16, 17]
    ximes = [1, 1.1, 1.1, 1.3, 1.2, 1.3, 1, 2]
    yimes = [4, 4, 4, 4, 5, 4, 5, 4]
    data_x = []
    data_y = []
    for i in range(len(times)):
        data_x.append([times[i], ximes[i]])
        data_y.append([times[i], yimes[i]])
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    new_sol(data_x)


solution()
