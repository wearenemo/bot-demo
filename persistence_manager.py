import os
import pickle

from game.exceptions import CrapsException


class PersistenceException(CrapsException):
    pass


class SaveException(PersistenceException):
    pass


class LoadException(PersistenceException):
    pass


class PersistenceManager:

    DATA = 'Data'
    GUILDS = 'Guilds'
    GUILD = 'Guild'
    TABLE = 'Table'
    DOT_PICKLE = '.pickle'

    @classmethod
    def save_table(cls, table):
        """
        Saves Table's players
        """
        return cls._save(table, table._id, cls.TABLE, lambda t: t._players)

    @classmethod
    def load_table(cls, table_id: int):
        """
        Loads Table's players
        """
        return cls._load(cls.TABLE, table_id, default={})

    ####################
    # Private methods
    #

    @classmethod
    def _path_for(cls, resource_type, resource_id: int):
        cwd = os.getcwd()
        path = None
        filename = None
        if resource_type == cls.TABLE:
            filename = f'{cls.TABLE}{cls.DOT_PICKLE}'
            path = os.path.join(
                cwd,
                f'/{cls.DATA}/{cls.GUILDS}/{cls.GUILD}_{resource_id}/{filename}')
        if not path:
            raise PersistenceException(
                f"No save path for resource of type {resource_type}")
        return path, filename

    @classmethod
    def _make_path_if_non_existent(cls, path):
        if not os.path.isfile(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                print("ERROR making file", exc)
                raise PersistenceException(
                    f"Can't create save path {path}: {exc}")
            except Exception as exc:
                print("EXCEPTION making file", exc)

    @classmethod
    def _save(cls, resource, resource_id, r_type, resource_callback=None):
        success = False
        try:
            path, filename = cls._path_for(r_type, resource_id)
            cls._make_path_if_non_existent(path)
            with open(path, 'wb') as f:
                try:
                    if resource_callback:
                        resource = resource_callback(resource)
                    pickle.dump(resource, f, protocol=pickle.HIGHEST_PROTOCOL)
                    success = True
                except pickle.PickleError as pe:
                    print('pickle error:', pe)
                    raise PersistenceException(str(pe))
                except BaseException as exc:
                    print("pickling exception:", exc)
                f.close()
        except PersistenceException as exc:
            print('persistence exception:', exc)
            raise SaveException(f"Can't save resource: {exc}")
        return success

    @classmethod
    def _load(cls, resource_type, resource_id, default=None):
        resource = default
        try:
            path, filename = cls._path_for(resource_type, resource_id)
            if not os.path.exists(path):
                raise LoadException(
                    f"Save file does not exist for {resource_type} "
                    f"at path {path}"
                )
            with open(path, 'rb') as f:
                try:
                    resource = pickle.load(f)
                except pickle.PickleError as pe:
                    raise PersistenceException(str(pe))
        except PersistenceException as exc:
            raise LoadException(f"Can't load resource: {exc}")
        finally:
            return resource
