import sys
sys.path.append(".")
from app.models.models import Base, engine
Base.metadata.create_all(bind=engine)
print("Tables created!")
