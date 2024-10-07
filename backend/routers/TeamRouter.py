from fastapi import APIRouter, Depends

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.services.TeamService import TeamService
from backend.services.dependencies import role_required

TeamRouter = APIRouter(
    prefix="/api/team",
    tags=["Team Endpoints"],
)

@TeamRouter.get("/{team_id}")
def get_team_employees_by_team_id(team_id: int,
                                  service: TeamService = Depends(),
                                  current_user: dict =
                                  Depends(role_required(EmployeeRole.HR,
                                                        EmployeeRole.MANAGER, EmployeeRole.STAFF))):
    return service.get_team_employees_by_team_id(team_id)
