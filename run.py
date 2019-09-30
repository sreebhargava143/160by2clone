from project import create_app
from project import db
from project.models import User, Message, Contact

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db':db,
        'User':User,
        'Message':Message,
        'Contact': Contact
    }

if __name__ == "__main__":
    app.run(debug=True)