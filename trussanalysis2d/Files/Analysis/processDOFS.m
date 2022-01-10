function [DOFS] = processDOFS(MESH, DISPLACEMENTS, DOFS)

numberNodes = MESH.number_nodes;
numberPin = DISPLACEMENTS.number_pin;
pinNodes = DISPLACEMENTS.pin_nodes;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerDirections = DISPLACEMENTS.roller_directions;


numberDOFS = 2 * numberNodes;

numberFixedDOFS = 2 * numberPin + numberRoller;
numberFreeDOFS = numberDOFS - numberFixedDOFS;
fixedDOFS = zeros(1, numberFixedDOFS);

fDOF = 1;
for numPin = 1 : numberPin
	pNode = pinNodes(numPin);
	fixedDOFS([fDOF, fDOF+1]) = [2*pNode-1, 2*pNode];
	fDOF = fDOF + 2;
end

for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rDirection = rollerDirections(numRol);
	if (rDirection == 1)
		fixedDOFS(fDOF) = 2 * rNode;
		fDOF = fDOF + 1;
	else
		fixedDOFS(fDOF) = 2 * rNode - 1;
		fDOF = fDOF + 1;
	end
end

freeDOFS = 1 : numberDOFS;
freeDOFS(fixedDOFS) = [];


DOFS.number_dofs = numberDOFS;
DOFS.number_fixed = numberFixedDOFS;
DOFS.number_free = numberFreeDOFS;
DOFS.fixed_dofs = fixedDOFS;
DOFS.free_dofs = freeDOFS;