#test python
import sys, os
print dir(sys)
print dir(os)
file_path_abs =  sys.argv
print dir(file_path_abs)
print file_path_abs

(filepath, filename) = os.path.split(file_path_abs[0])
print filepath