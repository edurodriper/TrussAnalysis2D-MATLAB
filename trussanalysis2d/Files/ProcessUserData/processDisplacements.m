function [DISPLACEMENTS] = processDisplacements(FILEDATA, DISPLACEMENTS)

fileData = FILEDATA.displacements;


% Process displacements file

fileLine = 1;

numberPin = fileData(fileLine, 1);
fileLine = fileLine + 1;
pinNodes = zeros(1, numberPin);
pinAngles = zeros(1, numberPin);
pinDisplacements = zeros(2, numberPin);
for numPin = 1 : numberPin
	pinNodes(numPin) = fileData(fileLine, 1);
	pinAngles(numPin) = fileData(fileLine, 2);
	pinDisplacements(1, numPin) = fileData(fileLine, 3);
	pinDisplacements(2, numPin) = fileData(fileLine, 4);
	fileLine = fileLine + 1;
end

numberRoller = fileData(fileLine, 1);
fileLine = fileLine + 1;
rollerNodes = zeros(1, numberRoller);
rollerDirections = zeros(1, numberRoller);
rollerAngles = zeros(1, numberRoller);
rollerDisplacements = zeros(1, numberRoller);
for numRol = 1 : numberRoller
	rollerNodes(numRol) = fileData(fileLine, 1);
	rollerDirections(numRol) = fileData(fileLine, 2);
	rollerAngles(numRol) = fileData(fileLine, 3);
	rollerDisplacements(numRol) = fileData(fileLine, 4);
	fileLine = fileLine + 1;
end

% numberTemperature = fileData(fileLine, 1);
% fileLine = fileLine + 1;
% temperatureElements = zeros(1, numberTemperature);
% temperatureDifferences = zeros(1, numberTemperature);
% temperatureCoefficients = zeros(1, numberTemperature);
% for numTem = 1 : numberTemperature
% 	temperatureElements(numTem) = fileData(fileLine, 1);
% 	temperatureDifferences(numTem) = fileData(fileLine, 2);
% 	temperatureCoefficients(numTem) = fileData(fileLine, 3);
% 	fileLine = fileLine + 1;
% end

% numberError = fileData(fileLine, 1);
% fileLine = fileLine + 1;
% errorElements = zeros(1, numberError);
% errorValues = zeros(1, numberError);
% for numErr = 1 : numberError
% 	errorElements(numErr) = fileData(fileLine, 1);
% 	errorValues(numErr) = fileData(fileLine, 2);
% 	fileLine = fileLine + 1;
% end

% Process displacements variables

numberSupport = numberPin + numberRoller;
supportNodes = [pinNodes, rollerNodes];


DISPLACEMENTS.number_pin = numberPin;
DISPLACEMENTS.pin_nodes = pinNodes;
DISPLACEMENTS.pin_angles = pinAngles;
DISPLACEMENTS.pin_displacements = pinDisplacements;
DISPLACEMENTS.number_roller = numberRoller;
DISPLACEMENTS.roller_nodes = rollerNodes;
DISPLACEMENTS.roller_directions = rollerDirections;
DISPLACEMENTS.roller_angles = rollerAngles;
DISPLACEMENTS.roller_displacements = rollerDisplacements;
DISPLACEMENTS.number_support = numberSupport;
DISPLACEMENTS.support_nodes = supportNodes;
% DISPLACEMENTS.number_temperature = numberTemperature;
% DISPLACEMENTS.temperature_elements = temperatureElements;
% DISPLACEMENTS.temperature_differences = temperatureDifferences;
% DISPLACEMENTS.temperature_coefficients = temperatureCoefficients;
% DISPLACEMENTS.number_error = numberError;
% DISPLACEMENTS.error_elements = errorElements;
% DISPLACEMENTS.error_values = errorValues;