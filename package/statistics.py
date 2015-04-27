__author__ = 'luigolas'

import numpy as np
from scipy.stats import cumfreq


class Statistics():
    """
    Position List: for each element in probe, find its same ids in gallery. Format: np.array([[2,14],[1,2],...])
    Mean List: Calculate means of position list by axis 0. Format: np.array([1.52, 4.89])
    Mode_list: TODO******* calculate statistical mode along axis 0. Format: (np.array([[2., 4.]]), np.array([[10, 12]]))
    Prob admissible range: For each row in Position List calculates if it is lower than a value. Then sum and calculates
                           percentage
    """
    def __init__(self):
        self.matching_order = None
        self.CMC = None
        self.mean_value = None

        self._name = None

    # def name(self):
    #     if self._name is not None:
    #         return self._name
    #     else:
    #         return self._exec.name()
    #
    # def dict_name(self):
    #     name = self._exec.dict_name()
    #
    #     if self.mean_value is None:
    #         name.update({"MeanList1": np.NaN, "MeanList2": np.NaN})
    #     else:
    #         name.update({"MeanList1": self.mean_value[0]})
    #         if len(self.mean_value) > 1:
    #             name.update({"MeanList2": self.mean_value[1]})
    #
    #     if self.rangeX is not None:
    #         for rangenum, range in zip(self._rangeX_set, self.rangeX):
    #             for index, range_elem in enumerate(range):
    #                 name.update({"Range-%d-%d" % (rangenum, index): range_elem})
    #     else:
    #         pass
    #         # name.update({"ProbAdmissible1": np.NaN, "ProbAdmissible2": np.NaN})
    #
    #     return name

    def run(self, dataset, ranking_matrix):
        # Filter ranking matrix to tests values of dataset
        if ranking_matrix.shape[0] != len(dataset.test_indexes):
            ranking_matrix = self._ranking_matrix_reshape(ranking_matrix, dataset.test_indexes)
        else:
            ranking_matrix = ranking_matrix

        self._calc_matching_order(ranking_matrix)
        self._calc_mean_value()
        self._calcCMC(dataset.test_size)

    def _calc_matching_order(self, ranking_matrix):
        matching_order = []

        for elemp, rank_list in enumerate(ranking_matrix):
            # probe_elem = dataset.test_indexes[elemp]
            for column, elemg in enumerate(rank_list):
                # if dataset.same_individual_by_pos(elemp, np.where(dataset.test_indexes == elemg)[0][0],
                #                                   set="test"):
                if elemp == elemg:
                    matching_order.append(column + 1)  # CMC count from position 1
                    break
        self.matching_order = np.asarray(matching_order, np.uint16)

    def _calc_mean_value(self):
        self.mean_value = np.mean(self.matching_order)
        # self.mean_value = np.mean(self.matching_order, 1)  # For multiview case

    def _calcCMC(self, size):
        cumfreqs = (cumfreq(self.matching_order, numbins=size)[0] / size) * 100.
        self.CMC = cumfreqs.astype(np.float32)
        # len(self.matching_order[self.matching_order <= admissible]) / float(self.dataset.test_size)

    # def plot_position_list(self, fig_name, zoom=None, show=False):
    #     bins_rank, num_positions = self.position_list.shape
    #     colors = itertools.cycle(["blue", "red", "green", "yellow", "orange"])
    #     for i in range(num_positions):
    #         plt.hist(self.position_list[:, i], bins=bins_rank, label='Pos ' + str(i), histtype='stepfilled', alpha=.8,
    #                  color=next(colors), cumulative=True, normed=True)
    #     plt.yticks(np.arange(0, 1.01, 0.05))
    #     plt.grid(True)
    #     plt.title("Ranking Histogram")
    #     plt.xlabel("Value")
    #     plt.ylabel("Frequency")
    #     # Put a legend below current axis
    #     plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    #     # Zoomed figure
    #     if zoom:
    #         plt.axis([0, zoom, 0, 1])
    #         plt.xticks(range(0, zoom+1, 2))
    #     plt.savefig(fig_name, bbox_inches='tight')
    #     if show:
    #         plt.show()
    #     # Clean and close figure
    #     plt.clf()
    #     plt.close()

    @staticmethod
    def _ranking_matrix_reshape(ranking_matrix, test_indexes):
        ranking_matrix = ranking_matrix[test_indexes]
        length = ranking_matrix.shape[0]
        elems = np.in1d(ranking_matrix, test_indexes).reshape(ranking_matrix.shape)
        ranking_matrix = ranking_matrix[elems]
        ranking_matrix =  ranking_matrix.reshape(length, length)
        rm = np.empty_like(ranking_matrix)
        for pos, val in enumerate(test_indexes):
            rm[ranking_matrix == val] = pos
        return rm