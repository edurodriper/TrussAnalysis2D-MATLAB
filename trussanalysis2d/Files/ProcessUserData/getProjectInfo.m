function [INFO] = getProjectInfo(INFO)

% Project directory
projectDir = uigetdir('', 'Select Project Folder');

% Output files name
fileName = input('Output files name: ', 's');


INFO.project_directory = projectDir;
INFO.file_name = fileName;