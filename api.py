from keystoneclient.v2_0.client import Client as ks_client
from keystoneclient.openstack.common.apiclient import exceptions

def authenticate(username, password, authobj=None):
    ''' Authenticate using Keystone, returns authentication object'''
    try:
        authobj = ks_client(
            username=username,
            password=password,
            auth_url="https://identity.api.rackspacecloud.com/v2.0")
    except exceptions.Unauthorized:
        print "Authentication Failed. Unauthorized"

    return authobj


class RequestEngine(object):

    def __init__(self, session):
        self.session = session
        self.endpoint = {'service_type': 'rax:monitor'}

    def get(self, location):
        return self.session.get(location,
                                endpoint_filter=self.endpoint).json()

    def post(self, location, json=None):
        return self.session.post(location,
                                 endpoint_filter=self.endpoint,
                                 json=json).json()

    def put(self, location, json=None):
        return self.session.put(location,
                                endpoint_filter=self.endpoint,
                                json=json).json()

    def delete(self, location):
        return self.session.delete(location,
                                   endpoint_filter=self.endpoint).json()


class GeneralCalls:

    def list_check_types(self, authobj):
        ''' List available check types '''
        location = "check_types"
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_check_type(self, authobj, check_type_id):
        ''' Full details of check type '''
        location = "check_types/%s" % check_type_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def list_notification_types(self, authobj):
        ''' List available notification types '''
        location = "notification_types"
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_notification_type(self, authobj, notification_type_id):
        ''' Full details of notification type '''
        location = "notification_types/%s" % notification_type_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def list_monitoring_zones(self, authobj):
        ''' List Monitoring Zones '''
        location = "monitoring_zones"
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_monitoring_zone(self, authobj, monitoring_zone_id):
        location = "monitoring_zones/%s" % monitoring_zone_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def trace_monitoring_zone(self, authobj, address, resolver=None):
        ''' Takes a FQDN/IP and will attempt to traceroute from
            monitoring collectors in a specific monitoring zone'''
        return


class EntityManager:

    def __init__(self, session):
        self.request = RequestEngine(session)

    def list(self):
        ''' Lists all entities on account '''
        location = "entities"
        entities = []
        for entity in self.request.get(location)['values']:
            entities.append(Entity(entity))
        return entities

    def get(self, entity_id):
        ''' Retrieves full entity details '''
        location = "entities/%s" % entity_id
        return Entity(self.request.get(location))

    def delete(self, entity_id):
        ''' Delete an entity '''
        location = "entities/%s" % entity_id
        return self.request.delete(location).json()

    def update(self, authobj, entity_id, entity_label):
        ''' Update entity label '''
        location = "entities/%s" % entity_id
        payload = {"label": entity_label}
        return self.request.update(location, json=payload).json()


class Entity(object):

    def __init__(self, raw_json):
        self.id = raw_json['id']
        self.name = raw_json['label']

    def __repr__(self):
        return '<entity %s>' % self.name

    def show(self):
        print self.id + " | " + self.name


class Checks:

    def list_checks(self, authobj, entity_id):
        ''' Given an entity, lists all checks '''
        location = "entities/%s/checks" % entity_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_check(self, authobj, entity_id, check_id):
        ''' Given an entity and check, list check details '''
        location = "entities/%s/checks/%s" % (entity_id, check_id)
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def update_check(self, authobj, entity_id, check_id, check_payload):
        ''' Placeholder until I can figure out how to implement this as checks
            can have a fairly unregular json, possibly just allow raw json
            and parse results  Verb=put'''

    def del_check(self, authobj, entity_id, check_id):
        ''' Given an entity and check, delete the check '''
        location = "entities/%s/checks/%s" % (entity_id, check_id)
        http_verb = "delete"
        return RequestEngine.make_request(authobj, location, http_verb)


class Alarms:

    def list_alarms(self, authobj, entity_id):
        ''' Given Entity, list all Alarms '''
        location = "entities/%s/alarms" % entity_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_alarm(self, authobj, entity_id, alarm_id):
        ''' Given Entity and Alarm, show full alarm details '''
        location = "entities/%s/alarms/%s" % (entity_id, alarm_id)
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def del_alarm(self, authobj, entity_id, alarm_id):
        ''' Given Entity and Alarm, delete the alarm '''
        location = "entities/%s/alarms/%s" % (entity_id, alarm_id)
        http_verb = "delete"
        return RequestEngine.make_request(authobj, location, http_verb)

    def test_alarm(self, authobj, entity_id, alarm_json):
        ''' Sends alarm to test-alarm endpoint for test '''
        location = "entities/%s/test-alarm" % entity_id
        http_verb = "post"
        return RequestEngine.make_request(
                authobj, location, http_verb, alarm_json)


class Notifications:

    def list_notifications(self, authobj):
        ''' List all notifications '''
        location = "notifications"
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_notification(self, authobj, notification_id):
        ''' Given a notification_id, provide full notification details '''
        location = "notifications/%s" % notification_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def test_notification(self, authobj, notification_id):
        ''' Given a notification_id, test the notification '''
        location = "notifications/%s/test" % notification_id
        http_verb = "post"
        return RequestEngine.make_request(authobj, location, http_verb)

    def update_notification(self, authobj, notification_id, notification_json):
        ''' Given a JSON, update the given notification_id '''
        location = "notifications/%s" % notification_id
        http_verb = "post"
        return RequestEngine.make_request(
                authobj, location, http_verb, notification_json)

    def del_notification(self, authobj, notification_id):
        ''' Given a notification_id, delete the notification_id '''
        location = "notifications/%s" % notification_id
        http_verb = "delete"
        return RequestEngine.make_request(authobj, location, http_verb)


class NotificationPlans:

    def list_notification_plans(self, authobj):
        ''' List all notification plans '''
        location = "notification_plans"
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def get_notification_plan(self, authobj, notification_plan_id):
        ''' Given a notification_plan_id, provide full details '''
        location = "notification_plans/%s" % notification_plan_id
        http_verb = "get"
        return RequestEngine.make_request(authobj, location, http_verb)

    def del_notification_plan(self, authobj, notification_plan_id):
        ''' Given a notification_plan_id, delete the notification_plan '''
        location = "notification_plan/%s" % notification_plan_id
        http_verb = "delete"
        return RequestEngine.make_request(authobj, location, http_verb)

    def update_notification_plan(
            self, authobj, notification_plan_id, notification_plan_json):
        ''' Given a notification_plan_id, update with the given json '''
        location = "notification_plans/%s" % notification_plan_id
        http_verb = "put"
        return RequestEngine.make_request(
                authobj, location, http_verb, notification_plan_json)
