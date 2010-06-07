require 'arecibo'

dict = {
  :account => 'yournumber',
  :priority => 1,
  :url => "http://badapp.org",
  :uid => "123124123123",
  :ip => "127.0.0.1",
  :type => "ὕαλον ϕαγεῖν δύναμαι· τοῦτο οὔ με βλάπτει",
  :server => "Test Script"
}
p = Arecibo.new(dict)
p.send