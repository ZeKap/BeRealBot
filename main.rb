require 'twitter'
require_relative 'tokens'
require_relative 'tweets'

# vars for prog
debug = true
minDays = 2
maxDays = 3
lastTweet = ""

# try to connect with tweeter api
def connect_api()
    keys = getKeys()
    apiKey          = keys["apiKey"]
    apiSecret       = keys["apiSecret"]
    accessToken     = keys["accessToken"]
    accessSecret    = keys["accessSecret"]

    $client = Twitter::REST::Client.new do |config|
        config.consumer_key = apiKey
        config.consumer_secret = apiSecret
        config.access_token = accessToken
        config.access_token_secret = accessSecret
    end
end

puts $client
