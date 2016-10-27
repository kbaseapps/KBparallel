# -*- coding: utf-8 -*-
#BEGIN_HEADER
from pprint import pprint
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport
import time
#END_HEADER


class KBParallel:
    '''
    Module Name:
    KBParallel

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/sean-mccorkle/KBparallel"
    GIT_COMMIT_HASH = "c7cbd48ecdebd57b688b8c326ecec7b72e93ce68"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.config = config

        # set default time limit
        if not 'time_limit' in config:
          self.config['time_limit']  = 5000000

        
        #END_CONSTRUCTOR
        pass


    def run(self, ctx, input_params):
        """
        :param input_params: instance of type "KBparallelrunInputParams"
           (run() method) -> structure: parameter "module_name" of String,
           parameter "method_name" of String, parameter "service_ver" of
           String, parameter "prepare_params" of list of unspecified object,
           parameter "collect_params" of list of unspecified object,
           parameter "client_class_name" of String, parameter "time_limit" of
           Long
        :returns: instance of type "Report" (A simple Report of a method run
           in KBase. It only provides for now a way to display a fixed width
           text output summary message, a list of warnings, and a list of
           objects created (each with descriptions). @optional warnings
           file_links html_links direct_html direct_html_link_index @metadata
           ws length(warnings) as Warnings @metadata ws length(text_message)
           as Size(characters) @metadata ws length(objects_created) as
           Objects Created) -> structure: parameter "text_message" of String,
           parameter "warnings" of list of String, parameter
           "objects_created" of list of type "WorkspaceObject" (Represents a
           Workspace object with some brief description text that can be
           associated with the object. @optional description) -> structure:
           parameter "ref" of type "ws_id" (@id ws), parameter "description"
           of String, parameter "file_links" of list of type "LinkedFile"
           (Represents a file or html archive that the report should like to
           @optional description) -> structure: parameter "handle" of type
           "handle_ref" (Reference to a handle @id handle), parameter
           "description" of String, parameter "name" of String, parameter
           "URL" of String, parameter "html_links" of list of type
           "LinkedFile" (Represents a file or html archive that the report
           should like to @optional description) -> structure: parameter
           "handle" of type "handle_ref" (Reference to a handle @id handle),
           parameter "description" of String, parameter "name" of String,
           parameter "URL" of String, parameter "direct_html" of String,
           parameter "direct_html_link_index" of Long
        """
        # ctx is the context object
        # return variables are: rep
        #BEGIN run
        print( "Hi this is KBParallel.run() input_params are")
        pprint( input_params )

        token = ctx['token']
        service_ver = "beta"
        if 'service_ver' in input_params and input_params['service_ver'] is not None: 
          service_ver = input_params['service_ver'] 


        #instantiate ManyHellos client here
        print( "about to initiate client .." )
        client = _BaseClient(self.callbackURL, timeout=self.config['time_limit'], service_ver=service_ver, token=token)

        # using manyHellos initializer (bad programming by Sean)
        #input_params = {
        #                'hello_msg': "Hai",
        #                'num_jobs': 3,
        #                'time_limit':  self.config['time_limit'],
        #                'njs_wrapper_url': self.config['njs-wrapper-url'],
        #                'token': token
        #               }
        #res = mh.manyHellos( input_params )
        #print( res )

        # issue prepare call

        print( "about to invoke prepare()")
        tasks_ret = client.call_method("{}.{1}_prepare".format(input_params['module_name'], 
                                                               input_params['method_name']),
                                       input_params["prepare_params"], 
                                       context=None)
        print( "back in run")
        tasks = tasks_ret[0]
        pprint( tasks )

        # initiate NJS wrapper
        print( "initiating NJS wrapper")
        njs = NJS( url=self.config['njs-wrapper-url'], token=self.token )  # Please fix hardcoded URL
        pprint( njs)
        for task in tasks:
            pprint( ["   launching task", task]  )
            #r1 = mh.manyHellos_runEach( ctx, task )
            #pprint( r1 )
            jobid = njs.run_job( { 'method': "{0}.{1}_runEach".format(input_params['module_name'], input_params['method_name']),
                                   'params': [task], 
                                   'service_ver':  service_ver} 
                               )
            print( "job_id", jobid )


        print( "about to invoke collect()" )
        res = client.call_method("{}.{1}_collect".format(input_params['module_name'], 
                                                         input_params['method_name']), 
                                 input_params["collect_params"], 
                                 context=None)        
        pprint( res )
        # for now, return a dummy object with a string message

        ret = { 'msg': "default KBparallel.run() return value" }
        #END run

        # At some point might do deeper type checking...
        if not isinstance(rep, dict):
            raise ValueError('Method run return value ' +
                             'rep is not type dict as required.')
        # return the results
        return [rep]

    def status(self, ctx, input_params):
        """
        :param input_params: instance of type "KBparallelstatusInputParams"
           (status() method) -> structure: parameter "joblist" of list of
           String
        :returns: instance of type "KBparallelstatusOutputObj" -> structure:
           parameter "num_jobs_checked" of Long, parameter "jobstatus" of
           list of String
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN status
        ret = notyet( "status" )
        #END status

        # At some point might do deeper type checking...
        if not isinstance(ret, dict):
            raise ValueError('Method status return value ' +
                             'ret is not type dict as required.')
        # return the results
        return [ret]

    def cancel_run(self, ctx, input_params):
        """
        :param input_params: instance of type "KBparallelcancel_runInput"
           (cancel_run() method)
        :returns: instance of type "KBparallelcancel_runOutput"
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN cancel_run
        ret = notyet( "cancel_run" )
        #END cancel_run

        # At some point might do deeper type checking...
        if not isinstance(ret, basestring):
            raise ValueError('Method cancel_run return value ' +
                             'ret is not type basestring as required.')
        # return the results
        return [ret]

    def getlog(self, ctx, input_params):
        """
        :param input_params: instance of type "KBparallelgetlogInput"
           (getlog() method)
        :returns: instance of type "KBparallelgetlogOutput"
        """
        # ctx is the context object
        # return variables are: ret
        #BEGIN getlog
        ret = notyet( "getlog" )
        #END getlog

        # At some point might do deeper type checking...
        if not isinstance(ret, basestring):
            raise ValueError('Method getlog return value ' +
                             'ret is not type basestring as required.')
        # return the results
        return [ret]