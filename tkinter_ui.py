import tkinter as tk
from tkinter import messagebox
from storage import load_projects, save_projects, load_archive, save_archive
from tkinter import simpledialog

def create_main_window():
    root = tk.Tk()
    root.title("Project Tracker")

    tk.Label(root, text="Project Tracker", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Button(root, text="View Projects", width=25, command=view_projects).pack(pady=5)
    tk.Button(root, text="Add Project", width=25, command=add_project_window).pack(pady=5)
    tk.Button(root, text="View Archived Projects", width=25, command=view_archived_projects).pack(pady=5)
    tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=10)

    root.mainloop()

def view_projects():
    projects = load_projects()
    if not projects:
        messagebox.showinfo("No Projects", "No saved projects found.")
        return

    win = tk.Toplevel()
    win.title("All Projects")

    tk.Label(win, text="Select a project:").pack()
    project_list = tk.Listbox(win, width=50)
    for p in projects:
        project_list.insert(tk.END, p["Project Name"])
    project_list.pack()

    def open_project_details():
        try:
            index = project_list.curselection()[0]
        except IndexError:
            messagebox.showwarning("Select Project", "Please select a project.")
            return

        open_project_view_window(index, projects)

    tk.Button(win, text="Open Project", command=open_project_details).pack(pady=10)


def add_project_window():
    def save_project():
        name = entry_name.get()
        desc = entry_desc.get()
        tasks_text = text_tasks.get("1.0", tk.END).strip().split("\n")
        tasks = [{"task": t.strip(), "done": False} for t in tasks_text if t.strip()]
        project = {
            "Project Name": name,
            "Description": desc,
            "Tasks": tasks
        }
        projects = load_projects()
        projects.append(project)
        save_projects(projects)
        messagebox.showinfo("Success", "Project saved.")
        add_win.destroy()

    add_win = tk.Toplevel()
    add_win.title("Add New Project")

    tk.Label(add_win, text="Project Name").pack()
    entry_name = tk.Entry(add_win, width=40)
    entry_name.pack()

    tk.Label(add_win, text="Description").pack()
    entry_desc = tk.Entry(add_win, width=40)
    entry_desc.pack()

    tk.Label(add_win, text="Tasks (one per line)").pack()
    text_tasks = tk.Text(add_win, width=40, height=10)
    text_tasks.pack()

    tk.Button(add_win, text="Save Project", command=save_project).pack(pady=10)

def archive_project_window():
    projects = load_projects()
    if not projects:
        messagebox.showinfo("No Projects", "There are no projects to archive.")
        return

    window = tk.Toplevel()
    window.title("Archive a Project")

    tk.Label(window, text="Select a project to archive:").pack()

    listbox = tk.Listbox(window, width=50)
    for p in projects:
        listbox.insert(tk.END, p["Project Name"])
    listbox.pack()

    def archive_selected():
        selected_index = listbox.curselection()
        if not selected_index:
            return
        idx = selected_index[0]
        archive = load_archive()
        archived = projects.pop(idx)
        archive.append(archived)
        save_projects(projects)
        save_archive(archive)
        messagebox.showinfo("Archived", f"Archived project: {archived['Project Name']}")
        window.destroy()

    tk.Button(window, text="Archive Selected Project", command=archive_selected).pack(pady=10)

def view_archived_projects():
    archive = load_archive()
    if not archive:
        messagebox.showinfo("Archive", "No archived projects.")
        return

    window = tk.Toplevel()
    window.title("Archived Projects")

    for project in archive:
        frame = tk.LabelFrame(window, text=project["Project Name"], padx=10, pady=5)
        frame.pack(padx=10, pady=5, fill="x")
        tk.Label(frame, text=project["Description"]).pack(anchor="w")
        for task in project["Tasks"]:
            status = "✓" if task["done"] else "✗"
            tk.Label(frame, text=f"  {status} {task['task']}", anchor="w").pack(anchor="w")

def complete_task_window():
    projects = load_projects()
    if not projects:
        messagebox.showinfo("No Projects", "No saved projects found.")
        return

    win = tk.Toplevel()
    win.title("Complete a Task")

    tk.Label(win, text="Select a project:").pack()

    project_list = tk.Listbox(win, width=40, height=10)
    for p in projects:
        project_list.insert(tk.END, p["Project Name"])
    project_list.pack()

    tk.Label(win, text="Select a task:").pack()
    task_list = tk.Listbox(win, width=50, height=10)
    task_list.pack()

    # Store selected project index safely
    selected_project_index = {"index": None}

    def load_tasks(event=None):
        try:
            idx = project_list.curselection()[0]
        except IndexError:
            return

        selected_project_index["index"] = idx  # Save the project index

        task_list.delete(0, tk.END)
        for task in projects[idx]["Tasks"]:
            status = "✓" if task["done"] else " "
            task_list.insert(tk.END, f"[{status}] {task['task']}")

    def mark_selected_done():
        proj_idx = selected_project_index["index"]
        try:
            task_idx = task_list.curselection()[0]
        except IndexError:
            messagebox.showwarning("Select Task", "Please select a task.")
            return

        if proj_idx is None:
            messagebox.showwarning("Select Project", "Please select a project.")
            return

        # Mark the task as done
        projects[proj_idx]["Tasks"][task_idx]["done"] = True
        save_projects(projects)
        messagebox.showinfo("Success", "Task marked as complete.")

        load_tasks()  # Refresh the task list view

    project_list.bind("<<ListboxSelect>>", load_tasks)

    tk.Button(win, text="Mark Task as Done", command=mark_selected_done).pack(pady=10)

def open_project_view_window(index, projects):
    project = projects[index]

    win = tk.Toplevel()
    win.title(f"Project: {project['Project Name']}")

    tk.Label(win, text=f"Description: {project['Description']}").pack(pady=5)
    tk.Label(win, text="Tasks:").pack()

    task_list = tk.Listbox(win, width=50)
    for task in project["Tasks"]:
        status = "✓" if task["done"] else " "
        task_list.insert(tk.END, f"[{status}] {task['task']}")
    task_list.pack()

    def refresh_task_list():
        task_list.delete(0, tk.END)
        for task in project["Tasks"]:
            status = "✓" if task["done"] else " "
            task_list.insert(tk.END, f"[{status}] {task['task']}")

    def mark_task_done():
        try:
            task_index = task_list.curselection()[0]
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task.")
            return

        project["Tasks"][task_index]["done"] = True
        save_projects(projects)

        # Refresh task list
        task_list.delete(0, tk.END)
        for task in project["Tasks"]:
            status = "✓" if task["done"] else " "
            task_list.insert(tk.END, f"[{status}] {task['task']}")

        messagebox.showinfo("Success", "Task marked as complete.")

    tk.Button(win, text="Mark Selected Task as Done", command=mark_task_done).pack(pady=5)

    def delete_task():
        try:
            task_index = task_list.curselection()[0]
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            del project["Tasks"][task_index]
            save_projects(projects)
            refresh_task_list()

    def add_task():
        new_task = simpledialog.askstring("Add Task", "Enter a new task:", parent=win)
        if not new_task:
            return

        # Try to insert after the currently selected task
        try:
            selected_index = task_list.curselection()[0]
            insert_position = selected_index + 1
        except IndexError:
            # If no task is selected, add to the end
            insert_position = len(project["Tasks"])

        project["Tasks"].insert(insert_position, {"task": new_task.strip(), "done": False})
        save_projects(projects)
        refresh_task_list()

    def archive_project():
        confirm = messagebox.askyesno("Archive Project", f"Are you sure you want to archive '{project['Project Name']}'?")
        if confirm:
            archive = load_archive()
            archive.append(project)
            del projects[index]
            save_projects(projects)
            save_archive(archive)
            messagebox.showinfo("Archived", "Project archived.")
            win.destroy()

    def delete_project():
        confirm = messagebox.askyesno("Delete Project", f"Delete project '{project['Project Name']}' permanently?")
        if confirm:
            del projects[index]
            save_projects(projects)
            messagebox.showinfo("Deleted", "Project deleted.")
            win.destroy()

    tk.Button(win, text="Add New Task", command=add_task).pack(pady=2)
    tk.Button(win, text="Delete Selected Task", command=delete_task).pack(pady=2)
    tk.Button(win, text="Archive Project", fg="red", command=archive_project).pack(pady=2)
    tk.Button(win, text="Delete Project", fg="red", command=delete_project).pack(pady=5)

if __name__ == "__main__":
    create_main_window()