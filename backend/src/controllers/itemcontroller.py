from bson.objectid import ObjectId
from datetime import datetime

from src.controllers.controller import Controller
from src.util.dao import DAO

class ItemController(Controller):
    def __init__(self, items_dao: DAO):
        super().__init__(dao=items_dao)

    def create(self, data: dict):
        """Create a new task object based on the data contained in the dict. The data must contain at least a userid, a video url and a title. If todos are contained in the data, create todo objects and associate them to the task

        attributes:
            data -- dict containing the data of the new task (at least a title, url, and userid)

        returns:
            task -- newly created task object
        
        raises:
            KeyError -- in case an important key is missing in the data dict
            Exception -- in case any database operation fails
        """

        # store the userid
        if 'userid' not in data:
            raise KeyError('When creating a task object, the userid of the associated user must be given')
        uid = data['userid']
        del data['userid']

        try:
            # add the video url
            video = self.videos_dao.create({'url': data['url']})
            del data['url']
            data['video'] = ObjectId(video['_id']['$oid'])

            # create and add todos
            todos = []
            for todo in data['todos']:
                todoobj = self.todos_dao.create({'description': todo, 'done': False})
                todos.append(ObjectId(todoobj['_id']['$oid']))
            data['todos'] = todos

            # create the task object and assign it to the user
            task = self.dao.create(data)
            self.users_dao.update(
                uid, {'$push': {'tasks': ObjectId(task['_id']['$oid'])}})
            return task['_id']['$oid']
        except Exception as e:
            raise