import json
import os

FILE_PATH = "projects.json"

## importing a json files to save and load different projects

def load_projects():
  if not os.path.exists(FILE_PATH):
    return []
  try:
    with open(FILE_PATH, "r") as file:
      data = json.load(file)
      return data
  except json.JSONDecodeError:
    return []

def save_projects(projects):
  with open(FILE_PATH, "w") as file:
    json.dump(projects, file, indent=2)

ARCHIVE_FILE = "archive.json"

def load_archive():
  if not os.path.exists(ARCHIVE_FILE):
    return []
  try:
    with open(ARCHIVE_FILE, "r") as file:
      data = json.load(file)
      return data
  except json.JSONDecodeError:
    return []

def save_archive(archive):
  with open(ARCHIVE_FILE, "w") as file:
    json.dump(archive, file, indent=2)