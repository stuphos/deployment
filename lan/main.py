# # server.py
# from SimpleXMLRPCServer import SimpleXMLRPCServer

# _peers = dict()

# def register_peer(name, address):
# 	_peers[name] = address

# def query_peers():
# 	return _peers

# def run():
# 	server = SimpleXMLRPCServer(('0.0.0.0', 8000))
# 	server.register_function(register_peer, 'peer.register')
# 	server.register_function(query_peers, 'peer.query')
# 	server.serve_forever()

from SimpleHTTPServer import BaseHTTPServer, SimpleHTTPRequestHandler
from urlparse import parse_qs
import json

peers = dict()

STATUS_PAGE = '''\
<html>
<head>
<script type="text/javascript">
</script>
</head>
<body>
<h2>Peers</h2>
<ul>
{status}
</ul>
</body>
</html>
'''

class Server(BaseHTTPServer.HTTPServer):
	class Handler(SimpleHTTPRequestHandler):
		server_version = "network/0.1"

		METHODS = {'peer.register': 'register_peer',
				   'peer.query': 'query_peers',
				   'droid': 'droid'}

		PAGES = {'status': 'status', '': 'status'}

		def do_GET(self):
			i = self.path.find('?')

			if i >= 0:
				qs = self.path[i+1:]
				path = self.path[:i]
				params = parse_qs(qs)
				params = dict((n, p[0]) if len(p) == 1 else p for (n, p) in params.iteritems())
			else:
				path = self.path
				params = dict()

			if path.startswith('/'):
				path = path[1:]

			try:
				if path.startswith('rpc/'):
					path = path[4:]
					method = getattr(self, self.METHODS[path])

					try: result = method(self, **params)
					except Exception, e:
						pass
					else:
						result = json.dumps(result)

						self.send_response(200)
						self.send_header("Content-type", 'application/json')
						self.send_header("Content-Length", str(result))
						self.end_headers()
						self.wfile.write(result)

				else:
					page = getattr(self, self.PAGES[path])
					result = page(self, **params)

					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					self.wfile.write(result)

			except Exception, e:
				print '%s: %s' % (e.__class__.__name__, e)
				self.send_response(500)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write('<h2>Server Error</h2>')

		def do_HEAD(self):
			pass


		def register_peer(self, request, name = None, address = None):
			e = request.client_address[0]
			r = peers.setdefault(e, dict())

			if len(r) >= 10:
				return 'Limit reached'

			if len(name) > 1000:
				return 'Name too long'

			if len(address) > 1000:
				return 'Address too long'

			r[name] = address
			return True

		def query_peers(self, request):
			return peers

  #def droid(self, request, method, arg):
      #import androidhelper as ah
      #d = ah()
      #getattr(d, method)(arg)

		def status(self, request):
			status = []
			for (e, addresses) in peers.iteritems():
				e = '?'
				a = []

				for (n, i) in addresses.iteritems():
					a.append('<li><a href="%s">%s (%s)</a></li>' % \
							 (i, n, i))

				a = '\n'.join(a)
				status.append('<li><h3>%s</h3><ul>%s</ul></li>' % (e, a))

			return STATUS_PAGE.format(status = '\n'.join(status))


	@classmethod
	def Run(self):
		i = self(('0.0.0.0', 8000), self.Handler)
		print 'serving'
		i.serve_forever()
		return i


def run():
	Server.Run()

if __name__ == '__main__':
	run()
