__author__ = 'fitsos'
from bottle import route, run, template, get, post, request, static_file # or route
import requests
import xmltodict, json

@route('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@route('/do_login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (( username == "" ) and ( password == "" )):
        text = "thanks"
        return template('{{text}}', text=text )
    else:
        print "error, try again"
        do_login()

@route('/create')
def created():
    xml = """<?xml version='1.0' encoding='utf-8'?>
    <job>
          <customer_name>Working</customer_name>
          <planned_start_at type="datetime">2013-10-16T05:30:00+00:00</planned_start_at>
          <planned_duration>7200</planned_duration>
          <steps type="array">
            <step>
              <name>Pick up goods</name>
              <location>
                <formatted_address>12 Heather Street, Auckland, NZ</formatted_address>
                <lat>-36.879621</lat>
                <lng>174.751282</lng>
              </location>
            </step>
            <step>
              <name>Return to base</name>
            </step>
          </steps>
    </job>"""
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    requests.post('http://api.vworkapp.com//2.0/jobs.xml?api_key=1tXGz8OBwqsAWLCbp4HL', data=xml, headers=headers)

@route('/show')
def show():
    # /2.0/jobs/[id].xml?[arguments]
    # example ID 1685598
    id = '/' + '1685809'
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    r = requests.get('http://api.vworkapp.com/api/2.0/jobs'+ id +'.xml?api_key=1tXGz8OBwqsAWLCbp4HL', headers=headers)
    text = r.text
    o = xmltodict.parse(text)                  #'<e> <a>text</a> <a>text</a> </e>'
    text = json.dumps(o)                       #'{"e": {"a": ["text", "text"]}}'
    print text
    job = text[0]
    print job
    return template('{{text}}', text=text )
    # return static_file("vworkclient.html", root='/Users/fitsos/PycharmProjects/VWorkClient/')

@route('/update')
def update():
    xml = """<job>

                <planned_duration>2000</planned_duration>
            </job>
            """
    # Formating is /2.0/jobs/[id].xml?[arguments]
    #
    # Job info in XML:
    # <id readonly="readonly">1673815</id>
    # <customer_name>Testing Co</customer_name>
    # <template_name>Pickup / Delivery</template_name>
    #
    # How you know it should work:
    # <confirmation>accepted</confirmation> will change to <confirmation>declined</confirmation>
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    r = requests.post('http://api.vworkapp.com/api/2.0/jobs/1673815.xml?api_key=1tXGz8OBwqsAWLCbp4HL', data=xml, headers=headers)

run(host='localhost', port=8080)


    # Job example
    #xml = """<?xml version='1.0' encoding='utf-8'?>
    #<job>
    #    <id readonly="readonly">123</id>
    #    <group_ids>2,33</group_ids>
    #    <customer_name>Joe Smith</customer_name>
    #    <template_name>Template</template_name>
    #    <worker_id>258</worker_id>
    #    <planned_duration>7200</planned_duration>
    #    <third_party_id>ACHME_12253</third_party_id>
    #    <planned_start_at>2011-12-25T22:32:07+00</planned_start_at>
    #    <confirmation>pending</confirmation>
    #    <steps type="array">
    #    <step>
    #      <name>Pick up goods</name>
    #      <location>
    #        <formatted_address>12 Heather Street, Auckland, NZ</formatted_address>
    #        <lat>-36.879621</lat>
    #        <lng>174.751282</lng>
    #      </location>
    #    </step>
    #    <step>
    #      <name>Return to base</name>
    #    </step>
    #    </steps>
    #    <custom_fields type="array">
    #    <custom_field>
    #      <name>Weight</name>
    #      <value>1.0</value>
    #      <type>free_text</type>
    #    </custom_field>
    #    </custom_fields>
    #</job>
    #        """
