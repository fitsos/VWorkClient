import logging
from bottle import route, run, request, template
import requests
import os

print("vworkapp.py running")
print os.environ["PORT"]
print os.environ["IP"]
@route('/hello/<name>')
def getjobs(name='World'):
    r = requests.post("http://api.vworkapp.com//2.0/jobs.xml?api_key=1tXGz8OBwqsAWLCbp4HL")
    text = r.text

    return template('{{text}}', text=text)



@route('/createjobs')
def create():
    
    r = requests.delete("http://api.vworkapp.com/2.0/jobs/1679570.xml?api_key=1tXGz8OBwqsAWLCbp4HL")
    text = r.text

    return template('{{text}}', text=text)


@route('/create')
def created():
    print "calling function"
    xml = """<?xml version='1.0' encoding='utf-8'?>
    <job>
          <customer_name>Proxy</customer_name>
          <planned_start_at type="datetime">2013-10-16T05:30:00+00:00</planned_start_at>
          <planned_duration>7200</planned_duration>
          <steps type="array">
            <step>
              <name>Pick up goods</name>
              <location>
                <formatted_address>225 Bush St, San Francisco, CA</formatted_address>
                <lat>-36.879621</lat>
                <lng>174.751282</lng>
              </location>
            </step>
            <step>
              <name>Return to base</name>
            </step>
          </steps>
    </job>"""
    print xml
    print "the"
    print os.environ["PORT"]
    print os.environ["IP"]
    # headers = {'Content-Type': 'application/xml'} # set what your server accepts
    # print requests.post('http://api.vworkapp.com//2.0/jobs.xml?api_key=1tXGz8OBwqsAWLCbp4HL', data=xml, headers=headers)
run(host=os.environ["IP"], port=os.environ["PORT"]) # This is used to be able to run this code on C9