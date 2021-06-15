import csv, re

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
with open('surveyresponse.csv', mode='r') as infile: #or whatever the .csv file is called
  reader = csv.DictReader(infile)
  responses = next(reader) #will only read one line, first line only

#loop using keys
for keys in responses:
  strippedkey = (re.sub('[()]','', keys.split(' ', 1)[0]))
  #This if statement was required when Github appeared in too separate question labels
  #if "(" not in keys:
  #  continue
  #strippedkey = keys.split("(")[1].split(")")[0]
  print(strippedkey)
  if strippedkey in jhubvaluemapping: #ie should not be an empty answer
    moodlevalue = jhubvaluemapping[strippedkey]
    jhubvalues[moodlevalue] = responses[keys]
print (jhubvalues) 

