function [MESH] = processMesh(FILEDATA, MESH)

fileData = FILEDATA.mesh;

% Process mesh file

fileLine = 1;

numberNodes = fileData(fileLine, 1);
fileLine = fileLine + 1;
nodeCoordinates = zeros(2, numberNodes);
for numNod = 1 : numberNodes
	nodeCoordinates(1, numNod) = fileData(fileLine, 1);
	nodeCoordinates(2, numNod) = fileData(fileLine, 2);
	fileLine = fileLine + 1;
end

numberElements = fileData(fileLine, 1);
fileLine = fileLine + 1;
elementConnectivity = zeros(2, numberElements);
elementMaterial = zeros(1, numberElements);
for numEle = 1 : numberElements
	elementConnectivity(1, numEle) = fileData(fileLine, 1);
	elementConnectivity(2, numEle) = fileData(fileLine, 2);
	elementMaterial(numEle) = fileData(fileLine, 3);
	fileLine = fileLine + 1;
end

numberMaterials = fileData(fileLine, 1);
fileLine = fileLine + 1;
materialE = zeros(1, numberMaterials);
materialA = zeros(1, numberMaterials);
for numMat = 1 : numberMaterials
	materialE(numMat) = fileData(fileLine, 1);
	materialA(numMat) = fileData(fileLine, 2);
	fileLine = fileLine + 1;
end


% Process mesh variables

elementE = zeros(1, numberElements);
elementA = zeros(1, numberElements);

for numEle = 1 : numberElements
	elementE(numEle) = materialE(elementMaterial(numEle));
	elementA(numEle) = materialA(elementMaterial(numEle));
end


MESH.number_nodes = numberNodes;
MESH.number_elements = numberElements;
MESH.node_coordinates = nodeCoordinates;
MESH.element_connectivity = elementConnectivity;
MESH.young_modulus = elementE;
MESH.area = elementA;
