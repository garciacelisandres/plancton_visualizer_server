from app.create import create_app
app = create_app("dev")

from app import routes, errorhandlers

app.run()
