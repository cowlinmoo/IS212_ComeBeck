from typing import Optional, List
from fastapi import Depends, HTTPException
from sqlalchemy import inspect
from datetime import datetime

from backend.repositories.DepartmentRepository import DepartmentRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.TeamRepository import TeamRepository
from backend.schemas.BaseSchema import BaseEmployeeInfo, BaseTeamInfo, BaseDepartmentInfo
from backend.schemas.DepartmentSchema import DepartmentSchema, TeamSchema

class DepartmentService:
    def __init__(
            self,
            team_repository: TeamRepository = Depends(),
            department_repository: DepartmentRepository = Depends(),
            employee_repository: EmployeeRepository = Depends()
    ) -> None:
        self.team_repository = team_repository
        self.department_repository = department_repository
        self.employee_repository = employee_repository

    def get_department_by_department_id(self, department_id: int) -> DepartmentSchema:
        department = self.department_repository.get_department_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        return self.department_to_schema(department)

    def department_to_schema(self, department) -> DepartmentSchema:
        director = self.employee_repository.get_employee(department.director_id) if department.director_id else None
        teams = self.team_repository.get_teams_by_department_id(department.department_id)

        department_dict = {
            "department_id": department.department_id,
            "name": department.name,
            "description": department.description,
            "director_id": department.director_id,
            "director": self.employee_to_schema(director) if director else None,
            "teams": [self.team_to_schema(team) for team in teams] if teams else None
        }

        return DepartmentSchema.model_validate(department_dict)

    def team_to_schema(self, team) -> TeamSchema:
        manager = self.employee_repository.get_employee(team.manager_id) if team.manager_id else None
        members = self.employee_repository.get_employees_by_team_id(team.team_id)
        child_teams = self.team_repository.get_child_teams(team.team_id)
        parent_team = self.team_repository.get_team(team.parent_team_id) if team.parent_team_id else None

        team_dict = {
            "team_id": team.team_id,
            "name": team.name,
            "description": team.description,
            "department": self.department_to_base_schema(team.department),
            "manager": self.employee_to_schema(manager) if manager else None,
            "parent_team": self.team_to_base_schema(parent_team) if parent_team else None,
            "child_teams": [self.team_to_base_schema(child_team) for child_team in child_teams] if child_teams else None,
            "members": [self.employee_to_schema(member) for member in members] if members else None
        }

        return TeamSchema.model_validate(team_dict)

    def team_to_base_schema(self, team) -> BaseTeamInfo:
        return BaseTeamInfo(
            team_id=team.team_id,
            name=team.name,
            description=team.description
        )

    def employee_to_schema(self, employee) -> BaseEmployeeInfo:
        return BaseEmployeeInfo(
            staff_id=employee.staff_id,
            staff_fname=employee.staff_fname,
            staff_lname=employee.staff_lname
        )

    def department_to_base_schema(self, department) -> BaseDepartmentInfo:
        return BaseDepartmentInfo(
            department_id=department.department_id,
            name=department.name
        )