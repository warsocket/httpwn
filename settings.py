#files are unpriviligeduser and in the jaildir
try:
    settings = {
    "unpriviligeduser": "www-data",
    "jaildir": "/var/spool/httpwn.org",
    "logfilepath": "/connection_log.db",
    "requestlogpath": "/requestlog.txt",
    "protocol": "http",
    "servername": "httpwn.org"
    }
except:
    sys.stderr.write("%s\n" % "Error in settings file, ABORTING...") 

