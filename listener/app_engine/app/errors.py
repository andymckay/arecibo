from exceptions import Exception

class AccountDoesNotExist(Exception): pass
class OldUID(Exception): pass
class StatusDoesNotExist(Exception): pass
class RSSDisabled(Exception): pass
class CSVDisabled(Exception): pass
class JSONDisabled(Exception): pass
class XMLDisabled(Exception): pass