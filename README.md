# CCC-Proj2

How to use TweetKey.py
1. If you have new key to Add then put your key in the file keyFile.kf with the following format.
    - #########################################################
    - access_token
    - access_token_secret
    - consumer_key
    - consumer_secret
2. create the object for the key:       "key = TweetKey()"
3. get total number of keys present:    "print(key.totalKeys())"
4. get the key with an index:           "print(key.getKey(2))"
Note: The key will return a list of 4 values in the same format as you put them in the file.
        The format is [access_token, access_token_secret, consumer_key, consumer_secret]
