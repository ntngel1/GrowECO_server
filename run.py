from server import app
import config

app.run(debug=True, port=config.SERVER_PORT)