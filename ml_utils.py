from math import comb
from typing import Iterable


def estim_ensemble_misclass_proba(e: float, n_estim: int):
	total_err = 0
	i = n_estim // 2 + 1

	while i <= n_estim:
		total_err += comb(n_estim, i) * (e ** i) * ((1 - e) ** (n_estim - i))
		i += 1

	return total_err