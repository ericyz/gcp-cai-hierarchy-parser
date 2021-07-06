from absl import app
from absl import flags

import json
import collections

FLAGS = flags.FLAGS

flags.DEFINE_string('cai-resource-file-path', None, 'The path of CAI resource export file.')
flags.mark_flag_as_required("cai-resource-file-path")

graph = collections.defaultdict(list)
folder_name_map = {}

def main(argv):
    del argv
    
    file_path = FLAGS['cai-resource-file-path'].value

    orgs = []
    folders = []
    projects = []

    with open(file_path) as file:
        for line in file.readlines():
            obj = json.loads(line)
            if obj['asset_type'] == 'cloudresourcemanager.googleapis.com/Organization':
                orgs.append(obj)
            elif obj['asset_type'] == 'cloudresourcemanager.googleapis.com/Folder':
                folders.append(obj)
            elif obj['asset_type'] == 'cloudresourcemanager.googleapis.com/Project':
                projects.append(obj)
    
    graph = build_graph(folders, projects)
    stack = []
    for org in orgs:
        org_id = org["resource"]["data"]["name"]
        stack.append((0, org_id))
    
    while stack:
        level, item = stack.pop()
        print('|'+'-'*level + folder_name_map.get(item, item))
        for child in graph[item]:
            stack.append((level+1, child))

def build_graph(folders, projects):
    graph = collections.defaultdict(list)

    for folder in folders:
        folder_id = folder["resource"]["data"]["name"]
        folder_name_map[folder_id] = folder["resource"]["data"]["displayName"]
        parent_id = folder["resource"]["data"]["parent"]
        graph[parent_id].append(folder_id)
    
    for project in projects:
        type = project["resource"]["data"]["parent"]["type"]
        parent_id = project["resource"]["data"]["parent"]["id"]
        project_id = project["resource"]["data"]["projectId"]
        graph[f'{type}s/{parent_id}'].append(project_id)
    return graph
   
if __name__ == '__main__':
    app.run(main)