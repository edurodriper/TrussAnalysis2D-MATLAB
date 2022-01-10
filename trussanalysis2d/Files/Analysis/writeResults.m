function [] = writeResults(INFO, MESH, DISPLACEMENTS, SOLUTION)

projectDir = INFO.project_directory;
fileName = INFO.file_name;
numberNodes = MESH.number_nodes;
numberElements = MESH.number_elements;
numberSupport = DISPLACEMENTS.number_support;
supportNodes = DISPLACEMENTS.support_nodes;
U = SOLUTION.global_displacements;
R = SOLUTION.global_reactions;
elementStress = SOLUTION.element_stress;
elementForce = SOLUTION.element_force;


newFileName = [fileName, '_RESULTS.dat'];
filePath = [projectDir, '\', newFileName];
fid = fopen(filePath, 'w');

barLine = '----------------------------------------';

fprintf(fid, '%18s\n', 'NODE DISPLACEMENTS');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%4s %11s %11s %11s\n', 'NODE', 'DX(M)', 'DY(M)', 'DM(M)');
for numNod = 1 : numberNodes
	displX = U(2*numNod-1);
	displY = U(2*numNod);
	displM = (displX^2 + displY^2)^0.5;
	fprintf(fid, '%-4d %11.3E %11.3E %11.3E\n', numNod, displX, displY, displM);
end
fprintf(fid, '\n');

fprintf(fid, '%27s\n', 'ELEMENT FORCES AND STRESSES');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%3s %14s %14s\n', 'EL.', 'FORCE(N)', 'STRESS(PA)');
for numEle = 1 : numberElements
	elemForce = elementForce(numEle);
	elemStress = elementStress(numEle);
	fprintf(fid, '%-3d %+14.6E %+14.6E\n', numEle, elemForce, elemStress);
end
fprintf(fid, '\n');

fprintf(fid, '%17s\n', 'SUPPORT REACTIONS');
fprintf(fid, '%40s\n', barLine);
fprintf(fid, '%4s %11s %11s %11s\n', 'NODE', 'RX(N)', 'RY(N)', 'RM(N)');
for numSup = 1 : numberSupport
	sNode = supportNodes(numSup);
	reactX = R(1, numSup);
	reactY = R(2, numSup);
	reactM = (reactX^2 + reactY^2)^0.5;
	fprintf(fid, '%-4d %11.3E %11.3E %11.3E\n', sNode, reactX, reactY, reactM);
end

fclose(fid);