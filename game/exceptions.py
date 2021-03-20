class CrapsException(Exception): pass;
class CrapsManagerException(CrapsException): pass;
class SeatsTaken(CrapsManagerException): pass;
class DoesNotExist(CrapsManagerException): pass;
class AlreadyExists(CrapsManagerException): pass;
class DealerException(CrapsException): pass;