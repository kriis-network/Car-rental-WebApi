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

# Employee operations
def find_all_employees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json, 'All employees'

def find_employee_by_id(employee_id):
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee) WHERE a.id=$id RETURN a;", id=employee_id)
        nodes_json = [node_to_json(record["a"]) for record in employee]
        return nodes_json, f'Employee with id {employee_id} found'

def save_employee(name, address, branch, employee_id):
    with _get_connection().session() as session:
        employees = session.run(
            "MERGE (a:Employee {id: $id}) SET a.name = $name, a.address = $address, a.branch = $branch, a.id = $id RETURN a;",
            name=name, address=address, branch=branch, id=employee_id
        )
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json, f'Employee with id {employee_id} saved to database'

def update_employee(name, address, branch, employee_id):
    with _get_connection().session() as session:
        employees = session.run(
            "MATCH (a:Employee {id: $id}) SET a.name = $name, a.address = $address, a.branch = $branch RETURN a;",
            name=name, address=address, branch=branch, id=employee_id
        )
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json, f'Employee with id {employee_id} updated'

def delete_employee(employee_id):
    _get_connection().execute_query("MATCH (a:Employee {id: $id}) DELETE a;", id=employee_id)
    return f'Employee with id {employee_id} deleted'


