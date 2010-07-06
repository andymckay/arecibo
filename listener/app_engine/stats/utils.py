from error.models import Error

# get around the 1000 count limit, based on
# http://notes.mhawthorne.net/post/172608709/appengine-counting-more-than-1000-entities
max_fetch = 1000

def count(*filters):
    count = 0

    query = Error.all(keys_only=True)
    for k, v in filters:
        query = query.filter(k, v)

    query = query.order('__key__')

    while count % max_fetch == 0:
        current_count = query.count()
        if current_count == 0:
            break
        count += current_count

        if current_count == max_fetch:
            last_key = query.fetch(1, max_fetch - 1)[0]
            query = query.filter('__key__ > ', last_key)

    return count