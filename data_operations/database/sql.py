
class db_schema(object):

  def __init__(self):
    self.DB_NAME = 'nostradamus'
    return

  def tables(self):
    TABLES = {}
    '''
    TABLES['dept_emp'] = (
    "CREATE TABLE IF NOT EXISTS `dept_emp` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `dept_no` char(4) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
    '''
    
    TABLES['Sectors'] = (
    "CREATE TABLE IF NOT EXISTS `Sectors` ("
    "  `sector_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `s_p` float,"
    "  `real_estate` float,"
    "  `consumer_staples` float,"
    "  `health_care` float,"
    "  `utilities` float,"
    "  `materials` float,"
    "  `industrials` float,"
    "  `financials` float,"
    "  `energy` float,"
    "  `communication_services` float,"
    "  `consumer_discretionary` float,"
    "  `information_technology` float,"
    "  PRIMARY KEY (`sector_id`)"
    ") ENGINE=InnoDB")
    return TABLES