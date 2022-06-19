from msrest.authentication import BasicAuthentication
from azure.devops.released.work_item_tracking.work_item_tracking_client import WorkItemTrackingClient
from tracker.config import settings

class Details(str):
    PERSONAL_ACCESS_TOKEN = settings.personal_access_token
    ORGANIZATION_URL = settings.organization_url
    QUERY_ID = settings.query_id
    BUSINESS_UNIT = 'Backend'
    ORGANIZATION = 'HRKJ_ORG'
    COMPANY = 'Harsh Developers'


def get_credentials(personal_access_token):
    credentials = BasicAuthentication('', personal_access_token)
    return credentials


def get_work_items(personal_access_token, organization_url, query_id):

    credentials = get_credentials(personal_access_token)

    wit = WorkItemTrackingClient(base_url=organization_url, creds=credentials)
    workitems = wit.query_by_id(query_id)

    work_items_dict = {}
    for work_item in workitems.work_items:
        work_item_obj = wit.get_work_item(work_item.id)

        if not 'System.Description' in work_item_obj.fields.keys():
            work_item_obj.fields['System.Description'] = ''
        # print(work_item_obj.fields['System.Description'])
        work_items_dict[work_item.id] = work_item_obj

    return work_items_dict

work_items = get_work_items(
    Details.PERSONAL_ACCESS_TOKEN,
    Details.ORGANIZATION_URL,
    Details.QUERY_ID
)
