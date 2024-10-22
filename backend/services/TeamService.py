from typing import Optional

from fastapi import Depends, HTTPException
from pydantic import parse_obj_as
from sqlalchemy import inspect

from backend.models import Team
from backend.repositories.DepartmentRepository import DepartmentRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.TeamRepository import TeamRepository
from backend.schemas.BaseSchema import BaseEmployeeInfo, BaseDepartmentInfo, BaseEmployeeSchema, BaseTeamInfo
from backend.schemas.TeamSchema import TeamSchema


class TeamService:
    def __init__(
            self,
            teamRepository: TeamRepository = Depends(),
            departmentRepository: DepartmentRepository = Depends(),
            employeeRepository: EmployeeRepository = Depends()
    ) -> None:
        self.teamRepository = teamRepository
        self.departmentRepository = departmentRepository
        self.employeeRepository = employeeRepository

    def get_team_employees_by_team_id(self, team_id: int) -> TeamSchema:
        team = self.teamRepository.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        return self.team_to_schema(team)

    def team_to_schema(self, team: Team) -> TeamSchema:
        department = self.departmentRepository.get_department_by_id(team.department_id)
        manager = self.employeeRepository.get_employee(team.manager_id) if team.manager_id else None
        members = self.employeeRepository.get_employees_by_team_id(team.team_id)
        def orm_to_dict(obj):
            return {c.key: getattr(obj, c.key)
                    for c in inspect(obj).mapper.column_attrs}

        team_dict = {
            "team_id": team.team_id,
            "name": team.name,
            "description": team.description,
            "department": BaseDepartmentInfo.model_validate(orm_to_dict(department)) if department else None,
            "manager": BaseEmployeeInfo.model_validate(orm_to_dict(manager)) if manager else None,
            "parent_team": BaseTeamInfo.model_validate(orm_to_dict(team.parent_team)) if team.parent_team else None,
            "child_teams": [BaseTeamInfo.model_validate(orm_to_dict(child_team)) for child_team in
                            team.child_teams] if team.child_teams else None,
            "members": [BaseEmployeeSchema.model_validate(orm_to_dict(member)) for member in
                        members] if members else None
        }

        return TeamSchema.model_validate(team_dict)