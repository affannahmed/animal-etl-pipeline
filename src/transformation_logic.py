from datetime import datetime
from dateutil import parser


class AnimalTransformer:

    @staticmethod
    def transform_animal(animal_data):
        transformed = animal_data.copy()
        
        # ---- Transform friends field : "dog,cat" to ["dog", "cat", "bird"] --- :)
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
                dt = parser.parse(transformed["born_at"])
                transformed["born_at"] = dt.isoformat()
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not parse born_at '{transformed['born_at']}': {e}")
                transformed["born_at"] = None
        
        return transformed
    
    @staticmethod
    def transform_batch(animals_list):
        """Transform a batch of animals."""
        return [AnimalTransformer.transform_animal(animal) for animal in animals_list]