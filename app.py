from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import os

PORT = 8000
DATA_FILE = "tasks.json"

# ✅ Robust load function
def load_tasks():
    # If file doesn't exist → create it
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()

            # If file is empty
            if not content:
                return []

            return json.loads(content)

    except (json.JSONDecodeError, ValueError):
        # If file is corrupted → reset
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

# ✅ Safe save
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

tasks = load_tasks()

class TodoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        task_html = ""
        for i, task in enumerate(tasks):
            done_class = "done" if task["done"] else ""

            complete_btn = ""
            if not task["done"]:
                complete_btn = f"""
                <form method="POST">
                    <input type="hidden" name="complete" value="{i}">
                    <button class="complete">Complete</button>
                </form>
                """

            delete_btn = f"""
            <form method="POST">
                <input type="hidden" name="delete" value="{i}">
                <button class="delete">Delete</button>
            </form>
            """

            task_html += f"""
            <div class="task {done_class}">
                <span>{task['text']}</span>
                <div class="actions">
                    {complete_btn}
                    {delete_btn}
                </div>
            </div>
            """

        html = f"""
        <html>
        <head>
            <title>To-Do App hai</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #f4f6f8;
                    display: flex;
                    justify-content: center;
                    margin-top: 50px;
                }}
                .container {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    width: 400px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                h2 {{
                    text-align: center;
                }}
                input[type="text"] {{
                    width: 70%;
                    padding: 8px;
                    margin-right: 5px;
                }}
                button {{
                    padding: 8px;
                    border: none;
                    cursor: pointer;
                    border-radius: 5px;
                }}
                .add-btn {{
                    background: #28a745;
                    color: white;
                }}
                .task {{
                    display: flex;
                    justify-content: space-between;
                    background: #f1f1f1;
                    padding: 10px;
                    margin-top: 10px;
                    border-radius: 5px;
                }}
                .done span {{
                    text-decoration: line-through;
                    color: gray;
                }}
                .complete {{
                    background: #007bff;
                    color: white;
                    margin-right: 5px;
                }}
                .delete {{
                    background: #dc3545;
                    color: white;
                }}
                .actions form {{
                    display: inline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📝 To-Do App hai hello</h2>

                <form method="POST">
                    <input type="text" name="task" placeholder="Enter task" required>
                    <button class="add-btn">Add</button>
                </form>

                {task_html}
            </div>
        </body>
        </html>
        """

        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        global tasks

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed = urllib.parse.parse_qs(post_data.decode())

        # Add task
        if "task" in parsed:
            task_text = parsed.get("task")[0]
            tasks.append({"text": task_text, "done": False})

        # Complete task
        if "complete" in parsed:
            index = int(parsed.get("complete")[0])
            if 0 <= index < len(tasks):
                tasks[index]["done"] = True

        # Delete task
        if "delete" in parsed:
            index = int(parsed.get("delete")[0])
            if 0 <= index < len(tasks):
                tasks.pop(index)

        save_tasks(tasks)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("", PORT), TodoHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
