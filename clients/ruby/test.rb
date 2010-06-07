require 'arecibo'

dict = {
  :account => 'youraccount number',
  :priority => 1,
  :url => "http://badapp.org",
  :uid => "sefsef",
  :ip => "127.0.0.1",
  :type => "sdfs",
  :server => "Test Script"
}
p = Arecibo.new("http://yourservername/v/1/", dict)
p.send