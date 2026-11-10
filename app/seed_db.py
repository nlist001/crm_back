

import json
from app.db import db_dependency
from app.models.products import BrandTable


def seed_db(db: db_dependency):
    def read_json(filename):
        with open(filename,'r') as file:
            return json.load(file)
    data = read_json("db-data/brands.json")
    
    brands = [BrandTable(**b) for b in data]
    db.bulk_save_objects(brands)
    db.commit()

    