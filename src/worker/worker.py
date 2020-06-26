from src.case_classes.job_cc import JobCC
from src.case_classes.employee_cc import EmployeeCC
from src.db.db import DbConnection
from src.service.redis_queue import redis_queue
import datetime
import time


def assign_job(job_input: dict, hrs_required=None):
    job = JobCC(*job_input.values())
    session = DbConnection()
    session.insert_or_update_job(job)
    if not hrs_required:
        hrs_required = job.hrs_required
    employees = get_employee(job, hrs_required)
    if employees:
        for employee in employees:
            # Make employee unavailable
            session.update_employee_status_by_ids(str(employee.employee_id), job.job_id, False)
    else:
        _pushing_task_to_queue(job)


def get_employee(job_in_cc: JobCC, required_hrs):
    session = DbConnection()
    if not required_hrs:
        required_hrs = job_in_cc.hrs_required
    employees_available = session.get_available_employees()
    if not employees_available:
        return None
    else:
        sum_hrs = 0
        selected_employees = []
        for employee in employees_available:
            if required_hrs <= sum_hrs:
                break
            employee_obj = EmployeeCC(employee.employee_id, employee.available_hrs)
            selected_employees.append(employee_obj)
            sum_hrs += employee.available_hrs
        if sum_hrs < required_hrs :
            return None

        _schedule_trigger(job_in_cc)
        return selected_employees


def _pushing_task_to_queue(job_to_be_pushed, required_hrs=None):
    redis_queue.enqueue(assign_job, job_to_be_pushed.__dict__, required_hrs)


def _check_on_job(job_to_be_checked: JobCC):
    session = DbConnection()
    job_info = session.get_job_info(job_to_be_checked)
    if job_info:
        if job_info.status:
            session.update_employee_status_by_job_id(job_info.job_id, True)
        else:
            _add_employee_to_job(job_to_be_checked)


def _add_employee_to_job(current_job: JobCC):
    session = DbConnection()
    new_employee = session.get_available_employee()
    session.update_employee_status_by_ids(str(new_employee.employee_id), current_job.job_id, False)


def _schedule_trigger(job_to_be_checked_later: JobCC):
    job_hrs = job_to_be_checked_later.hrs_required
    # Use seconds here so we don't waste too much time here
    redis_queue.enqueue_in(datetime.timedelta(seconds=job_hrs * 2), _check_on_job, job_to_be_checked_later)
