import numpy

from pyRMSD.availableCalculators import availableCalculators
from pyRMSD.symmTools import symm_groups_validation, symm_permutations, swap_atoms, min_rmsd_of_rmsds_list


class RMSDCalculator(object):
    """
    Python 3 compatibility implementation of the pyRMSD RMSDCalculator API
    used by pyProCT.
    """

    def __init__(self, calculatorType,
                 fittingCoordsets,
                 calculationCoordsets=None,
                 fitSymmetryGroups=[],
                 calcSymmetryGroups=[]):
        if calculatorType not in availableCalculators():
            print("Calculator ", calculatorType, " is not an available calculator.")
            raise ValueError

        self.fitting_coordinates = numpy.asarray(fittingCoordsets, dtype=numpy.float64)
        self.calculator_type = calculatorType
        self.number_of_conformations = self.fitting_coordinates.shape[0]
        self.number_of_fitting_atoms = self.fitting_coordinates.shape[1]

        if calculationCoordsets is not None:
            self.calculation_coordinates = numpy.asarray(calculationCoordsets, dtype=numpy.float64)
            if self.number_of_conformations != self.calculation_coordinates.shape[0]:
                print("Calculation coordinates must hold the same number of conformations than fitting coordinates.")
                raise ValueError
            self.number_of_calculation_atoms = self.calculation_coordinates.shape[1]
        else:
            self.calculation_coordinates = None
            self.number_of_calculation_atoms = 0

        self.__threads_per_block = 32
        self.__blocks_per_grid = 8
        self.__number_of_threads = 8

        symm_groups_validation(fitSymmetryGroups)
        symm_groups_validation(calcSymmetryGroups)
        self.fit_symmetry_groups = fitSymmetryGroups
        self.calc_symmetry_groups = calcSymmetryGroups

    def pairwise(self, first_conformation_number, second_conformation_number,
                 get_superposed_coordinates=False):
        first_coords = self.fitting_coordinates[first_conformation_number]
        second_coords = self.fitting_coordinates[second_conformation_number]
        tmp_coordsets = numpy.copy(numpy.array([first_coords, second_coords]))

        tmp_calculation_coordsets = None
        if self.calculation_coordinates is not None:
            first_calculation_coords = self.calculation_coordinates[first_conformation_number]
            second_calculation_coords = self.calculation_coordinates[second_conformation_number]
            tmp_calculation_coordsets = numpy.array([first_calculation_coords, second_calculation_coords])

        calculator = RMSDCalculator(self.calculator_type,
                                    tmp_coordsets,
                                    tmp_calculation_coordsets,
                                    self.fit_symmetry_groups,
                                    self.calc_symmetry_groups)
        rmsd = calculator.oneVsFollowing(0)[0]

        if get_superposed_coordinates:
            if tmp_calculation_coordsets is None:
                return rmsd, tmp_coordsets
            return rmsd, tmp_coordsets, tmp_calculation_coordsets
        return rmsd

    def oneVsTheOthers(self, conformation_number, get_superposed_coordinates=False):
        previous_coords = self.fitting_coordinates[:conformation_number]
        following_coords = self.fitting_coordinates[conformation_number + 1:]
        rearranged_coords_list = [numpy.copy(self.fitting_coordinates[conformation_number])]

        for coords in previous_coords:
            rearranged_coords_list.append(numpy.copy(coords))

        for coords in following_coords:
            rearranged_coords_list.append(numpy.copy(coords))

        rearranged_coords = numpy.array(rearranged_coords_list)

        rearranged_calculation_coords = None
        if self.calculation_coordinates is not None:
            previous_coords = self.calculation_coordinates[:conformation_number]
            following_coords = self.calculation_coordinates[conformation_number + 1:]
            rearranged_calculation_coords_list = [self.calculation_coordinates[conformation_number]]

            for coords in previous_coords:
                rearranged_calculation_coords_list.append(coords)

            for coords in following_coords:
                rearranged_calculation_coords_list.append(coords)

            rearranged_calculation_coords = numpy.array(rearranged_calculation_coords_list)

        rmsd_array = RMSDCalculator(self.calculator_type,
                                    rearranged_coords,
                                    rearranged_calculation_coords,
                                    self.fit_symmetry_groups,
                                    self.calc_symmetry_groups).oneVsFollowing(0)

        if get_superposed_coordinates:
            if rearranged_calculation_coords is None:
                return rmsd_array, rearranged_coords
            return rmsd_array, rearranged_coords, rearranged_calculation_coords
        return rmsd_array

    def oneVsFollowing(self, conformation_number):
        if self.fit_symmetry_groups == []:
            return self.__one_vs_following_with_reference(conformation_number,
                                                          self.fitting_coordinates[conformation_number])

        symm_rmsds = []
        for permutation in symm_permutations(self.fit_symmetry_groups):
            coords_copy = numpy.array(self.fitting_coordinates, copy=True, dtype=numpy.float64)
            for symm_group in permutation:
                if symm_group not in self.fit_symmetry_groups:
                    for symm_pair in symm_group:
                        swap_atoms(coords_copy[conformation_number], symm_pair[0], symm_pair[1])
            symm_rmsds.append(self.__one_vs_following_with_reference(conformation_number,
                                                                     coords_copy[conformation_number],
                                                                     coords_copy))
        return min_rmsd_of_rmsds_list(numpy.array(symm_rmsds))

    def pairwiseRMSDMatrix(self):
        rmsds = []
        for i in range(self.number_of_conformations - 1):
            rmsds.extend(self.oneVsFollowing(i))
        return list(rmsds)

    def iterativeSuperposition(self):
        if self.number_of_conformations <= 1:
            return self.fitting_coordinates

        reference = numpy.array(self.fitting_coordinates[0], copy=True, dtype=numpy.float64)
        previous_residual = None
        for _ in range(100):
            residual = 0.0
            for i in range(self.number_of_conformations):
                rotation, reference_center, mobile_center = self.__fit_transform(reference,
                                                                                 self.fitting_coordinates[i])
                self.fitting_coordinates[i] = self.__apply_transform(self.fitting_coordinates[i],
                                                                     rotation,
                                                                     reference_center,
                                                                     mobile_center)
                if self.calculation_coordinates is not None:
                    self.calculation_coordinates[i] = self.__apply_transform(self.calculation_coordinates[i],
                                                                            rotation,
                                                                            reference_center,
                                                                            mobile_center)
                residual += self.__rmsd(reference, self.fitting_coordinates[i])

            reference = self.fitting_coordinates.mean(0)
            if previous_residual is not None and abs(previous_residual - residual) < 1.0e-7:
                break
            previous_residual = residual

        return self.fitting_coordinates

    def setNumberOfOpenMPThreads(self, number_of_threads):
        self.__number_of_threads = number_of_threads

    def setCUDAKernelThreadsPerBlock(self, number_of_threads, number_of_blocks):
        self.__threads_per_block = number_of_threads
        self.__blocks_per_grid = number_of_blocks

    def __one_vs_following_with_reference(self, conformation_number, reference_fit,
                                          fitting_coordinates=None):
        fitting_coordinates = self.fitting_coordinates if fitting_coordinates is None else fitting_coordinates
        rmsds = []
        for other in range(conformation_number + 1, self.number_of_conformations):
            rmsds.append(self.__pairwise_rmsd(reference_fit,
                                             fitting_coordinates[other],
                                             conformation_number,
                                             other))
        return numpy.array(rmsds)

    def __pairwise_rmsd(self, reference_fit, mobile_fit, reference_index, mobile_index):
        reference_calc = self.__calculation_coordset(reference_index)
        mobile_calc = self.__calculation_coordset(mobile_index)

        if self.calculator_type.startswith("NOSUP"):
            return self.__rmsd_with_calculation_symmetry(reference_calc, mobile_calc)

        rotation, reference_center, mobile_center = self.__fit_transform(reference_fit, mobile_fit)
        mobile_calc_superposed = self.__apply_transform(mobile_calc,
                                                       rotation,
                                                       reference_center,
                                                       mobile_center)
        return self.__rmsd_with_calculation_symmetry(reference_calc, mobile_calc_superposed)

    def __calculation_coordset(self, conformation_index):
        if self.calculation_coordinates is None:
            return self.fitting_coordinates[conformation_index]
        return self.calculation_coordinates[conformation_index]

    def __fit_transform(self, reference, mobile):
        reference = numpy.asarray(reference, dtype=numpy.float64)
        mobile = numpy.asarray(mobile, dtype=numpy.float64)

        reference_center = reference.mean(0)
        mobile_center = mobile.mean(0)
        reference_centered = reference - reference_center
        mobile_centered = mobile - mobile_center

        covariance = numpy.dot(mobile_centered.T, reference_centered)
        left, singular_values, right = numpy.linalg.svd(covariance)
        handedness = numpy.sign(numpy.linalg.det(numpy.dot(left, right)))
        correction = numpy.diag([1.0, 1.0, handedness])
        rotation = numpy.dot(numpy.dot(left, correction), right)
        return rotation, reference_center, mobile_center

    def __apply_transform(self, coords, rotation, reference_center, mobile_center):
        return numpy.dot(coords - mobile_center, rotation) + reference_center

    def __rmsd(self, reference, mobile):
        return numpy.sqrt(numpy.sum((reference - mobile) ** 2) / reference.shape[0])

    def __rmsd_with_calculation_symmetry(self, reference_calc, mobile_calc):
        if self.calc_symmetry_groups == []:
            return self.__rmsd(reference_calc, mobile_calc)

        rmsds = []
        for permutation in symm_permutations(self.calc_symmetry_groups):
            mobile_copy = numpy.array(mobile_calc, copy=True, dtype=numpy.float64)
            for symm_group in permutation:
                if symm_group not in self.calc_symmetry_groups:
                    for symm_pair in symm_group:
                        swap_atoms(mobile_copy, symm_pair[0], symm_pair[1])
            rmsds.append(self.__rmsd(reference_calc, mobile_copy))
        return min(rmsds)
