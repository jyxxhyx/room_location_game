import itertools

import pulp
from pulp import PULP_CBC_CMD, GUROBI_CMD

from model.abstract_model import AbstractModel


class RoomLocation(AbstractModel):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        self.model = pulp.LpProblem("RoomLocation", pulp.LpMaximize)
        return

    def _set_iterables(self):
        self.cap_m = list(range(self.m))
        self.cap_n = list(range(self.n))
        self.cap_k = list(range(self.k))
        self.prod = list(itertools.product(self.cap_m, self.cap_n, self.cap_k))
        return

    def _set_variables(self):
        self.x = pulp.LpVariable.dicts('x',
                                       indices=self.prod,
                                       cat=pulp.LpBinary)
        self.y = pulp.LpVariable.dicts('y', self.prod, cat=pulp.LpBinary)
        self.z = pulp.LpVariable.dicts('z', self.cap_k, cat=pulp.LpBinary)
        return

    def _set_objective(self):
        self.model += pulp.lpSum(self.z[k] for k in self.cap_k)
        return

    def _set_constraints(self):
        for k in self.cap_k:
            self.model += (pulp.lpSum(self.x[i, j, k] for i in self.cap_m
                                      for j in self.cap_n) == 1, f'assign_{k}')
        for (i, j) in itertools.product(self.cap_m, self.cap_n):
            self.model += (pulp.lpSum(self.x[i, j, k]
                                      for k in self.cap_k) <= 1,
                           f'assign_{i}_{j}')
        for (i, j, k) in self.prod:
            self.model += (self.y[i, j, k] <= self.x[i, j, k],
                           f'cell_{i}_{j}_{k}')
            self.model += (self.y[i, j, k] <=
                           pulp.lpSum(self.x[i, j2, k2] for j2 in self.cap_n
                                      for k2 in self.cap_k) - self.x[i, j, k],
                           f'row_{i}_{j}_{k}')
            self.model += (self.y[i, j, k] <=
                           pulp.lpSum(self.x[i2, j, k2] for i2 in self.cap_m
                                      for k2 in self.cap_k) - self.x[i, j, k],
                           f'col_{i}_{j}_{k}')
        for k in self.cap_k:
            self.model += (self.z[k] == pulp.lpSum(self.y[i, j, k]
                                                   for i in self.cap_m
                                                   for j in self.cap_n),
                           f'feasible_{k}')
        return

    def _optimize(self):
        time_limit_in_seconds = 0.1 * 60 * 60
        self.model.writeLP('test.lp')
        # self.model.solve(PULP_CBC_CMD(timeLimit=time_limit_in_seconds))
        self.model.solve(GUROBI_CMD(timeLimit=time_limit_in_seconds))
        return

    def _is_feasible(self):
        return True

    def _process_infeasible_case(self):
        return list(), list()

    def _post_process(self):
        coords = list()
        flags = list()
        for (i, j, k) in self.prod:
            if self.x[i, j, k].value() > 0.9:
                coords.append((i, j))
                if self.y[i, j, k].value() > 0.9:
                    flags.append(True)
                else:
                    flags.append(False)
        return coords, flags
