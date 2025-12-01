from datetime import datetime
from dateutil import parser


class AnimalTransformer:

    @staticmethod
    def transform_animal(animal_data):
        transformed = animal_data.copy()

        if "friends" in transformed and transformed["friends"]:
            if isinstance(transformed["friends"], str):
                transformed["friends"] = [
                    friend.strip() 
                    for friend in transformed["friends"].split(",") 
                    if friend.strip()
                ]
        else:
            transformed["friends"] = []

        if "born_at" in transformed and transformed["born_at"]:
            try:
                if isinstance(transformed["born_at"], int):
                    dt = datetime.fromtimestamp(transformed["born_at"] / 1000)
                    transformed["born_at"] = dt.isoformat()
                elif isinstance(transformed["born_at"], str):
                    dt = parser.parse(transformed["born_at"])
                    transformed["born_at"] = dt.isoformat()
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not parse born_at '{transformed['born_at']}': {e}")
                transformed["born_at"] = None
        
        return transformed
    
    @staticmethod
    def transform_batch(animals_list):
        return [AnimalTransformer.transform_animal(animal) for animal in animals_list]