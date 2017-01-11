import os
import sys


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from scheduler.app import create_app
    app = create_app(SECRET_KEY=os.environ["SECRET_KEY"])
    app.run(debug=True)
