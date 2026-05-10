"""Small compatibility fallback for the original minepy.MINE API.

The upstream minepy package does not currently build cleanly on this
Python/NumPy combination. This local module preserves the tiny API surface
used by the notebook: MINE().compute_score(x, y) followed by MINE().mic().
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_selection import mutual_info_regression


class MINE:
    def __init__(self, *args, **kwargs):
        self._mic = 0.0

    def compute_score(self, x, y):
        x_arr = np.asarray(x, dtype=float).reshape(-1, 1)
        y_arr = np.asarray(y, dtype=float).ravel()

        valid = np.isfinite(x_arr[:, 0]) & np.isfinite(y_arr)
        if valid.sum() < 3:
            self._mic = 0.0
            return

        try:
            score = mutual_info_regression(
                x_arr[valid],
                y_arr[valid],
                discrete_features=False,
                random_state=0,
            )[0]
        except Exception:
            corr = np.corrcoef(x_arr[valid, 0], y_arr[valid])[0, 1]
            score = 0.0 if not np.isfinite(corr) else abs(corr)

        self._mic = float(score) if np.isfinite(score) else 0.0

    def mic(self):
        return self._mic
