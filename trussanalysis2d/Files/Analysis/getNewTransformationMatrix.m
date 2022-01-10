function [ANALYSIS] = getNewTransformationMatrix(DISPLACEMENTS, DOFS, ANALYSIS)

numberDOFS = DOFS.number_dofs;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerAngles = DISPLACEMENTS.roller_angles;


Tc = eye(numberDOFS);

for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rDOFS = [2*rNode-1, 2*rNode];
	rAngle = rollerAngles(numRol);
	C = cos(rAngle * pi / 180);
	S = sin(rAngle * pi / 180);
	T = [C, S; -S, C];
	Tc(rDOFS, rDOFS) = T;
end


ANALYSIS.transformation_new_matrix = Tc;