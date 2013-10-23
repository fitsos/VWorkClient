from bottle import get, post, request, run, template, static_file, route, redirect
import xmltodict
import urllib2
import time
from twilio.rest import TwilioRestClient
from beaker.middleware import SessionMiddleware
import bottle

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1000,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

@route('/<path>') # route to show the home page has to be /home.html in order to show the html document properly
def server_static(path):
    print path
    return static_file(path, root='static/')

@bottle.route('/login', method='POST') # or @route('/login', method='POST')
def login_submit():
    name = request.forms.getall('test') # this is getting all form fields with a name of test
    #setting up the request to the api using the information from the form
    xml = """<?xml version='1.0' encoding='utf-8'?>
    <job>
    <customer_name>""" + name[0] +"""</customer_name>
          <planned_start_at type="datetime">2013-10-16T12:30:00+00:00</planned_start_at>
          <planned_duration>2500</planned_duration>
          <steps type="array">
            <step>
              <name>Pick up</name>
              <location>
                <formatted_address>"""+ name[1] +"""</formatted_address>
              </location>
            </step>
            <step>
              <name>Return Passengers</name>
              <location>
                <formatted_address>"""+ name[2] +"""</formatted_address>
              </location>
            </step>
          </steps>
    </job>"""

    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    url = 'http://api.vworkapp.com//2.0/jobs.xml?api_key=1tXGz8OBwqsAWLCbp4HL'
    req = urllib2.Request(url, xml, headers) #sending job request
    response = urllib2.urlopen(req) #getting the reponse from the api
    the_page = response.read() #reading response in XML
    parsed = xmltodict.parse(the_page) # parsing the XML response
    show = parsed['job']['id']['#text'] # grabbing the job id for the create job
    s = bottle.request.environ.get('beaker.session') # has to be called in order to save to sessions
    s['name'] = name
    s['show'] = show
    s.save()
    redirect("/jobs")

@bottle.route('/jobs')
def jobs():
    s = bottle.request.environ.get('beaker.session')
    s['name'] = "Andrew"
    test = s.get('name')
    output = template('jobs.tpl', test=test)
    return output


@bottle.route('/twilio', method='POST')
def twil():
    s = bottle.request.environ.get('beaker.session')
    n = s.get('show')
    jobs = "http://api.vworkapp.com/api/2.0/jobs/" + n + ".xml?api_key=1tXGz8OBwqsAWLCbp4HL"
    reqs = urllib2.Request(jobs) #sending job request
    responses = urllib2.urlopen(reqs) #getting the reponse from the api
    the_pages = responses.read() #reading response in XML
    parse = xmltodict.parse(the_pages)
    #print parse
    worker = parse['job']['worker_name']
    while worker is None:
        #print "none"
        time.sleep(10)
        reqs = urllib2.Request(jobs)
        responses = urllib2.urlopen(reqs)
        the_pages = responses.read()
        parse = xmltodict.parse(the_pages)
        worker = parse['job']['worker_name']
    # getting the worker id and requesting the worker lat and lng
    worker_id = parse['job']['worker_id']
    worker_response = "http://api.vworkapp.com/api/2.0/workers/" + worker_id + ".xml?api_key=1tXGz8OBwqsAWLCbp4HL"
    req = urllib2.Request(worker_response)
    url_response = urllib2.urlopen(req)
    page = url_response.read()
    par = xmltodict.parse(page)
    s = bottle.request.environ.get('beaker.session')
    s['lat'] = par['worker']['latest_telemetry']['lat']
    s['lng'] = par['worker']['latest_telemetry']['lng']
    s.save()
    lat = s.get('lat')
    lng = s.get('lng')
    print lat
    print lng
    output = template('index.tpl', lat=lat, lng=lng)
    return output

    #Twilio information below
    #account_sid = "AC23c4932bf583f5006bb48d22342d1702"
    #auth_token  = "ceb45f66b539b6e07be1933fbdaa1c8a"
    #client = TwilioRestClient(account_sid, auth_token)
    #message = client.sms.messages.create(body="You're driver is " + worker,
    #    to="+15104592120",    # Replace with your phone number
    #    from_="+15108580626") # Replace with your Twilio number

bottle.run(app=app)

run(host='localhost', port=8080)

