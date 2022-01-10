function [] = writeInputData(INFO, MESH, DISPLACEMENTS, FORCES)

projectDir = INFO.project_directory;
fileName = INFO.file_name;
numberNodes = MESH.number_nodes;
numberElements = MESH.number_elements;
nodeCoordinates = MESH.node_coordinates;
elementConnectivity = MESH.element_connectivity;
materialE = MESH.young_modulus;
materialA = MESH.area;
numberPin = DISPLACEMENTS.number_pin;
pinNodes = DISPLACEMENTS.pin_nodes;
pinDisplacements = DISPLACEMENTS.pin_displacements;
pinAngles = DISPLACEMENTS.pin_angles;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerDirections = DISPLACEMENTS.roller_directions;
rollerDisplacements = DISPLACEMENTS.roller_displacements;
rollerAngles = DISPLACEMENTS.roller_angles;
numberForces = FORCES.number_forces;
forceNodes = FORCES.force_nodes;
forceComponents = FORCES.force_components;
forceAngles = FORCES.force_angles;


newFileName = [fileName, '_DATA.dat'];
filePath = [projectDir, '\', newFileName];
fid = fopen(filePath, 'w');

barLine = '----------------------------------------';

fprintf(fid, '%16s\n', 'NODE COORDINATES');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%4s %11s %11s\n', 'NODE', 'X(M)', 'Y(M)');
for numNod = 1 : numberNodes
	nCoordX = nodeCoordinates(1, numNod);
	nCoordY = nodeCoordinates(2, numNod);	
	fprintf(fid, '%-4d %11.3f %11.3f\n', numNod, nCoordX, nCoordY);
end
fprintf(fid, '\n');

fprintf(fid, '%8s\n', 'ELEMENTS');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%3s %6s %6s %11s %10s\n', ...
	'EL.', 'NODE1', 'NODE2', 'A(M2)', 'E(PA)');
for numEle = 1 : numberElements
	node1 = elementConnectivity(1, numEle);
	node2 = elementConnectivity(2, numEle);
	A = materialA(numEle);
	E = materialE(numEle);
	fprintf(fid, '%-3d %6d %6d %11.6G %10.5G\n', numEle, node1, node2, A, E);
end
fprintf(fid, '\n');

if (numberPin > 0)
	fprintf(fid, '%12s\n', 'PIN SUPPORTS');
	fprintf(fid, '%40s\n', barLine);
	fprintf(fid, '%4s %11s %11s %11s\n', 'NODE', 'DX''(M)', 'DY''(M)', 'ANGLE(DEG)');
	for numPin = 1 : numberPin
		pNode = pinNodes(numPin);
		pDisplX = pinDisplacements(1, numPin);
		pDisplY = pinDisplacements(2, numPin);
		pAngle = pinAngles(numPin);
		fprintf(fid, '%-4d %11.3f %11.3f %11.2f\n', pNode, pDisplX, pDisplY, pAngle);
	end
	fprintf(fid, '\n');
end

if (numberRoller > 0)
	fprintf(fid, '%15s\n', 'ROLLER SUPPORTS');
	fprintf(fid, '%40s\n', barLine);
	fprintf(fid, '%4s %11s %11s %11s\n', 'NODE', 'DIRECTION', 'DN(M)', 'ANGLE(DEG)');
	for numRol = 1 : numberRoller
		rNode = rollerNodes(numRol);
		rDirection = rollerDirections(numRol);
		rDisplN = rollerDisplacements(numRol);
		rAngle = rollerAngles(numRol);
		fprintf(fid, '%-4d %11d %11.3f %11.2f\n', rNode, rDirection, rDisplN, rAngle);
	end
	fprintf(fid, '\n');
end

fprintf(fid, '%6s\n', 'FORCES');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%4s %11s %11s %11s\n', 'NODE', 'FX''(N)', 'FY''(N)', 'ANGLE(DEG)');
for numFor = 1 : numberForces
	fNode = forceNodes(numFor);
	fCompX = forceComponents(1, numFor);
	fCompY = forceComponents(2, numFor);
	fAngle = forceAngles(numFor);
	fprintf(fid, '%-4d %11.6G %11.6G %11.2f\n', fNode, fCompX, fCompY, fAngle);
end	

fclose(fid);