function [ANALYSIS] = getGlobalForceVector(FORCES, DOFS, ANALYSIS)

numberForces = FORCES.number_forces;
forceNodes = FORCES.force_nodes;
forceComponents = FORCES.force_components;
forceAngles = FORCES.force_angles;
numberDOFS = DOFS.number_dofs;


F = zeros(numberDOFS, 1);

for numFor = 1 : numberForces
	fNode = forceNodes(numFor);
	fNodeDOFS = [2*fNode-1, 2*fNode];
	fCompXiYi = forceComponents(:, numFor);
	fAngle = forceAngles(numFor);
	C = cos(fAngle * pi / 180);
	S = sin(fAngle * pi / 180);
	T = [C, S; -S, C];
	fCompXY = T' * fCompXiYi;
	F(fNodeDOFS) = F(fNodeDOFS) + fCompXY;
end


ANALYSIS.force_global_vector = F;
