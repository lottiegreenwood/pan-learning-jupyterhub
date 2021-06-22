import csv, re
from string import Template
import sys, getopt

jhubvalues = {}
jhubvaluemapping = {
  'Course': 'SHORTCOURSE',
  'Branch': 'BRANCH_REQUESTED',
  'Github': 'REQUESTED_GITHUB_REPO_LINK',
  'CPU': 'REQUESTED_CPU',
  'Memory': 'REQUESTED_MEMORY',
  'Container': 'REQUESTED_CONTAINER',
  'Software': 'REQUIRED_SOFTWARE',
  'Containerfile': 'DOCKERFILE',
  'Dockerhub': 'DOCKERHUB',
  'Permission': 'PERMISSION_TO_SHARE'  
}
def REQUESTED_CPU(reqcpu):
  if reqcpu == "Default":
    jhubvalues["CPU_GUARANTEE"] = "1"
  elif reqcpu == "More (2 core limit)": 
    jhubvalues["CPU_GUARANTEE"] = "2"
  elif reqcpu == "A lot (4 core limit)": 
    jhubvalues["CPU_GUARANTEE"] = "4"
  else:
    jhubvalues["CPU_GUARANTEE"] = "UNKNOWN"

def REQUESTED_MEMORY(reqmem):
  if reqmem == "Default":
    jhubvalues["MEM_GUARANTEE"] = "2G"
  elif reqmem == "More (4G limit)": 
    jhubvalues["MEM_GUARANTEE"] = "4G"
  elif reqmem == "A lot (16G limit)": 
    jhubvalues["MEM_GUARANTEE"] = "16G"
  else:
    jhubvalues["MEM_GUARANTEE"] = "UNKNOWN"

def REQUESTED_CONTAINER(reqcontainer):
  if reqcontainer == "Just JupyterHub":
    jhubvalues["IMAGE_NAME"] = "jupyterhub/k8s-singleuser-sample"
    jhubvalues["IMAGE_TAG"] = "0.10.6-n031.h4728fa2f"
  elif reqcontainer == "Dram container with McStas":
    jhubvalues["IMAGE_NAME"] = "trnielsen/jhub_py38_dram"
    jhubvalues["IMAGE_TAG"] = "latest"
  elif reqcontainer == "Dram container with SCIPP":
    jhubvalues["IMAGE_NAME"] = "trnielsen/jhub37_mantid_baseline"
    jhubvalues["IMAGE_TAG"] = "latest"
  else:
    jhubvalues["IMAGE_NAME"] = "trnielsen/jhub_py38_dram"
    jhubvalues["IMAGE_TAG"] = "latest"

def SHORTCOURSE(shortcourse):
  jhubvalues["SHORTCOURSE"] = shortcourse.lower()

funcmapper = {
  "REQUESTED_CONTAINER": REQUESTED_CONTAINER,
  "REQUESTED_CPU": REQUESTED_CPU,
  "REQUESTED_MEMORY": REQUESTED_MEMORY,
  "SHORTCOURSE": SHORTCOURSE,
  }

def main(argv):
  csvinput = 'surveyresponse.csv' 
  try:
    opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
    print('test.py -i <inputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('test.py -i <inputfile>')
      sys.exit()
    elif opt in ("-i", "--ifile"):
      csvinput = arg
  with open(csvinput, mode='r') as infile: #or whatever the .csv file is called
    reader = csv.DictReader(infile)
    responses = next(reader) #will only read one line, first line only
  #loop using keys
  for keys in responses:
    strippedkey = (re.sub('[()]','', keys.split(' ', 1)[0]))
    if strippedkey in jhubvaluemapping:
      if responses[keys]: #ie should not be an empty answer   
        moodlevalue = jhubvaluemapping[strippedkey]
        if moodlevalue not in funcmapper:
          jhubvalues[moodlevalue] = (responses[keys])
        else: 
          func = funcmapper.get(moodlevalue, lambda: "Invalid value")
          func(responses[keys])
  print (jhubvalues) 
  with open('jhubtemplate.yml', mode='r') as templatefile:
    src = Template(templatefile.read())
    result = src.substitute(**jhubvalues)
    outputfile = jhubvalues["SHORTCOURSE"]+"config.yaml.erb"
    f = open(outputfile, "w")
    f.write(result)
    f.close()
  

if __name__ == "__main__":
    main(sys.argv[1:])
