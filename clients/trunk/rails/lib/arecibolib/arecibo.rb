require 'net/http'
require 'uri'

class Arecibo
  def initialize data
    @data = data
    # where errors are going
    @arecibo_url = URI.parse('http://www.areciboapp.com/v/1/')
    # the length of time to wait for a server to respond
    @timeout = 10
  end
  
  def send
    # make a post
    post = Net::HTTP::Post.new(@arecibo_url.path)
    post.set_form_data(@data)
    # make request
    req = Net::HTTP.new(@arecibo_url.host, @arecibo_url.port)
    req.read_timeout = @timeout
    # push it through
    res = req.start {|http| http.request(post) }
    case res
    when Net::HTTPSuccess
        # ok, we don't need to do anything else
      else
        # let this bubble up to the rest of the script
        raise res.error!
      end
  end
end

