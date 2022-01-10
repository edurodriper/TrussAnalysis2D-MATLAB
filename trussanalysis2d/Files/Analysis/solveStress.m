function [SOLUTION] = solveStress(MESH, SOLUTION)

U = SOLUTION.global_displacements;
numberElements = MESH.number_elements;
nodeCoordinates = MESH.node_coordinates;
elementConnectivity = MESH.element_connectivity;
materialE = MESH.young_modulus;
materialA = MESH.area;


elementStress = zeros(1, numberElements);
elementForce = zeros(1, numberElements);
ncX = nodeCoordinates(1, :);
ncY = nodeCoordinates(2, :);
for numEle = 1 : numberElements
	% Element nodes
	node1 = elementConnectivity(1, numEle);
	node2 = elementConnectivity(2, numEle);

	% Element dofs
	elementDOFS = [2*node1-1, 2*node1, 2*node2-1, 2*node2];

	% Element material constants
	E = materialE(numEle);
	A = materialA(numEle);
	
	% Element components and length
	dx = ncX(node2) - ncX(node1);
	dy = ncY(node2) - ncY(node1);
	L = (dx^2 + dy^2)^0.5;

	% Sine and cossine of angle between reference frames
	C = dx / L;
	S = dy / L;

	% Element transformation matrix
	T = [C, S, 0, 0; -S, C, 0, 0; 0, 0, C, S; 0, 0, -S, C];
	
	% Local element displacements
	Ul = T * U(elementDOFS);

	% Element stress
	elementStress(numEle) = E * 1 / L * [-1, 0, 1, 0] * Ul;

	% Element force
	elementForce(numEle) = elementStress(numEle) * A;
end


SOLUTION.element_stress = elementStress;
SOLUTION.element_force = elementForce;