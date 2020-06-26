from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from os import getenv
import logging
import traceback
from src.models.Job import Job
from src.case_classes.job_cc import JobCC
from src.case_classes.employee_cc import EmployeeCC
from src.models.Employee import Employee


class DbConnection:

    def __init__(self):
        self.session = self.start_session()

    @staticmethod
    def start_session():
        engine = create_engine('mysql+pymysql://{0}@{2}:{4}/{3}'.format('root', getenv('MYSQL_DB_PWD') , '127.0.0.1',
                                                                          'nextbee_media_job', '3306'))
        Session = sessionmaker(bind=engine)
        return Session()


    def close_sessions(self):
        self.session.close()

    def get_available_employees(self):
        try:
            query = self.session.query(Employee).filter(Employee.status).order_by(Employee.available_hrs.desc())
            query_result = query.all()
            return query_result
        except Exception:
            logging.error(traceback.format_exc())
            raise
        finally:
            self.close_sessions()

    def get_available_employee(self):
        try:
            query = self.session.query(Employee).filter(Employee.status).order_by(Employee.available_hrs)
            query_result = query.first()
            return query_result
        except Exception:
            logging.error(traceback.format_exc())
            raise
        finally:
            self.close_sessions()


    def get_job_info(self, job:JobCC):
        try:
            query = self.session.query(Job).filter(Job.job_id == job.job_id)
            query_result = query.first()
            return query_result
        except Exception:
            logging.error(traceback.format_exc())
            raise
        finally:
            self.close_sessions()


    def insert_or_update_job(self, job: JobCC):
        try:
            query = self.session.query(Job).filter(Job.job_id == job.job_id)
            query_result = query.all()
            if query_result:
                query.update({Job.status: False, Job.assignee: None, Job.hrs_required: job.hrs_required})
                self.session.commit()
            else:
                job = Job(job_id=job.job_id, job_desc=job.job_desc, hrs_required=job.hrs_required, status=False)
                self.session.merge(instance=job)
                self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise
        finally:
            self.session.close()


    def update_employee_status(self, employee: EmployeeCC, job_id: int, status: bool):
        try:
            query = self.session.query(Employee).filter(Employee.employee_id == employee.employee_id)
            query.update({Employee.status: status, Employee.job_id: job_id})
            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_employee_status_by_ids(self, employee_ids: str, job_id: int, status: bool):
        try:
            employee_ids = employee_ids.split(',')
            query = self.session.query(Employee).filter(Employee.employee_id.in_(employee_ids))
            query.update({Employee.status: status, Employee.job_id: job_id}, synchronize_session='fetch')
            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_employee_status_by_job_id(self, job_id: int, status: bool):
        try:
            query = self.session.query(Employee).filter(Employee.job_id == job_id)
            query.update({Employee.status: status, Employee.job_id: job_id}, synchronize_session='fetch')
            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise
        finally:
            self.session.close()