function [SOLUTION] = solveReaction(SOLUTION, DISPLACEMENTS)

Fc = SOLUTION.new_forces;
numberPin = DISPLACEMENTS.number_pin;
pinNodes = DISPLACEMENTS.pin_nodes;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerDirections = DISPLACEMENTS.roller_directions;
rollerAngles = DISPLACEMENTS.roller_angles;
numberSupport = DISPLACEMENTS.number_support;


R = zeros(2, numberSupport);
sNode = 1;

% Pin support 
for numPin = 1 : numberPin
	pNode = pinNodes(numPin);
	fixedDOFS = [2*pNode-1, 2*pNode];
	R(:, sNode) = Fc(fixedDOFS);
	sNode = sNode + 1;
end

% Roller support
for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rDirection = rollerDirections(numRol);
	rAngle = rollerAngles(numRol);
	Rc = zeros(2, 1);
	if (rDirection == 1)
		% fixes the y direction
		% assumes that the roller can roll in th x direction
		fixedDOF = 2 * rNode;
		Rc(2) = Fc(fixedDOF);
		
	else
		fixedDOF = 2 * rNode - 1;
		Rc(1) = Fc(fixedDOF);
	end
	C = cos(rAngle * pi / 180);
	S = sin(rAngle * pi / 180);
	T = [C, S; -S, C];
	R(:, sNode) = T' * Rc;
	sNode = sNode + 1; 
end


SOLUTION.global_reactions = R;

