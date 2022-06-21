import os
from dashboard.utils import Details
import shutil
import openpyxl


def create_excel(work_item):
    try:
        id = work_item.id
        title = work_item.title
        org = Details.ORGANIZATION

        title = '-'.join(title.split(' '))
        file_name = f"CR-{id}-{title}.xlsx"

        path = os.path.join(os.getcwd(), 'docs/CR')
        if not os.path.exists(path):
            os.makedirs(path)
        template = os.path.join(path, "template.xlsx")
        cr_excel = os.path.join(path, file_name)

        shutil.copyfile(template, cr_excel)

        workbook = openpyxl.load_workbook(cr_excel)
        sheet = workbook.active

        sheet['A3'] = f"Project Code: {org}"
        sheet['A4'] = "Version of the work product: "
        sheet['A5'] = "Reviewer(s): "
        sheet['A6'] = "Review Date: "
        sheet['A7'] = "Effort spent on review (man-hour): "
        sheet['A8'] = f"Incident No: {id}"
        sheet['A9'] = f"Description: {title}"

        workbook.save(cr_excel)
        file_path = os.path.join(path, file_name)
        return {'message': "CR Document Created", 'file_path': file_path, 'file_name': file_name}

    except Exception as e:
        print(e)
        return {'message': "Cannot Create Document", 'file_path': None, 'file_name': None}
