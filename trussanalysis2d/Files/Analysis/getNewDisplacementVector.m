function [ANALYSIS] = getNewDisplacementVector(DISPLACEMENTS, DOFS, ANALYSIS)

numberDOFS = DOFS.number_dofs;
numberPin = DISPLACEMENTS.number_pin;
pinNodes = DISPLACEMENTS.pin_nodes;
pinDisplacements = DISPLACEMENTS.pin_displacements;
pinAngles = DISPLACEMENTS.pin_angles;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerDirections = DISPLACEMENTS.roller_directions;
rollerDisplacements = DISPLACEMENTS.roller_displacements;


Uc = zeros(numberDOFS, 1);

for numPin = 1 : numberPin
	pNode = pinNodes(numPin);
	pDOFS = [2*pNode-1, 2*pNode];
	pDisplXiYi = pinDisplacements(:, numPin);
	pAngle = pinAngles(numPin);
	C = cos(pAngle * pi / 180);
	S = sin(pAngle * pi / 180);
	T = [C, S; -S, C];
	pDisplXY = T' * pDisplXiYi;
	Uc(pDOFS) = pDisplXY;
end

for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rDirection = rollerDirections(numRol);
	rDisplacement = rollerDisplacements(numRol);
	if (rDirection == 1)
		rDOF = 2 * rNode;
	else
		rDOF = 2 * rNode - 1;
	end
	Uc(rDOF) = rDisplacement;
end


ANALYSIS.displacements_new_vector = Uc;