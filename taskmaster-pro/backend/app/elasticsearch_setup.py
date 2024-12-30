from .elasticsearch_client import es

# The create_index() function is used to create the 'tasks' index in Elasticsearch.
def create_index():
    if not es.indices.exists(index="tasks"):
        es.indices.create(index="tasks", body={
            "mappings": {
                "properties": {
                    "task_id": {"type": "integer"},
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "due_date": {"type": "date"},
                    "owner_id": {"type": "integer"},
                    "is_completed": {"type": "boolean"},
                }
            }
        })
        print("Index 'tasks' created")
    else:
        print("Index 'tasks' already exists")

def delete_index():
    if es.indices.exists(index="tasks"):
        es.indices.delete(index="tasks")
        print("Index 'tasks' deleted")

if __name__ == "__main__":
    delete_index()  # Optional: Clears the index
    create_index()  # Creates a new index with the appropriate mappings
