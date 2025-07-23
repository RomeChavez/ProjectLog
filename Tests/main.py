from storage import load_projects, save_projects, load_archive, save_archive

def project_info(): ## this function is going to get the project info and description with tasks
  print("Create a New Project")

  ## this code get the basic info of the project

  project_name = input("Enter Project Name: ")
  description = input("Enter Project Description: ")

  ## this code will have the user input the tasks they want done with the project

  tasks = []
  print("Add tasks for this project (type 'done' when finished):")
  while True:
        task = input("Enter a task: ").strip()
        if task.lower() == "done":
            break
        if task:
            tasks.append({"task": task, "done": False})

  ## this code will store everything in a dictionary

  project = {
    "Project Name": project_name,
    "Description": description,
    "Tasks": tasks
  }

  ## Display conformation

  print("\nProject Created")
  print(f"Project Name: {project_name}")
  print(f"Description: {description}")
  print(f"Tasks: {tasks}")
  for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task['task']} [ ]") ## [ ] is a visual indicator that the task is not done yet

  return project

def view_all_projects():
  projects = load_projects()

  if not projects:
    print("\n No projects found.")
    return

  print("\n All Projects:")
  for i, project in enumerate(projects, 1):
    print(f"\n{i}. Project Name: {project['Project Name']}")
    print(f"Description: {project['Description']},")
    print("Tasks: ")
    for j, task in enumerate(project['Tasks'], 1):
      status = "X" if task['done'] else " "
      print(f"  {j}. {task['task']} [{status}]")

def mark_tasks_complete(project):
  print("\nTasks for Project:")
  for i, task in enumerate(project['Tasks'], 1):
    status = "X" if task['done'] else " "
    print(f"  {i}. {task['task']} [{status}]")

  while True:
    task_to_mark = input("Enter the task number to mark as complete (or 'done' to finish): ")
    if task_to_mark.lower() == 'done':
      break
    try:
      task_index = int(task_to_mark) - 1
      if 0 <= task_index < len(project['Tasks']):
        project['Tasks'][task_index]['done'] = True
        print(f"Task {task_index + 1} marked as complete.")
      else:
        print("Invalid task number.")
    except ValueError:
      print("Please enter a valid number or 'done'.")

def archive_project():
  projects = load_projects()

  if not projects:
    print("\n No projects found.")
    return

  print("\nSelect a project to archive:")
  for i, project in enumerate(projects, 1):
    print(f"{i}. {project['Project Name']}")

  try:
        choice = int(input("Enter the project number to archive (or 0 to cancel): ")) - 1
        if choice == -1:
            return
        if 0 <= choice < len(projects):
            archive = load_archive()
            archived = projects.pop(choice)
            archive.append(archived)
            save_projects(projects)
            save_archive(archive)
            print(f"Project '{archived['Project Name']}' moved to archive.")
        else:
            print("Invalid project number.")
  except ValueError:
        print(" Please enter a valid number.")

def view_archived_projects():
  archive = load_archive()
  if not archive:
    print("\n No archived projects found.")
    return

  print("\n Archived Projects:")
  for i, project in enumerate(archive, 1):
        print(f"\n{i}. Project Name: {project['Project Name']}")
        print(f"Description: {project['Description']}")
        print("Tasks:")
        for j, task in enumerate(project["Tasks"], 1):
            status = "X" if task["done"] else " "
            print(f"  {j}. {task['task']} [{status}]")


## main menu where the user can create a project, view projects, or exit

# from storage import load_projects, save_projects

def main():
  while True:
    print("\n=== Project Tracker ===")
    print("1. Create a New Project")
    print("2. View All Projects")
    print("3. Archive a Project")
    print("4. View Archived Projects")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
      project = project_info()
      projects = load_projects()
      projects.append(project)
      save_projects(projects)
      print("\nProject saved successfully!")
    elif choice == "2":
      projects = load_projects()
      if not projects:
        print("\n No projects found.")
        continue

      ## show all projects
      print("\nAll Projects:")
      for i, project in enumerate(projects, 1):
        print(f"{i}. {project['Project Name']}")

      ## select a project
      try:
        selected = int(input("Select a project number to view: ")) - 1
        if selected < 0 or selected >= len(projects):
          print("Invalid selection.")
          continue
      except ValueError:
        print("Please enter a valid number.")
        continue

      ## Let user mark tasks as complete
      mark_tasks_complete(projects[selected])
      save_projects(projects)

    elif choice == "3":
      archive_project()
    elif choice == "4":
      view_archived_projects()
    elif choice == "5":
      print("Exiting Project Tracker. Goodbye!")
      break
    else:
      print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
  main()