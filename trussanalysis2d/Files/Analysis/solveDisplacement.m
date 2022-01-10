function [SOLUTION] = solveDisplacement(ANALYSIS, DOFS, SOLUTION)

fixedDOFS = DOFS.fixed_dofs;
freeDOFS = DOFS.free_dofs;
F = ANALYSIS.force_global_vector;
Uc = ANALYSIS.displacements_new_vector;
Tc = ANALYSIS.transformation_new_matrix;
K = ANALYSIS.stiffness_global_matrix;

% New force vector
Fc = Tc * F;
% New stiffness matrix
Kc = Tc * K * Tc';

% Free new displacements
Uc(freeDOFS) = Kc(freeDOFS, freeDOFS) \ ...
	(Fc(freeDOFS) - Kc(freeDOFS, fixedDOFS) * Uc(fixedDOFS));

% Fixed new forces
Fc(fixedDOFS) = Kc(fixedDOFS, freeDOFS) * Uc(freeDOFS) + ...
	Kc(fixedDOFS, fixedDOFS) * Uc(fixedDOFS) - Fc(fixedDOFS);

% Global displacement and force vectors
U = Tc' * Uc;
F = Tc' * Fc;


SOLUTION.new_displacements = Uc;
SOLUTION.new_forces = Fc;
SOLUTION.global_displacements = U;
SOLUTION.global_forces = F;