DROP TABLE IF EXISTS opportunities;
DROP TABLE IF EXISTS master_naturalist;

CREATE TABLE master_naturalist (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  email VARCHAR (255) UNIQUE NOT NULL,
  password LONGBLOB NOT NULL,
  admin TINYINT(1) DEFAULT 0,
  project_coordinator TINYINT(1) DEFAULT 0
);

CREATE TABLE opportunities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  owner INT,
  title VARCHAR (150) NOT NULL,
  body LONGTEXT NOT NULL,
  anywhere TINYINT(1) DEFAULT 0,
  anytime TINYINT(1) DEFAULT 0,
  location VARCHAR (255),
  city VARCHAR (50),
  event_start DATETIME,
  event_end DATETIME,
  expiration_date DATETIME,
  category VARCHAR (50),
  project_id VARCHAR (50),
  recurring_weekly TINYINT(1) DEFAULT 0,
  recurring_monthly INT,
  link VARCHAR (255),
  just_show_up TINYINT(1) DEFAULT 0,
  CONSTRAINT fk_category FOREIGN KEY (owner)
                         REFERENCES master_naturalist(id)
);
