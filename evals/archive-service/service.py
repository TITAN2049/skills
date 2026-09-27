"""Small in-memory service used to evaluate specialist cooperation."""
from copy import deepcopy


class ApiError(Exception):
    def __init__(self, status, code):
        super().__init__(code)
        self.status = status
        self.code = code


class Store:
    def __init__(self, projects):
        self._projects = deepcopy(projects)

    def list_projects(self, actor):
        if actor is None:
            raise ApiError(401, "unauthenticated")
        return deepcopy([
            project for project in self._projects
            if project["workspace_id"] == actor["workspace_id"]
        ])
