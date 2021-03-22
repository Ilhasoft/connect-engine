import requests
from django.utils import timezone

from weni import utils
from weni.authentication.models import User
from weni.celery import app
from weni.common.models import Service, Organization


@app.task()
def status_service() -> None:
    def is_page_available(url: str, method_request: requests, **kwargs) -> bool:
        """This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        False.
        """
        try:
            response = method_request(url=url, **kwargs)
            if int(response.status_code) == 200:
                return True
            return False
        except Exception:
            return False

    for service in Service.objects.all():
        service.status = is_page_available(
            url=service.url, method_request=requests.get, timeout=10
        )
        service.last_updated = timezone.now()
        service.save(update_fields=["status", "last_updated"])


@app.task(name="delete_organization")
def delete_organization(inteligence_organization: int, user_email):
    grpc_instance = utils.get_grpc_types().get("inteligence")
    grpc_instance.delete_organization(
        organization_id=inteligence_organization,
        user_email=user_email,
    )
    return True


@app.task(name="update_organization")
def update_organization(inteligence_organization: int, organization_name: str):
    grpc_instance = utils.get_grpc_types().get("inteligence")
    grpc_instance.update_organization(
        organization_id=inteligence_organization,
        organization_name=organization_name,
    )
    return True


@app.task(name="update_user_permission_organization")
def update_user_permission_organization(
    inteligence_organization: int, user_email: str, permission: int
):
    grpc_instance = utils.get_grpc_types().get("inteligence")
    grpc_instance.update_user_permission_organization(
        organization_id=inteligence_organization,
        user_email=user_email,
        permission=permission,
    )
    return True


@app.task(name="update_project")
def update_project(organization_uuid: str, user_email: str, organization_name: str):
    grpc_instance = utils.get_grpc_types().get("flow")
    grpc_instance.update_project(
        organization_uuid=organization_uuid,
        user_email=user_email,
        organization_name=organization_name,
    )
    return True


@app.task(name="delete_project")
def delete_project(inteligence_organization: int, user_email):
    grpc_instance = utils.get_grpc_types().get("flow")
    grpc_instance.delete_project(
        project_uuid=inteligence_organization,
        user_email=user_email,
    )
    return True


@app.task(name="update_user_permission_project")
def update_user_permission_project(
    flow_organization: str, user_email: str, permission: int
):
    grpc_instance = utils.get_grpc_types().get("flow")
    grpc_instance.update_user_permission_project(
        organization_uuid=flow_organization,
        user_email=user_email,
        permission=permission,
    )
    return True


@app.task(name="migrate_organization")
def migrate_organization(user_email: str):
    user = User.objects.get(email=user_email)
    grpc_instance = utils.get_grpc_types().get("inteligence")

    organizations = grpc_instance.list_organizations(user_email=user_email)

    for organization in organizations:
        org, created = Organization.objects.get_or_create(
            inteligence_organization=organization.get("id"),
            defaults={"name": organization.get("name"), "description": ""},
        )

        role = grpc_instance.get_user_organization_permission_role(
            user_email=user_email, organization_id=organization.get("id")
        )

        org.authorizations.create(user=user, role=role)
