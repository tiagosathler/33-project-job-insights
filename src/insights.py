from src.jobs import read


def get_unique_job_types(path: str):
    """Checks all different job types and returns a list of them

    Must call `read`

    Parameters
    ----------
    path : str
        Must be passed to `read`

    Returns
    -------
    list
        List of unique job types
    """
    jobs = read(path)
    job_types = set()
    for job in jobs:
        job_types.add(job["job_type"])

    return list(job_types)


def filter_by_job_type(jobs: list[dict], job_type: str):
    """Filters a list of jobs by job_type

    Parameters
    ----------
    jobs : list
        List of jobs to be filtered
    job_type : str
        Job type for the list filter

    Returns
    -------
    list
        List of jobs with provided job_type
    """
    list_of_jobs = []
    for job in jobs:
        if job["job_type"] == job_type:
            list_of_jobs.append({"id": job["id"]})
    return list_of_jobs


def get_unique_industries(path: str):
    """Checks all different industries and returns a list of them

    Must call `read`

    Parameters
    ----------
    path : str
        Must be passed to `read`

    Returns
    -------
    list
        List of unique industries
    """
    jobs = read(path)
    industry_types = set()
    for job in jobs:
        if job["industry"] != "":
            industry_types.add(job["industry"])

    return list(industry_types)


def filter_by_industry(jobs: list[dict], industry: str):
    """Filters a list of jobs by industry

    Parameters
    ----------
    jobs : list
        List of jobs to be filtered
    industry : str
        Industry for the list filter

    Returns
    -------
    list
        List of jobs with provided industry
    """
    list_of_jobs = []
    for job in jobs:
        if job["industry"] == industry:
            list_of_jobs.append({"id": job["id"]})
    return list_of_jobs


def get_max_salary(path: str):
    """Get the maximum salary of all jobs

    Must call `read`

    Parameters
    ----------
    path : str
        Must be passed to `read`

    Returns
    -------
    int
        The maximum salary paid out of all job opportunities
    """
    jobs = read(path)
    max_salaries = [0]
    for job in jobs:
        if job["max_salary"].isdecimal():
            max_salaries.append(int(job["max_salary"]))
    return max(max_salaries)


def get_min_salary(path: str):
    """Get the minimum salary of all jobs

    Must call `read`

    Parameters
    ----------
    path : str
        Must be passed to `read`

    Returns
    -------
    int
        The minimum salary paid out of all job opportunities
    """
    jobs = read(path)
    min_salaries = [100000000]
    for job in jobs:
        if job["min_salary"].isdecimal():
            min_salaries.append(int(job["min_salary"]))
    return min(min_salaries)


def matches_salary_range(job: dict, salary: int):
    """Checks if a given salary is in the salary range of a given job

    Parameters
    ----------
    job : dict
        The job with `min_salary` and `max_salary` keys
    salary : int
        The salary to check if matches with salary range of the job

    Returns
    -------
    bool
        True if the salary is in the salary range of the job, False otherwise

    Raises
    ------
    ValueError
        If `job["min_salary"]` or `job["max_salary"]` doesn't exists
        If `job["min_salary"]` or `job["max_salary"]` aren't valid integers
        If `job["min_salary"]` is greather than `job["max_salary"]`
        If `salary` isn't a valid integer
    """
    job_keys = job.keys()
    job_values = job.values()

    if "min_salary" not in job_keys and "max_salary" not in job_keys:
        raise ValueError("keys 'min_salary' and 'max_salary' must be present")

    if not all([isinstance(value, int) for value in job_values]):
        raise ValueError("'min_salary' and 'max_salary' must be integers")

    if not isinstance(salary, int):
        raise ValueError("'salary' must be an integer")

    min_salary = job["min_salary"]
    max_salary = job["max_salary"]

    if min_salary >= max_salary:
        raise ValueError("'min_salary' must be less than to 'max_salary'")

    return min_salary <= salary <= max_salary


def filter_by_salary_range(jobs: list[dict], salary: int):
    """Filters a list of jobs by salary range

    Parameters
    ----------
    jobs : list
        The jobs to be filtered
    salary : int
        The salary to be used as filter

    Returns
    -------
    list
        Jobs whose salary range contains `salary`
    """
    filtered_jobs = []
    response = False

    for job in jobs:
        try:
            response = matches_salary_range(job, salary)
        except ValueError:
            pass
        else:
            if response:
                filtered_jobs.append(job)

    return filtered_jobs
