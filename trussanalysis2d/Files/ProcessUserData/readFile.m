function [fileData] = readFile(fileName, filePath)

fid = fopen([filePath, fileName], 'r');

% Initialize matrix row to match file line
i = 1;

while ~feof(fid)
	% String with line content
	newLine = fgetl(fid);
	lineLength = length(newLine);
	% Comma location
	commaLoc = strfind(newLine, ',');
	% Define delimiters to numerical values
	del = [1, commaLoc, lineLength];

	for j = 1 : length(del)-1
		startDel = del(j);
		endDel = del(j+1);
		% String with content inside delimiters
		strValue = newLine(startDel:endDel);
		% Convert string to double and insert into matrix
		fileData(i ,j) = str2double(strValue);
	end
	% Move to next matrix row
	i = i + 1;
end

fclose(fid);