import sys
from src.client import AnimalAPIClient
from src.transformation_logic import AnimalTransformer
from src.loading_logic import AnimalLoader


def fetch_all_animals(client):
    print("Fetching all animals")
    
    all_animal_ids = []
    page = 1
    
    while True:
        try:
            response = client.get_animals_page(page)
            items = response.get("items", [])
            
            if not items:
                break
            

            animal_ids = [item["id"] for item in items]
            all_animal_ids.extend(animal_ids)
            
            total_pages = response.get("total_pages", page)
            print(f"Fetched page {page}/{total_pages} ({len(items)} animals)")

            if page >= total_pages:
                break
            
            page += 1
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            raise
    
    print(f"Found {len(all_animal_ids)} animals total\n")
    return all_animal_ids


def fetch_animal_details(client, animal_ids):

    print(f"Fetching details for {len(animal_ids)} animals")
    
    animals_details = []
    
    for i, animal_id in enumerate(animal_ids, 1):
        try:
            details = client.get_animal_details(animal_id)
            animals_details.append(details)
            if i % 100 == 0 or i == len(animal_ids):
                print(f"   Progress: {i}/{len(animal_ids)} animals fetched")
                
        except Exception as e:
            print(f"Error fetching animal {animal_id}: {e}")
            raise
    
    print(f"Fetched details for {len(animals_details)} animals\n")
    return animals_details


def main():
    print("Starting Animal ETL Pipeline\n")
    print("=" * 50)
    
    try:
        client = AnimalAPIClient()

        animal_ids = fetch_all_animals(client)

        animals_details = fetch_animal_details(client, animal_ids)

        print("Transforming animal data...")
        transformed_animals = AnimalTransformer.transform_batch(animals_details)
        print(f"Transformed {len(transformed_animals)} animals\n")

        loader = AnimalLoader(client, batch_size=100)
        total_loaded = loader.load_animals(transformed_animals)
        
        print("\n" + "=" * 50)
        print(f"Pipeline completed successfully!")
        print(f"Total animals processed: {total_loaded}")
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nPipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()