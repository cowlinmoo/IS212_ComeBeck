from fastapi import APIRouter, Depends

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.schemas.TeamSchema import TeamSchema
from backend.services.TeamService import TeamService
from backend.services.dependencies import role_required

TeamRouter = APIRouter(
    prefix="/api/team",
    tags=["Team Endpoints"],
)


@TeamRouter.get("/{team_id}", response_model=TeamSchema)
def get_team_by_team_id(team_id: int,
                                  service: TeamService = Depends(),
                                  current_user: dict =
                                  Depends(role_required(EmployeeRole.HR,
                                                        EmployeeRole.MANAGER,
                                                        EmployeeRole.STAFF))):
    return service.get_team_employees_by_team_id(team_id)


@TeamRouter.get("/manager/{manager_id}", response_model=TeamSchema)
def get_team_by_manager_id(manager_id: int,
                                  service: TeamService = Depends(),
                                  current_user: dict =
                                  Depends(role_required(EmployeeRole.HR,
                                                        EmployeeRole.MANAGER))):
    return service.get_team_employees_by_manager_id(manager_id)
