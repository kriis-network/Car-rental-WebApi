from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://3da6e885.databases.neo4j.io:7687"
AUTH = ("neo4j", "M_jBdvj6VIQZoTZvmxin541E1-nU_jAAlEUkDnWHJtI")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

# Customer operations
def find_all_customers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers]
        return nodes_json, 'All customers'

def find_customer_by_id(customer_id):
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer) WHERE a.id=$id RETURN a;", id=customer_id)
        nodes_json = [node_to_json(record["a"]) for record in customer]
        return nodes_json, f'Customer with id {customer_id} found'

def save_customer(name, age, address, ordered_car, customer_id):
    with _get_connection().session() as session:
        customers = session.run(
            "MERGE (a:Customer {id: $id}) SET a.name = $name, a.age = $age, a.address = $address, a.ordered_car = $ordered_car, a.id = $id RETURN a;",
            name=name, age=age, address=address, ordered_car=ordered_car, id=customer_id
        )
        nodes_json = [node_to_json(record["a"]) for record in customers]
        return nodes_json, f'Customer with id {customer_id} saved to database'

def update_customer(name, age, address, ordered_car, customer_id):
    with _get_connection().session() as session:
        customers = session.run(
            "MATCH (a:Customer {id: $id}) SET a.name = $name, a.age = $age, a.address = $address, a.ordered_car = $ordered_car RETURN a;",
            name=name, age=age, address=address, ordered_car=ordered_car, id=customer_id
        )
        nodes_json = [node_to_json(record["a"]) for record in customers]
        return nodes_json, f'Customer with id {customer_id} updated'

def delete_customer(customer_id):
    _get_connection().execute_query("MATCH (a:Customer {id: $id}) DELETE a;", id=customer_id)
    return f'Customer with id {customer_id} deleted'
