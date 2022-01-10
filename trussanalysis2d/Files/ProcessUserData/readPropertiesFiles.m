function [FILEDATA] = readPropertiesFiles(FILEDATA, INFO)

projectDir = INFO.project_directory;


% Read mesh file
[fileName, filePath] = uigetfile(...
	'*.txt', 'Select Mesh File', [projectDir, '\']);
[fileDataMesh] = readFile(fileName, filePath);

% Read displacements file
[fileName, filePath] = uigetfile(...
	'*.txt', 'Select Displacements File', [projectDir, '\']);
[fileDataDisp] = readFile(fileName, filePath);

% Read forces file
[fileName, filePath] = uigetfile(...
	'*.txt', 'Select Forces File', [projectDir, '\']);
[fileDataForc] = readFile(fileName, filePath);


FILEDATA.mesh = fileDataMesh;
FILEDATA.displacements = fileDataDisp;
FILEDATA.forces = fileDataForc;
