import json
import yaml
import math

dh = {}

pi = 3.14

# we save data from json file to dictionary to change dh notation to coefficients
with open('in.json') as inFile:
    dh = json.load(inFile)
    
# we write to output file (format.yaml) our coefficients
with open('out.yaml', 'w') as outFile:
    for it in dh.keys():
        coeffs = dh[it]
        outFile.write(it + ': \n')
        outFile.write("   " + 'len: ' + str(math.sqrt(math.pow(coeffs[1], 2) + math.pow(coeffs[0], 2))) + '\n')
        outFile.write("   " + 'xyz: ' + '0.0 ' + str(0.5*coeffs[0]) + ' ' + str(0.5 * coeffs[1]) + '\n')
        
        if(coeffs[1] == 0):
            outFile.write("   " + 'rpy: ' + '0.0 ' + str(pi/2) + ' ' + str(pi/2) + '\n')
        else:
            outFile.write("   " + 'rpy: ' + '0.0 0.0 0.0' + '\n')
        
        outFile.write("   " + 'limit: ' + str(-1 *math.sqrt(math.pow(coeffs[1], 2) + math.pow(coeffs[0], 2))) + '\n')
        
        
        outFile.write('\n')
