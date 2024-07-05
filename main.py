from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.complex import ComplexModel
from spyne.model.primitive import String

class Person(ComplexModel):
    id = Integer
    name = Unicode
    age = Integer

people = {}

class PersonService(ServiceBase):
    @rpc(Integer, _returns=Person)
    def get_person(ctx, person_id):
        person = people.get(person_id)
        if person is None:
            return None
        return person

    @rpc(Person, _returns=Unicode)
    def create_person(ctx, person):
        if person.id in people:
            return 'Person with this ID already exists.'
        people[person.id] = person
        return 'Person created successfully.'

    @rpc(Integer, _returns=Unicode)
    def delete_person(ctx, person_id):
        if person_id in people:
            del people[person_id]
            return 'Person deleted successfully.'
        else:
            return 'Person not found.'

application = Application([PersonService],
    tns='spyne.examples.person',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    server = make_server('127.0.0.1', 8000, wsgi_application)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/?wsdl")

    server.serve_forever()