class AnimalLoader:

    
    def __init__(self, client, batch_size=100):
        self.client = client
        self.batch_size = batch_size
        self.total_loaded = 0
    
    def load_animals(self, animals_list):

        # --- Load animals in batches ---

        total_animals = len(animals_list)
        print(f"\nLoading {total_animals} animals in batches of {self.batch_size}...")
        
        for i in range(0, total_animals, self.batch_size):
            batch = animals_list[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_animals + self.batch_size - 1) // self.batch_size
            
            try:
                self.client.post_animals(batch)
                self.total_loaded += len(batch)
                print(f"Batch {batch_num}/{total_batches} loaded ({len(batch)} animals)")
            except Exception as e:
                print(f"Error loading batch {batch_num}: {e}")
                raise
        
        print(f"\n Successfully loaded {self.total_loaded} animals!")
        return self.total_loaded