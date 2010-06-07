require 'arecibolib/arecibo'
require 'socket'
require 'time'

class ActionController::Base
  def override_arecibo(exception)
      # this is a method once all the data
      # has been prepared for the default setup
      # if you would like to change it now is
      # good chance to do so, eg: change priority
      # or exclude some kinds of errors, or certain ips
  end
  
  def report_to_arecibo(exception)
    @arecibodata = {
      :account => ARECIBO_ACCOUNT_NUMBER,
      :msg => "",
      :url => "#{request.protocol}#{request.host_with_port}#{request.request_uri}",
      :user_agent => request.user_agent,
      :server => Socket.gethostname,
      :ip => request.remote_ip,
      :uid => Time.new.to_i
    }
    
    name = exception.class.name
    notfounds = ["ActionController::RoutingError","ActiveRecord::RecordNotFound",
                 "ActionController::UnknownController", "ActionController::UnknownAction"]
    if notfounds.index(name)
        @arecibodata[:status] = 404
        @arecibodata[:priority] = 5
    else
        @arecibodata[:status] = 500
        @arecibodata[:priority] = 1
    end
    
    @arecibodata[:type] = exception.class.name
    @arecibodata[:traceback] = exception.exception.to_s + "\n\n" + "#{exception.backtrace.join("\n")}"
    # make a nice message out of the post @arecibodata
    request.env.each { |k, v| @arecibodata[:msg] += "#{k.to_s}: #{v.to_s}\n"  }
    @arecibodata[:msg] = "#{params.inspect}\n\n#{@arecibodata[:msg]}"
    
    override_arecibo(exception)
    
    begin 
      p = Arecibo.new(@arecibodata)
      p.send
    rescue 
      logger.error "Posting to Arecibo failed with: #{$!} for error #{@arecibodata[:type]}"
    end
    
    # experimental
    begin
      render :template => ARECIBO_RESULT_TEMPLATE, 
             :status => @arecibodata[:status]
    rescue
      # pass, if ARECIBO_RESULT_TEMPLATE fails, ignore this
    end
  end
end
