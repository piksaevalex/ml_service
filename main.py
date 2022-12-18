from app import app
from app.db.database import Base, engine
from app.flask_api.controller import *

if __name__ == '__main__':
    print("Creating database .......")
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000, debug=True)
