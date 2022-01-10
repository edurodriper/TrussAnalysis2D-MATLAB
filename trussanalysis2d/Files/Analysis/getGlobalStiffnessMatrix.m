function [ANALYSIS] = getGlobalStiffnessMatrix(MESH, ANALYSIS)

numberNodes = MESH.number_nodes;
numberElements = MESH.number_elements;
nodeCoordinates = MESH.node_coordinates;
elementConnectivity = MESH.element_connectivity;
materialE = MESH.young_modulus;
materialA = MESH.area;


ncX = nodeCoordinates(1, :);
ncY = nodeCoordinates(2, :);
K = zeros(2*numberNodes, 2*numberNodes);

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

	% Global element stiffness matrix
	Ke = E * A / L * ...
		[C*C, C*S, -C*C, -C*S; ...
		C*S, S*S, -C*S, -S*S; ...
		-C*C, -C*S, C*C, C*S; ...
		-C*S, -S*S, C*S, S*S];

	% Assembly
	K(elementDOFS, elementDOFS) = K(elementDOFS, elementDOFS) + Ke;
end


ANALYSIS.stiffness_global_matrix = K;